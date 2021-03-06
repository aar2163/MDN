<?php
 include "mdn.php";
 $title = "Custom Nodes";
?>
<html>
<head>
<title><?php echo $title;?></title>
</head>
<body>

<?php

 $ticket = $_GET["ticket"];

 $data = get_data($ticket);
 

 if(!isset($data['ticket']))
 {
  $ticket = 'INVALID';
 }

 if($_GET['software'] == 'namd')
 {
  $is_namd = True;
 }

 $software = get_software($data,$_GET);

 do_header($ticket);
?>


<p><h1><?php echo $title;?></h1></p>

<p>MDN uses a <a href="choosing-groups.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">GROMACS index file</a> to let you choose which atoms will be used to construct and analyze the network.</p>

<p>The default node mapping is done at the residue level. Each residue included in the chosen group becomes a node. This is done using the uploaded topology or PSF file.</p>

<p>This approach results in each network node representing one residue. If you do not wish to use this type of network definition, you need to upload your own definition of the network nodes. This should also use GROMACS index file format:</p>

<p><img src="http://mdn.cheme.columbia.edu/images/custom-nodes.png" border=5></p>

<p>The network definition shown above specifies four nodes, with 15 atoms constituting the first node. <b>Custom nodes should be defined using the label Node_#</b> and they should be in numerical order, starting with Node_0.</p>

<?php
 if($is_namd)
 {
  echo "<p>Please remember that GROMACS atom indices start at 1. Please also note that this is the only information required for NAMD jobs. Feel free to delete the automatically generated .ndx file and upload your own network definition, following the format shown above.</p>\n";
 }
 else
 {
  echo "<p>Please note that MDN needs a valid index file for GROMACS jobs. If you decide to use your own network definition, make sure the index file also contains the standard GROMACS groups (System, Protein, etc).</p>\n";
 }
?>

<p>All custom nodes defined using this format will be included in a group called 'SPECIFIED_NODES'. Once you finish uploading your files, you will be able to use your custom network definition during network setup (see <a href="network-construction.html">Section 5</a> for further details):</p>

<p><img src="http://mdn.cheme.columbia.edu/images/specified_nodes.png" border=5></p>

<p latex="subsection"><b>Custom Groups</b></p>

<p>You may also define groups of atoms based on the custom node definitions (see <a href="creating-groups.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">Section 3</a>).</p>


</body>
</html>
