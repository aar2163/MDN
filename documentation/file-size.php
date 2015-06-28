<?php
 include "mdn.php";
 $title = "File Size";
?>

<html>
<head>
<title>Documentation - <?php echo $title;?></title>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script>
$(document).ready(function(){
<?php
  if($_GET["software"] != "gromacs")
  {
    print '$("p.gromacs").hide();'."\n";
    print '$("div.gromacs").hide();'."\n";
  }
  if($_GET["software"] != "namd")
  {
    print '$("p.namd").hide();'."\n";
    print '$("div.namd").hide();'."\n";
  }
?>
    $("p.gromacs_header").click(function(){
        $("p.gromacs").toggle();
        $("div.gromacs").toggle();
    });
    $("p.namd_header").click(function(){
        $("p.namd").toggle();
        $("div.namd").toggle();
    });
});
</script>

</head>
<body>

<?php

 $ticket = $_GET["ticket"];

 $data = get_data($ticket);
 

 if(!isset($data['ticket']))
 {
  $ticket = 'INVALID';
 }

 do_header($ticket);
?>



<p><h1><?php echo $title;?></h1></p>

<p><b>The maximum file size allowed is <?php echo $mdn_max_upload;?>. Most trajectories are a lot bigger than this.</a></p></b></p>

<p>Computer simulations of biomolecules usually generate a lot of information about the systems under consideration. For these simulations to be useful, the description of the system's energy and forces must be carefully considered. One important factor that significantly affects the behavior of biomolecules is the presence of solvent molecules. These are usually explicitly included in the simulation box, and a significant fraction of the total data output is likely due to solvent molecules.</p>

<p>While including solvent molecules is extremely desirable when simulating most biomolecular systems, <b>the uploaded trajectory does not need to include them</b>. Network analysis is concerned with atoms/residues of solute molecules, such as ligands, proteins, and other types of biomolecules. Only in very special cases, you might want to include specific water molecules in your network, but these would need to be specified as a <a href="choosing-groups.php">separate group</a>.</p>

<p>Excluding water molecules from your trajectory thus significantly reduces the corresponding file size. It also makes network construction and analysis extremely faster. In addition, the number of frames can be adjusted so the trajectory is below the <?php echo $mdn_max_upload;?> limit.</p>


<p class="gromacs_header"><img latex="hide" src="http://mdn.cheme.columbia.edu/images/next-icon.png" width=12><b>GROMACS</b></p>

<p class="gromacs"><u>These tasks can be easily accomplished with the GROMACS tool trjconv.</u></p> 

<p class="gromacs"><b>Please note that all uploaded files must match the trajectory.</b><p>

<p class="gromacs"><b>Coordinates (.gro)</b>: Use trjconv to create an input file without solvent molecules</p>
<p class="gromacs"><b>Topology (.top)</b>: Use any text editor to delete water molecules from the topology.</p>

<p class="gromacs"><img src="http://mdn.cheme.columbia.edu/images/topology-sol.png" border=5></p>

<p class="gromacs">In this example you want to delete the line starting with SOL. You might also delete the sodium ions (NA), but you would need to change the other files accordingly. <u>Note that network construction is based on inter-residue interaction energies, so deleting both solvent molecules and ions does not have any influence on the results.</u></p>

<p class="gromacs"><b>Parameter File (.mdp)</b>: This file likely makes references to groups containing water molecules if you performed a constant temperature simulation. You will need to delete these. In fact, you can actually remove any parameters related to temperature/pressure control. The only parameters that matter are related to energy calculation, such as periodic boundary conditions and cutoffs.</p>

<p class="gromacs"><b>Index File (.ndx)</b>: Use make_ndx to generate an index file for your system. Use the modified .gro file as input.</p>

<p class="namd_header"><img latex="hide" src="http://mdn.cheme.columbia.edu/images/next-icon.png" width=12><b>NAMD</b></p>

<p class="namd"><u>These tasks can be easily accomplished with the NAMD tool catdcd.</u></p> 

<p class="namd"><code>catdcd -i index.dat -s coordinates.pdb -stype pdb -o traj_dry.dcd -otype dcd traj.dcd</code></p>

<p class="namd">You will need an index file (index.dat) containing the indices of non-solvent atoms. This can be done with the VMD Tk Console:</p>

<p class="namd"><img src="http://mdn.cheme.columbia.edu/images/notwater_script.png" border=5></p>

<p class="namd"><b>Please note that all uploaded files must match the trajectory.</b><p>

<p class="namd"><b>Coordinates (.pdb)</b>: Use VMD to create a PDB file without solvent molecules</p>
<p class="namd"><b>Structure (.psf)</b>: Use the psfgen tool in VMD to create a PSF file without solvent molecules.</p>

</body>
</html>
