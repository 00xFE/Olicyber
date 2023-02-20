<?php
	if(isset($_GET['richiesta'])) {
	  if (preg_match("/.*/i", $_GET['richiesta'], $match))  {
	    echo "No, mi dispiace non posso fare questo!";
		} else {
			echo "flag{TROVAMI}";
		}
	} else {
 	  echo "Fai una richiesta e provero a realizzarla";
	}
?>