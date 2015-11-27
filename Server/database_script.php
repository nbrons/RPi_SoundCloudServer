<?php
//PHP Script that loads song list from soundcloud into database 
$con = mysql_connect("<host>","<user>","<pass>") or die('Could not connect: ' . mysql_error());		//sets up the database
mysql_select_db("songs", $con);

$jsondata = $_POST['songs'];		//gets JSON data
$data = json_decode($jsondata, true);

foreach($data as $item) {			//loops through track list
	$trackid = $item['id'];			//gets each item by their ID
	$sql = "SELECT * FROM songs WHERE trackid = '$trackid'";	//makes a call to the database, to see if the song is already in the database
	$result = mysql_query($sql,$con);
	
	if($item['streamable'] && mysql_num_rows($result) == 0){		//if the streaming is permitted and exists
	$title = $item['title'];										//loads data into variables
	$artwork_url = $item['artwork_url'];
	$duration = $item['duration'];
	
	$sql = "INSERT INTO songs(id, trackid, title, artwork_url, duration) VALUES(NULL, '$trackid', '$title', '$artwork_url', '$duration')";		//inserts the song into the database

	if(!mysql_query($sql,$con))
	{
		die('Error : ' . mysql_error());
	}
	}
}

?>