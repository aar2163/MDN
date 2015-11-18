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

<script type="text/javascript">
function recp(id) {
  $('#myStyle').load('data.php?id=' + id);
}
</script>

<!--
<div id='myStyle'>
</div>
-->

<?php
 $ticket = $_GET["ticket"];

 $data = get_data($ticket);
 $dir = $data['base_dir'];
 

 if(!isset($data['ticket']))
 {
  echo "<p>Invalid ticket.</p>";
 }
 else
 {
  do_header($ticket);

  echo '<p><b>Job name: '.$data['jobname'].'</b></p>'."\n";


  $step_d[0] = "Upload Files";
  $step_d[1] = "Create Network";
  $step_d[2] = "Network Overview";
  $step_d[3] = "Network Analysis";

  $link[0] = "files.php?ticket=$ticket";
  $link[1] = "setnetwork.php?ticket=$ticket";
  $link[2] = "overview.php?ticket=$ticket";
  $link[3] = "analysis.php?ticket=$ticket";

  $condition[0] = $data['network']['available'];
  $condition[1] = $data['network']['success'];
  $condition[2] = $data['network']['success'];
  $condition[3] = isset($data['output_files']);

  $count = count($step_d);

   #echo '<div id="big">'."\n";
   echo '<div id="statuss">
	<div id="status_step" class="status">
		<h2>Index</h2>
		<ul>';
                  for($ii=0;$ii<$count;$ii++)
                  {
			echo '<li><span class="bigtip"><span><h3><a href="'.$link[$ii].'">'. $step_d[$ii] .'</a></h3></span></li>';
                  }
  echo '      </ul>
        </div>

        <div id="status_status" class="status">
		<h2>Group</h2>
		<ul>';
                  $bOK = True;
                  for($ii=0;$ii<$count;$ii++)
                  {
                        if ($condition[$ii])
                        {
                         echo '<li><span class="bigtip"><img src="images/oktick.png"></span></li>';
                        }
                        else
                        {
                         echo '<li><span class="bigtip"><img src="images/pending.png"></span></li>';
                        }
                  }
  echo '      </ul>
        </div></div>';
  $type = $_GET["type"];
  $ticket = $_GET["ticket"];
  $delete = $_GET["delete"];
  echo '<div style="clear: both;"></div>';
  echo '<p><b>Please cite this work as:</b><br>Ribeiro, A.A.S.T., Ortiz V. Journal of Chemical Theory and Computation 10, 1762-1769 (2015)';

 }
?>

<script src="filedrag.js"></script>
</body>
</html>
