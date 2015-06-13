<?php
 include "mdn.php";
 $title = "Creating Custom Groups";
?>
<html>
<head>
<title>Documentation - <?php echo $title;?></title>
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

<p>As seen in <a href="choosing-groups.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">Section 2</a>, MDN uses GROMACS index files to define groups of atoms to be used for network analysis. GROMACS users are required to upload their own index file, while one is automatically generated for NAMD users. It must be noted that it is frequently interesting to create custom groups, allowing for analysis of specific parts of your system. These groups may be defined in terms of atom indices or node indices. The latter option is relevant only if custom node definitions are being employed (see <a href="custom-nodes.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">Section 4</a>).</p>

<p latex="subsection"><b>Groups based on atom indices</b></p>

<p>Groups based on atom indices follow the standard GROMACS format. In the example shown below, "extragroup" contains 10 atoms. This type of group definition may be conveniently prepared with the GROMACS tool make_ndx. NAMD users may use VMD to obtain a list of relevant atom indices and insert them into a .ndx file. In this case, the automatically created index file should be deleted and the one prepared by the user should be uploaded to the server. NAMD users should also be advised that GROMACS atom indices start at 1, while NAMD indices start at 0.</p>

<p><img src="http://mdn.cheme.columbia.edu/images/extragroup.png" border=5></p>

<p latex="subsection"><b>Groups based on node indices</b></p>

<p>Groups of atoms may also be defined in terms of network nodes. This is relevant only if custom node definitions are being employed (see <a href="custom-nodes.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">Section 4</a>).</p>

<p><img src="http://mdn.cheme.columbia.edu/images/custom-groups.png" border=5 width=700></p>

<p>In the example shown above, two groups of atoms are defined. NodeGroup_0 has all atoms contained in nodes 0 to 99, and NodeGroup_1 containing atoms of nodes 100 to 183. The format NodeGroup_i should be observed when defining groups of atoms in this manner.</p>

</body>
</html>
