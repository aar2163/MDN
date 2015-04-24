<?php
include 'mdn.php';
?>


<?php
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/


 $email =  "aar2163@columbia.edu";
 $name = "Andre";

 $allow[0] = '/.edu$/';
 $allow[1] = '/.ac.uk$/';
 $allow[2] = '/(?<!(.com))(.br)$/';

 $nallow = count($allow);

 for($ii=0;$ii<$nallow;$ii++)
 {
  $match = preg_match($allow[$ii],$email,$matches);
  if($match != 0)
  {
   break;
  }
 }

 if($match == 0)
 {
  print "<p>Your email was not recognized as institutional. If that is not true, contact us at aar2163@columbia.edu</p>";
  exit;
 }

 #exit;
 $ticket = uniqid();



 $subject = 'MDN Ticket';
 $message = "Dear $name,\r\rYou have requested to use the MDN server.\r\rYour validation ticket is: $ticket\r\rPlease access the URL http://mdn.cheme.columbia.edu/validate.php?ticket=$ticket to validate your ticket.\r\rHappy simulating,\rMDN Crew";
 $headers = 'From: aar2163@columbia.edu' . "\r\n" .
    'Reply-To: aar2163@columbia.edu' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();

 $message = wordwrap($message, 100, "\r\n");

 mail($email, $subject, $message, $headers);

 echo "<p>An email has been sent to $email</p>";



?>

</body>
</html>
