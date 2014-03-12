<?php
	$letters = file("wordlist.txt");
	
	foreach($letters as $letter) {
		$letter = trim($letter);
		if (strlen($letter) == 4) echo "$letter\n";
	}
?>