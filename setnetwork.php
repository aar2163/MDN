<?php
 include 'mdn.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Network Setup</title>

<script src="jquery.min.js"></script>

<script>

// the selector will match all input controls of type :checkbox
// and attach a click event handler 
/*$(document).ready(function(){
    $("p").click(function(){
        $(this).hide();
    });
});*/

$(document).ready(function(){
 $("input:checkbox").click(function() {
  // in the handler, 'this' refers to the box clicked on
  var $box = $(this);
  
  if ($box.is(":checked")) {
    // the name of the box is retrieved using the .attr() method
    // as it is assumed and expected to be immutable
    var group = "input:checkbox[name='" + $box.attr("name") + "']";
    // the checked state of the group/box on the other hand will change
    // and the current value is retrieved using .prop() method
    $(group).prop("checked", false);
    $box.prop("checked", true);
  } else {
    $box.prop("checked", false);
  }
 });
});
</script>
</head>

<body>



<?php

ob_start();

$bin = "/home/andre/gromacs463/bin";


if(isset($_GET["ticket"]))
{
 $ticket = $_GET["ticket"];

 $data = get_data($ticket);
 $dir = $data['base_dir'];

 $available =  $data['network']['available'];

 if(!check_ticket($ticket,$data))
 {
  echo "<p>Invalid ticket</p>";
 }
 elseif($available)
 {
  do_header($ticket);


  system("rm -f $dir/\#*");


  echo '<p><h1>Network Setup</h1></p>';
  echo "<p><h2>You must select a group to construct the network:</h2></p>\n\n";
  echo '<h2>Why? <a href="documentation/network-construction.html">Click here</a></h2></p>';

  $cmd = "python groupinfo.py $ticket; echo $?";
  unset($out);
  exec($cmd,$out,$err);
  $count = count($out);

  for($ii=0;$ii<$count-1;$ii++)
  {
   $v[$ii] = split(' ',$out[$ii]);
  }

  echo '<form action="setnetwork.php" method="get">';
  echo '<input type="hidden" name="ticket" value="'.$ticket.'">'."\n\n";

  echo '<div id="groups_small">
	<div id="group_index" class="menu_network">
		<h2>Index</h2>
		<ul>'."\n";
                  for($ii=0;$ii<$count-1;$ii++)
                  {
                    if($v[$ii][2] == "True")
                    {
			echo '<li><span class="tip"><span>'.$v[$ii][0].'</span></li>'."\n";
                    }
                  }
  echo '      </ul>
        </div>

        <div id="group_group" class="menu_network">
		<h2>Group</h2>
		<ul>';
                  for($ii=0;$ii<$count-1;$ii++)
                  {
                    if($v[$ii][2] == "True")
                    {
			echo '<li><span class="tip"><span>'. $v[$ii][1] .'</span></li>'."\n";
                    }
                  }

  echo '      </ul>
         </div>

         <div id="group_s1" class="menu_network">
         	<h2>Group</h2>
         	<ul>'."\n";
                   for($ii=0;$ii<$count-1;$ii++)
                   {
                    if($v[$ii][2] == "True")
                    {
         		echo '<li><span class="tip"><input type="checkbox" class="radio" name="netindex" value="'.$ii.'"></span></li>'."\n";
                    }
                   }

  echo '      </ul>
      </div>
   ';
  echo '</div><div style="clear: both"></div>'."\n";
  echo '<p><h3>If you are not pleased with the current groups, <a href="files.php?ticket='.$ticket.'">upload another index file (.ndx)</a></h3></p>';

  echo '<p><input type="submit" value="Construct Network"></p>';

  $netindex = $_GET["netindex"];
  $reset = $_GET["reset"];

  $running =  $data['network']['running'];

  if(isset($reset) and $reset == "yes")
  {
   /* User cannot reset network if job is running */
   if(!$running)
   {
    /*Clean network info in the database */
    $data['network']['running'] = false;
    $data['network']['done'] = false;
    $data['network']['success'] = false;
    
    $steps = array('step0','step1','step2','step3','step4','step5','step6');

    foreach ($steps as $key)
    {
     $data['network'][$key]['running'] = false;
     $data['network'][$key]['done'] = false;
     $data['network'][$key]['success'] = false;
     $data['network'][$key]['output'] = '';
    }

    update_data($ticket,$data);

    unlink("$dir/$ticket-netout");

    echo '<p>Network reset.</p></div>';
   }
   else
   {
    echo '<p>Network construction is running. You have to wait before resetting.</p></div>';
   }
  }

  if(isset($netindex))
  {
    $done            =  $data['network']['done'];
    $specified_nodes =  $data['index']['specified_nodes'];

    if(!$running and !$done)
    {
     $valid = $data['index']['groups'][$netindex]['network_ok'];

     if($valid)
     {
      echo '<p>Preparing the network. <a href="statusprepenergy.php?ticket='.$ticket.'">Check the status</a></p></div>';
      #system("/usr/bin/php prepenecore.php $ticket $netindex > /dev/null &");
      $pwd = getcwd();
      $hostname = gethostname();
      $qsub = "qsub -vTICKET=$ticket,INDEX=$netindex $pwd/job-qsub";
      $cmd = "ssh www-torque@$hostname '$qsub'";
      exec($cmd,$out,$err);
     }
     else
     {
      echo '<p><b>Invalid group. Pick another one.</b></p></div>';
     }
    

    }
    elseif(!$done)
    {
     echo '<p>Network construction is running. <a href="statusprepenergy.php?ticket='.$ticket.'">Check the status</a></p></div>';
    }
    else
    {
     echo '<p>Network construction is done. <a href="statusprepenergy.php?ticket='.$ticket.'">Check the output</a></p>
           <p>You can also specify a new index by <a href="setnetwork.php?ticket='.$ticket.'&reset=yes">resetting the network</a></p>
</div>';
    }

   }
   else
   {
    echo "</div>";
   }
  }
  else
  {
   echo "<p>Network setup unavailable</p>\n";
  }
 
}



?>

</body>
</html>
