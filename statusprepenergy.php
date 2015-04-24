<?php
 include 'mdn.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Status of Network Setup</title>
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

 if(!check_ticket($ticket,$data))
 {
  echo "<p>Invalid ticket.</p>";
 }
 elseif(isset($_GET["show_error"]))
 {
  do_header($ticket);
  $id = $_GET["show_error"];
  $step = 'step'."$id";
  $out = $data['network'][$step]['output'];
  $count = count($out);
  echo $step;
  for($ii=0;$ii<$count;$ii++)
  {
   echo "$out[$ii]<br>\n";
  }
 }
 else
 {
  do_header($ticket);

  $dir = $data['base_dir'];


  /*$step_d[0] = "Creating Index";
  $step_d[1] = "Creating Energy Groups";
  $step_d[2] = "Creating TPR File";
  $step_d[3] = "Calculating Energies";
  $step_d[4] = "Extracting Energies";
  $step_d[5] = "Creating Energy Matrix";
  $step_d[6] = "Creating Adjacency Matrix";*/

  $list = $data['network']['steps_nr'];

  $count = count($list);


   echo '<div id="statuss">
	<div id="status_step" class="status">
		<h2>Index</h2>
		<ul>';
                  foreach ($list as $item)
                  {
			echo '<li><span class="tip"><span>'. $data['network'][$item]['title'] .'</span></li>';
                  }
  echo '      </ul>
        </div>

        <div id="status_status" class="status">
		<h2>Group</h2>
		<ul>';
                  $bOK = True;
                  for($ii=0;$ii<$count;$ii++)
                  {
                        $key = "step$ii";
                        $success = $data['network'][$key]['success'];
                        $running = $data['network'][$key]['running'];
                        $done    = $data['network'][$key]['done'];
                        if ($done  and $success)
                        {
                          echo '<li><span class="tip"><img width="12px" src="images/oktick.png"></span></li>';
                        }
                        elseif ($done and !$success)
                        {
                         $error_url = "statusprepenergy.php?ticket=$ticket&show_error=$ii";
                         if($bOK)
                         {
                          echo '<li><span class="tip"><a href="'. $error_url .'">Failed</a></span></li>';
                         }
                         else
                         {
                          echo '<li><span class="tip"><img width="10px" src="images/error_x.png"></span></li>';
                         }
                         $bOK = False;
                        }
                        else
                        {
                         $bOK = False;
                         if($running)
                         {
                          echo '<li><span class="tip"><img width="12px" src="images/run.jpg"></span></li>';
                         }
                         else
                         {
                          echo '<li><span class="tip"><img width="12px" src="images/waiting.png"></span></li>';
                         }
                        }
                  }
  echo '      </ul>
        </div>';
  $type = $_GET["type"];
  $ticket = $_GET["ticket"];
  $delete = $_GET["delete"];

  if($bOK == True)
  {
   echo "<p><b>Successfully constructed network</b></p>\n";

   $top = file_get_contents("$dir/$ticket-topol");
   $top = preg_replace('/\s+/', '', $top);

   $out = $data['network']['step6']['output'];
   for($ii=0;$ii<count($out)-1;$ii++)
   {
    $s = $out[$ii];
    echo "<p><b>$s</b></p>\n";
   }

  }

 }
?>

<script src="filedrag.js"></script>
</body>
</html>
