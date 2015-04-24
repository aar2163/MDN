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

$ip = $_SERVER['REMOTE_ADDR'];

if($ip == "128.59.144.35")
{
 $mongo = new MongoClient();
 $db = $mongo->selectDB("MDN");
 $col = $db->jobs;
 $query = array();
 $fields = array('ticket' => 1,'user_name' => 1,'user_email' => 1,'jobname' => 1);
 $cursor = $col->find($query,$fields);
 echo '<div id="status">
       <div id="status_step" class="status">
	<h2>Index</h2>
	<ul>';
        foreach ($cursor as $data)
        {
          $t = $data['ticket'];
          echo '<li><span class="tip"><span><a href="main.php?ticket='. $t .'">'.$t.'</a></span></li>';
        }
 echo ' </ul>
       </div>

       <div id="status_status" class="status">
	<h2>Group</h2>
        <ul>';
        foreach ($cursor as $data)
        {
          echo '<li><span class="tip"><span>'. $data['user_name'] .'</span></li>';
        }
 echo ' </ul>
       </div>

       <div id="status_status" class="status">
	<h2>Group</h2>
        <ul>';
        foreach ($cursor as $data)
        {
          echo '<li><span class="tip"><span>'. $data['user_email'] .'</span></li>';
        }
 echo ' </ul>
       </div>

       <div id="status_status" class="status">
	<h2>Group</h2>
        <ul>';
        foreach ($cursor as $data)
        {
          if(!isset($data['jobname']) or $data['jobname'] == "")
          {
           $data['jobname'] = "null";
          }
          echo '<li><span class="tip"><span>'. $data['jobname'] .'</span></li>';
        }
}
else
{
 echo "Invalid Request";
}



exit();


?>

</body>
</html>
