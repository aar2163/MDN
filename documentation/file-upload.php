<?php
 include "mdn.php";
 $title = "File Upload";
?>

<html>
<head>
<title>Documentation - <?php echo $title;?></title>


<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script>
$(document).ready(function(){

$("latex").hide();

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

<p>In order to use MDN, you need to upload a number of files. <b>MDN currently supports analysis of GROMACS and NAMD simulations.</b></p>



<p class="gromacs_header" latex="subsection"><img src="http://mdn.cheme.columbia.edu/images/next-icon.png" width=12 latex="hide"><b>GROMACS</b></p>

<p class="gromacs">The basic files that need to be uploaded are listed in the following Table:</p>

   <div id="groups" class="gromacs">
    <div class="menu_network">
      <ul><b>File Type</b>
       <li><span class="tip"><span>Coordinates File</span></li>
       <li><span class="tip"><span>Topology File</span></li>
       <li><span class="tip"><span>MDP Parameter File</span></li>
       <li><span class="tip"><span>Trajectory File</span></li>
       <li><span class="tip"><span>Index File</span></li>
      </ul>
    </div>
    <div class="menu_network">
      <ul><b>Possible Extensions</b>
       <li><span class="tip"><span>.gro</span></li>
       <li><span class="tip"><span>.top</span></li>
       <li><span class="tip"><span>.mdp</span></li>
       <li><span class="tip"><span>.xtc, .trr, .pdb, .gro</span></li>
       <li><span class="tip"><span>.ndx</span></li>
      </ul>
    </div>
    <div class="menu_network">
      <ul><b>Maximum Size</b>
       <li><span class="tip"><span>10MB</span></li>
       <li><span class="tip"><span>1MB</span></li>
       <li><span class="tip"><span>1MB</span></li>
       <li><span class="tip"><span><?php echo $mdn_max_upload;?></span></li>
       <li><span class="tip"><span>1MB</span></li>
      </ul>
    </div>
   </div>

<div style="clear: both;"></div>

<p class="gromacs"><b>The maximum file size allowed is 100 MB.</b> Most trajectories are a lot bigger than this, but one can significantly reduce their size by: (1) reducing the number of configurations sampled, and (2) removing all solvent molecules (which are not needed for the network analysis). Please see <a href="file-size.php?ticket=<?php echo "$ticket";?>&software=gromacs">Appendix A</a> for instructions on how to modify your simulation files to remove frames and remove the solvent.</p>


<p class="gromacs"><b>The index file is especially important</b>, since it is used to define the nodes and groups of nodes for the analysis performed by MDN. Please refer to <a href="choosing-groups.php">Section 2</a> for additional details.</p>

<p class="gromacs">To start uploading your files, go to the Main Menu and click on Upload Files. You will see something similar to:</p>

<p class="gromacs"><img src="http://mdn.cheme.columbia.edu/images/file-upload-start.png" border=5></p>

<p class="gromacs">Upload the necessary files. Note that once you upload the topology file, MDN will read its contents and ask for any auxiliary files (.itp) listed in your topology. At this point, you will see something like:</p>

<p class="gromacs"><img src="http://mdn.cheme.columbia.edu/images/file-upload-top.png" border=5></p>

<p class="gromacs">In this example no additional files need to be uploaded, as the auxiliary itp files could be found in the default gromacs installation. If you have itp files for molecules specific to your system, like different protein chains or a ligand, MDN will ask for them.

<p class="gromacs">Once the upload has been completed, you will see a summary of the files. A typical example might look like:</p> 

<p class="gromacs"><img src="http://mdn.cheme.columbia.edu/images/file-upload-last.png" border=5></p>

<p class="namd_header" latex="subsection"><img src="http://mdn.cheme.columbia.edu/images/next-icon.png" width=12 latex="hide"><b>NAMD</b></p>

<p class="namd">The basic files that need to be uploaded are listed in the following Table:</p>


   <div id="groups" class="namd">
    <div class="menu_network">
      <ul><b>File Type</b>
       <li><span class="tip"><span>Coordinates File</span></li>
       <li><span class="tip"><span>Structure File</span></li>
       <li><span class="tip"><span>Configuration File</span></li>
       <li><span class="tip"><span>Parameters File</span></li>
       <li><span class="tip"><span>Trajectory File</span></li>
      </ul>
    </div>
    <div class="menu_network">
      <ul><b>Possible Extensions</b>
       <li><span class="tip"><span>.pdb</span></li>
       <li><span class="tip"><span>.psf</span></li>
       <li><span class="tip"><span>.conf</span></li>
       <li><span class="tip"><span>.par, .inp</span></li>
       <li><span class="tip"><span>.dcd</span></li>
      </ul>
    </div>
    <div class="menu_network">
      <ul><b>Maximum Size</b>
       <li><span class="tip"><span>10MB</span></li>
       <li><span class="tip"><span>10MB</span></li>
       <li><span class="tip"><span>1MB</span></li>
       <li><span class="tip"><span>1MB</span></li>
       <li><span class="tip"><span><?php echo $mdn_max_upload;?></span></li>
      </ul>
    </div>
   </div>

<div style="clear: both;"></div>

<p class="namd"><b>The maximum file size allowed is 100 MB.</b> Most trajectories are a lot bigger than this, but one can significantly reduce their size by: (1) reducing the number of configurations sampled, and (2) removing all solvent molecules (which are not needed for the network analysis). Please see <a href="file-size.php?ticket=<?php echo "$ticket";?>&software=namd">Appendix A</a> for instructions on how to modify your simulation files to remove frames and remove the solvent.</p>

<p class="namd">To start uploading your files, go to the Main Menu and click on Upload Files. You will see something similar to:</p>

<p class="namd"><img src="http://mdn.cheme.columbia.edu/images/namd-file-upload-start.png" border=5></p>

<p class="namd">Upload the necessary files. Note that once you upload the coordinates file, MDN will use the GROMACS tool <a href="http://www.gromacs.org/Documentation/Gromacs_Utilities/make_ndx">make_ndx</a> to create the Groups file by defining groups of atoms, such as all protein atoms. At this point, you will see something like:</p>

<p class="namd"><img src="http://mdn.cheme.columbia.edu/images/namd-file-upload-coord.png" border=5></p>

<p class="namd">This Groups file, with extension .ndx, is created automatically, and is in the format of a GROMACS index file. This is a very important file, since it defines which atoms will be used to define the network nodes. You may also choose to delete this file, and upload your own version, if you want to use your own definition of network nodes (as opposed to the default definition of one node for each residue). Please refer to <a href="choosing-groups.php?software=namd">Section 2</a> for details.

<p class="namd">Note: <b> please make sure that the box dimensions and center, specified in the .conf file, are those corresponding to the initial configuration provided in the coordinates file. A mismatch between these will cause a fatal error.</b></p>

<p class="namd">Once the upload has been completed, you will see a summary of the files. A typical example might look like:</p> 

<p class="namd"><img src="http://mdn.cheme.columbia.edu/images/namd-file-upload-last.png" border=5></p>
</body>
</html>
