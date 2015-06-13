<?php
 include "mdn.php";
 $title = "Choosing Groups";
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


<p><b>The list of nodes for network construction and analysis is determined by selecting groups from an index file.</b></p>

<?php
 if($is_namd)
 {
  echo "<p><b>NAMD users: please be aware that MDN uses GROMACS index files (.ndx) to define groups of atoms, using the following format:</b></p>\n";
 }
 else
 {
  echo "<p>A GROMACS index file (.ndx) defines groups of atoms, using the following format:\n";
 }
?>


<p><img src="http://mdn.cheme.columbia.edu/images/groups.png" border=5></p>

<p>In the above example there is a total of 50000 atoms, with a protein group having 1001 atoms and a solvent group containing 48999 atoms. Please note that an actual index file would list all atoms belonging to each group.
<?php
 if($is_namd)
 {
  echo "<b>Please also note that GROMACS atom indices start at 1, while NAMD indices start at 0.</b></p>\n";
  echo "<p>Once you upload your coordinates file, MDN will automatically use the GROMACS tool make_ndx to create the corresponding index file. For NAMD jobs, only one group is strictly necessary: the one listing all atoms that will be included in the network. If you are not pleased with the automatically generated groups, you can delete the index file and upload your own version. You can prepare your own index file manually, following the format shown above. Alternatively, you can also use make_ndx to do this task (all that is needed is the PDB file, and a GROMACS installation).</p>";
 }
 else
 {
  echo '</p><p>GROMACS has a tool called make_ndx that can generate index files containing custom group definitions. As seen in <a href="network-construction.html">Section 4</a>, including additional user-defined groups can greatly increase the number of systems this tool can be applied to.</p>';
 }
?>


<p>MDN reads the information contained in the index file to let you choose which groups will be used for network construction and analysis.</p>

<p latex="subsection"><b>Network Construction</b></p>

<p>Network construction involves splitting a group of atoms into network nodes. This is done at the residue level, so information contained in the <?php if ($is_namd) { echo "PSF"; } else { echo "topology"; } ?> file will also be used. A group of atoms will be allowed for network construction if it does not contain partial residues. In other words, the group has to either contain all atoms of a residue (as specified in the topology), or none of those atoms. However, you can overcome this constraint if you generate and upload an index file with your own node definitions. Instructions for this can be found in <a href="custom-nodes.php?ticket=<?php echo $ticket;?>&software=<?php echo $software;?>">Section 4</a></p>


<p latex="subsection"><b>Network Analysis: Pathway Selection</b></p>

<p>The analysis performed by MDN is based on the calculation of internode shortest paths. These are usually calculated for all pairs of nodes, but you may also choose to calculate the shortest paths between specific nodes. The index file is also used for pathway selection. The group that was chosen for network construction, as well as any of its subsets will be allowed for pathway selection. MDN will then calculate the shortest paths between the corresponding nodes.

<p latex="subsection"><b>Network Analysis: Output</b></p>

<p>MDN performs network coupling analysis and reports the results in the final output file. This analysis is done for the entire network, and also for any subsets of the network specified in the index file</p>

<p><b>In summary, the groups listed in the index file are essential for MDN analysis. Take some time to think about which groups should be included in your index file.</p>
</body>
</html>
