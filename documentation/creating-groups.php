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

<p>Including additional user-defined groups can greatly increase the number of systems MDN can be applied to, and it allows for analysis of specific parts of your system (as explained in Section 1.3).</p>

<p>GROMACS has a tool called make_ndx that can generate index files containing custom group definitions.</p>

<p>Note: MDN needs a valid index file for GROMACS jobs. If you decide to use your own network definition, make sure the index file also contains the standard GROMACS groups (System, Protein, etc).</p>

<p>Groups may be defined in terms of atom indices or node indices:</p>


<p latex="subsection"><b>Groups based on atom indices</b></p>

<p>When setting-up a network, MDN's default node mapping is one node for every residue. Each residue included in the chosen group becomes a node. This is done automatically, using the uploaded topology/PSF file. If you choose to use this node definition, then all that is left for you to do is to create the groups that will be used for network construction (Section 1.2) and analysis (Section 1.3).</p>

<p>Groups based on atom indices follow the standard GROMACS format. In the example shown below, "extragroup" contains 10 atoms. This type of group definition may be conveniently prepared with the GROMACS tool make_ndx. NAMD users may use VMD to obtain a list of relevant atom indices and insert them into a text file with extension .ndx. In this case, the automatically created index file should be deleted and the one prepared by the user should be uploaded to the server. NAMD users should also be advised that GROMACS atom indices start at 1, while NAMD indices start at 0. The atom index numbers used in the index file should be those in the PDB file (starting at one, not at zero).</p>

<p><img src="http://mdn.cheme.columbia.edu/images/extragroup.png" border=5></p>

<p latex="subsection"><b>Custom Node Definition/Groups based on node indices</b></p>

<p>Groups of atoms may also be defined in terms of network nodes. This is relevant only if custom node definitions are being employed.</p>

<p>If you do not wish to use the default node-per-residue network mapping, you need to include your own definition of the network nodes in the index file. Each node is defined as a separate group, as shown in the following example:</p>

<p><img src="http://mdn.cheme.columbia.edu/images/custom-nodes.png" border=5></p>

<p>The network definition shown above specifies four nodes, with 15 atoms constituting the first node. User-defined nodes are distinguished from other groups of atoms by using the label 'Node_#'. These should be in numerical order, starting with Node_0. NAMD users should be aware that, as with other groups of atoms defined in the index file, the atom index numbers should start at one, not at zero.</p>

<p>All custom nodes defined using this format will be included in a group called 'SPECIFIED_NODES'. You will be able to use your network definition during network setup (see Section 1.2 for further details):</p>

<p><img src="http://mdn.cheme.columbia.edu/images/specified_nodes.png" border=5></p>

<p>If you want to calculate coupling values between subgroups of the complete set of network nodes ('SPECIFIED_NODES'), you will need to add extra lines to your index file, specifying which nodes will be included in each subgroup:</p>  

<p><img src="http://mdn.cheme.columbia.edu/images/custom-groups.png" border=5 width=700></p>

<p>In the example shown above, two groups of atoms are defined. NodeGroup_0 has all atoms contained in nodes 0 to 99, and NodeGroup_1 containing atoms of nodes 100 to 183. The format NodeGroup_# should be observed when defining groups of atoms in this manner.</p>

<p>Once you have setup the network using the 'SPECIFIED_NODES' group, you will be able to use these subgroups to calculate partial coupling values in the Network Analysis step.</p>

<p><img src="http://mdn.cheme.columbia.edu/images/custom-groups-analysis.png" border=5></p>

</body>

</body>
</html>
