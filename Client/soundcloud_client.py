#!/usr/bin/python
import MySQLdb
import soundcloud
import pygst
import gst
import Queue
import time
import os
import signal
from threading import Timer

# creates a player object to be called when playing songs
class Player(object):

	#constructor
	def __init__(self, channel):
		#defines a pipeline, and a player. Adds player to pipeline
		self.pipeline = gst.Pipeline("player")
		self.player = gst.element_factory_make("playbin", "player")
		self.pipeline.add(self.player)

		#pulse sink for audio and fakesink for video
		pulse = gst.element_factory_make("alsasink", "alsa")
		fakesink = gst.element_factory_make("fakesink", "fakesink")

		#video properties are retained to "trick" the pi that there is a channel for video, not nescessary
		self.player.set_property('uri', channel)
		self.player.set_property("audio-sink", pulse)
		self.player.set_property("video-sink", fakesink)

		#sets the bus and signal watch to check for changes to the bus
		self.bus = self.player.get_bus()
		self.bus.add_signal_watch()
		self.bus.enable_sync_message_emission()
		
		#emits message
		self.bus.connect("message", self.on_message)

	#actions to take when an error message is emitted
	def on_message(self, bus, message):
		t = message.type
		print t

	#play song
	def play(self):
		self.pipeline.set_state(gst.STATE_PLAYING)
	
	#pause song
	def pause(self):
		self.pipeline.set_state(gst.STATE_PAUSED)

	#stop song
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)


#connects and queries database
db = MySQLdb.connect(host="<hostname>", user="<user>", passwd="<password>", db="songs")
cur = db.cursor()
cur.execute("SELECT * FROM songs")

playlist = Queue.Queue()

#create a client object with your app credentials
#NOTE: EVENTUALLY NEEDS TO ADD URL COLUMN TO DATABASE, TO REDUCE REDUNDANCY
client = soundcloud.Client(client_id='<clientid>')

#Fetches and stores each URL and adds it to the playlist queue
for row in cur.fetchall() :
	track = client.get('/tracks/'+str(row[1]))
	duration = row[4]
	stream_url = client.get(track.stream_url, allow_redirects=False)
	playlist.put((stream_url.location, duration))

#control enabled via keyboard
def input_with_timeout(dur, player):

	#function to kill player
	def killit():
		os.kill(os.getpid(), signal.SIGINT)

	#timer with kill function tagged onto end
	t = Timer(dur/1000, killit)
	
	#plays
	player.play()
	try:
		#starts timer
		t.start()
		#awaits user input and acts based on input
		keyboard = raw_input("Enter your next command...")
		while 1:
			if keyboard == "play":
				player.play()
				t.start()
			elif keyboard == "pause":
				player.pause()
				t.sleep()
			elif keyboard == "stop":
				player.stop()
				t.cancel()
				return "stop"
			elif keyboard == "next":
				player.stop()
				t.cancel()
				return "next"
	except KeyboardInterrupt:
		print "Exception thrown"		
		pass
	player.stop()
	t.cancel()
	print "Timer cancelled"
	return

#"main" section, where as long as the playlist is empty, loops	
while(playlist.empty()!=True):
	#gets a temp url and duration from tuple stored in queue
	tmp_url, dur = playlist.get()
	
	#creates new player object for current song
	player = Player(tmp_url)
	
	#gets input value from player object
	value = input_with_timeout(dur, player)
	
	#if the user told the player to stop, it stops
	if(value == "stop"):
		break

