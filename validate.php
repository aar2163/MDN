<?php
include 'mdn.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>MDN File Upload</title>
<link rel="stylesheet" type="text/css" media="all" href="styles.css" />
<script src="jquery.min.js">
</script>
<script>
$(document).ready(function(){
  $("button").click(function(){
    $("#div1").load("demo_test.txt");
  });
});
</script>
</head>
<body>

<?php
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/

echo "<link href=\"site.css\" media=\"all\" rel=\"stylesheet\" type=\"text/css\">";

echo '<header></header>';

if(isset($_GET["ticket"]))
{
 $ticket = $_GET["ticket"];

 $data = get_data($ticket);


 if(isset($data))
 {
  if($data['validated'])
  {
   echo '<p>This ticket has already been validated. <a href="main.php?ticket='.$ticket.'">Go to main menu</a></p>';
  }
  elseif(!isset($data['jobname']) and !isset($_GET['jobname']))
  {
   echo '<p><b>Choose a job name</b></p>'."\n";
   echo '<form action="validate.php" method="get">'."\n";
   echo '<input type="text" name="jobname">'."\n";
   echo '<input type="hidden" name="ticket" value="'.$ticket.'">'."\n";
   echo '<input type="submit">'."\n";
  }
  elseif(!isset($_GET['software']) and isset($_GET['jobname']))
  {
   echo '<p><b>Choose a simulation software</b></p>'."\n";
   echo '<form action="validate.php" method="get">'."\n";
   echo '<div><ul><li><img width=200 src="images/gromacs_logo.png"></li><li><input type="radio" name="software" value="gromacs"></li></ul>'."\n";
   if($data['user_email'] == 'aar2163@gmail.com')
   {
    echo '<ul><li><img width=200 src="images/namd_logo.jpg"></li><li><input type="radio" name="software" value="namd"></li></ul></div>'."\n";
   }
   echo '<br><input type="hidden" name="ticket" value="'.$ticket.'">'."\n";
   echo '<p><input type="submit"></p>'."\n";
   $data['jobname'] = $_GET['jobname'];
   update_data($ticket,$data);
  }
  elseif(isset($data['jobname']) and isset($_GET['software']))
  {
   $software = $_GET['software'];
   system("/usr/bin/python init-data.py $ticket $software");
   echo "<p>Ticket Validated</p><p><a href=\"main.php?ticket=$ticket\">Start building your network</a></p>";
  }
  else
  {
   echo "<p>Fatal error. Please generate a new ticket.</p>";
  }
 }
 else
 {
  echo "<p>Invalid ticket.</p>";
 }
}

?>

</body>
</html>
