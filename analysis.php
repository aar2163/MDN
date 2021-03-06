<?php
 include 'mdn.php'
?>
<html>
<head>
<link rel="stylesheet" type="text/css" media="all" href="styles.css" />
<title>Centrality Analysis</title>
<script src="jquery.min.js"></script>

</head>
<body>



<?php

ob_start();



if(isset($_GET["ticket"]))
{
 $ticket = $_GET["ticket"];

 $data = get_data($ticket);

 $dir = $data['base_dir'];

 if(!isset($data['ticket']))
 {
  echo "<p>Invalid ticket</p>";
 }
 else
 {
  do_header($ticket);


  system("rm -f $dir/\#*");

  $index = file_get_contents("$dir/$ticket-index");
  $index = preg_replace('/\s+/', '', $index);

  if(!file_exists("$dir/$index"))
  {
   #$cmd = "echo q|$bin/make_ndx -f $dir/$input -o $dir/index.ndx";
   #exec($cmd,$out,$err);
   echo "Error: File $index not found\n";
  }
  else
  {
   echo "<p><h1>Network Analysis</h1></p>\n";


   $group1 = $_GET["group1"];
   $group2 = $_GET["group2"];
   $reset = $_GET["reset"];

   $output       = "$dir/$ticket-centrality.csv";
   $output_atoms = "$dir/$ticket-centrality_atoms.csv";
   $effic        = "$dir/$ticket-effic.dat";
   $zip          = "$dir/$ticket-output.zip";
   $wpath        = "$dir/$ticket-wpath.npy";
   $adj          = "$dir/$ticket-adj.npy";
   $enerd        = "$dir/$ticket-enerd.npy";
   $netindex     = "$dir/$ticket-netindex.ndx";
   $wpath_dat    = "$dir/$ticket-wpath.dat";
   $adj_dat      = "$dir/$ticket-adj.dat";
   $dist_dat     = "$dir/$ticket-dist.dat";


   $success = $data['network']['success'];

   if(!$success)
   {
    echo '<p><h2>There is no network available for analysis.</h2></p>';
    echo '<p><h2><a href="main.php?ticket='.$ticket.'">Go back to main menu.</a></h2></p>';
    exit();
   }


   //$nnodes = trim(`/usr/bin/python get_nnodes.py $ticket`);
   $nnodes = count($data['network']['nodes']['names']);


   if(isset($reset) and $reset == "yes")
   {
    unlink($output);
    unlink($output_atoms);
    unlink($zip);
    unset($data['output_files']);

    update_data($ticket,$data);

    echo '<p><h3>Output reset. <a href="analysis.php?ticket='.$ticket.'">Perform new analysis</a></h3></p>';
   }
   elseif(isset($group1) and isset($group2))
   {
    if(!isset($data['output_files']))
    {
     system("/usr/bin/python netwpath.py $ticket $wpath $group1 $group2");
     system("/usr/bin/python centrality.py $ticket $adj $wpath $enerd $enerd $adj_dat $wpath_dat $dist_dat");
     $cmd = "/var/www/html/centrality $nnodes $adj_dat $wpath_dat $dist_dat $dist_dat $output $effic; echo $?";
     exec($cmd,$out,$err);
     $count = count($out);
     $valid = ($out[count($out)-1] == 0);
     if($valid)
     {
     }
     system("/usr/bin/python centrality_atoms.py $ticket $output $output_atoms $enerd");
     system("/usr/bin/python coupling.py $ticket $effic");
     system("/usr/bin/python output.py $ticket $zip");
    }
    else
    {
     echo '<p><h2>Output already exists. <a href="analysis.php?ticket='.$ticket.'&reset=yes">Click here to reset</a></h2></p>';
    }
    echo '<p><a href="uploads/'.$ticket.'/'.$ticket.'-output.zip">Download Output</a></p>';
    echo '<p><a href="documentation/output.html">Output Format and Visualization Instructions</a></p>';
   }
   else   
   {
    echo '<p>Check out a brief <a href="documentation/network-analysis.html">explanation of node betweenness, and network coupling</a></p>';

    echo "<p><h2>You must choose two groups of nodes for pathway determination:</h2>\n";
    echo '<h2>Why? <a href="documentation/pathways.html">Click here</a></h2></p>';
    $cmd = "python centrality_info.py $ticket; echo $?";
    exec($cmd,$out,$err);
    $count = count($out);
   
    echo '<form action="analysis.php" method="get">';
    echo '<input type="hidden" name="ticket" value="'.$ticket.'">'."\n\n";

    for($ii=0;$ii<$count-1;$ii++)
    {
     $v[$ii] = split(' ',$out[$ii]);
    }


    echo '<div id="groups">
         <div id="group_index" class="group">
         	<h2>Index</h2>
         	<ul>'."\n";
                   for($ii=0;$ii<$count-1;$ii++)
                   {
                    if($v[$ii][2] == "True")
                    {
         		echo '<li><span class="tip"><span>'. $v[$ii][0] .'</span></li>'."\n";
                    }
                   }
    echo '      </ul>
         </div>

         <div id="group_group" class="group">
         	<h2>Group</h2>
         	<ul>'."\n";
                   for($ii=0;$ii<$count-1;$ii++)
                   {
                    if($v[$ii][2] == "True")
                    {
         		echo '<li><span class="tip"><span>'. $v[$ii][1] .'</span></li>'."\n";
         		#echo '<li><span class="tip"><span>'. $out[$ii] .'</span></li>';
                    }
                   }

    echo '      </ul>
         </div>

         <div id="group_s1" class="group">
         	<h2>Group</h2>
         	<ul>'."\n";
                   for($ii=0;$ii<$count-1;$ii++)
                   {
                    if($v[$ii][2] == "True")
                    {
         		echo '<li><span class="tip"><input type="checkbox" class="lCheckBox" name="group1" value="'.$ii.'"></span></li>'."\n";
         		#echo '<li><span class="tip"><span>'. $out[$ii] .'</span></li>';
                    }
                   }
    echo '      </ul>
         </div>

         <div id="group_s2" class="group">
         	<h2>Group</h2>
         	<ul>'."\n";
                   for($ii=0;$ii<$count-1;$ii++)
                   {
                    if($v[$ii][2] == "True")
                    {
         		echo '<li><span class="tip"><input type="checkbox" class="lCheckBox" name="group2" value="'.$ii.'"></span></li>'."\n";
         		#echo '<li><span class="tip"><span>'. $out[$ii] .'</span></li>';
                    }
                   }
    echo '      </ul>
         </div>
    ';

    echo '</div><div style="clear: both"></div>'."\n";
    echo '<p><h3>If you are not pleased with the current groups, <a href="files.php?ticket='.$ticket.'">upload another index file (.ndx)</a></h2></p>';


    echo '<p><input type="submit" value="Run Analysis"></p>';
   }

  }
 }
}



?>

</body>
</html>
