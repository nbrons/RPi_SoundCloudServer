# Raspberry Pi SoundCloud Server
A Soundcloud Server that can stream your SoundCloud Library from your Raspberry Pi


<h2>Setup Instructions</h2>
<ol>

<li> Set up a working web server with mysql and php. I decided to run a server through DigitalOcean, running Ubuntu and LAMP</li>
<li> Upload "Server" files onto the server </li>
<li> Create a new SoundCloud application and specify the Redirect URL (which will be the location of callback.html) </li>
<li> Set up a new mySQL database on your server. The database should be called "songs", with a table called "songs" 
<ul><li> Run the following MySQL command once the database has been created: "CREATE TABLE songs (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, trackid INT (6) NOT NULL, title VARCHAR(60) NOT NULL, artwork_url VARCHAR (200), duration INT (10));</li></ul>
<li> Go to the location of index.html on your server, click through the login scenario, and then click on the button to load your songs into SoundCloud </li><li>
<li> Install the following on your Raspberry Pi device: 
<ul><li> python, gstreamer, soundcloud, mysql </li>
    <li> you might need to run the command "pip install requests[security]"</li>
	<li> you may also need to run the command "pip install soundcloud"</li></ul></li>
<li> Update all occurences of host, user, pass, your client id, your callback URL, and clientid to reflect the appropriate information </li>
<li> Run the Python script on the Pi and enjoy </li>
</ol>

<h2>To-Do list</h2>
<ul>
<li>Remove SoundCloud references in Python by adding url to database instead </li>
<li>Replace command line interface with a simple GUI </li>
<li>Display artwork on GUI </li>
<li>Consider the possibility of ditching the web server and hosting all content locally on Raspberry Pi</li>
<li>Implement some sort of remote system using and iPhone or Android</li>
<li>Allow two-way song movement (next and previous). Perhaps use a two-way linked list</li>
</ul>

<h2>Possible Remote Ideas</h2>
<ul>
<li>Bluetooth</li>
<li>IR</li>
<li>SSH</li>
<li>Port listening</li>
<li>Node.js or some other type of live server mechanism</li>
</ul>
