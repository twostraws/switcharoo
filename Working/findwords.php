<?php
	$words = file("words");
	
	$counted = array();
	
	foreach($words as $word) {
		for ($i = 0; $i < strlen($word); ++$i) {
			$letter = $word{$i};
			if ($letter == "\n") continue;
			
			$current_word = trim($word);
			$current_word[$i] = "?";
			
			if (isset($counted[$current_word])) {
				$counted[$current_word]++;
			} else {
				$counted[$current_word] = 1;
			}
		}
	}
	
	asort($counted);
	var_dump($counted);