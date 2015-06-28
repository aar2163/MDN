<?php
 include "mdn.php";
 $title = "Atom Groups";
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


<p>As seen in Sections 1.2 and 1.3, MDN uses GROMACS index files to define groups of atoms to be used for network setup and analysis. GROMACS users are required to upload their own index file, while one is automatically generated for NAMD users.</p>

<p>A GROMACS index file (.ndx) defines groups of atoms, using the following format:</p>


<p><img src="http://mdn.cheme.columbia.edu/images/groups.png" border=5></p>

<p>In the above example there is a total of 50000 atoms, with a protein group having 1001 atoms and a solvent group containing 48999 atoms. Please note that an actual index file would list all atoms belonging to each group.

<?php
 if($is_namd)
 {
  echo "<b>Please also note that GROMACS atom indices start at 1, while NAMD indices start at 0.</b></p>\n";
  echo "<p>Once you upload your coordinates file, MDN will automatically use the GROMACS tool make_ndx to create the corresponding index file. For NAMD jobs, only one group is strictly necessary: the one listing all atoms that will be included in the network. If you are not pleased with the automatically generated groups, you can delete the index file and upload your own version. You can prepare your own index file manually, following the format shown above. Alternatively, you can also use make_ndx to do this task (all that is needed is the PDB file, and a GROMACS installation).</p>";
 }
?>


<p>MDN reads the information contained in the index file to let you choose which groups will be used for network construction and analysis.</p>

</body>
</html>
