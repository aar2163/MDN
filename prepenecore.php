<?php
 include 'mdn.php';
?>

<html>
<body>


<?php
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/

function make_steps($data)
{
 $ticket = $data['ticket'];
 $dir = $data['base_dir'];
 $bin = $data['software']['binpath'];
 $software = $data['software']['name'];

 $netindex = $data['network']['chosen_group'];

 $coord  = $data['files']['coordinates']['fname'];
 $top  = $data['files']['topology']['fname'];
 $traj  = $data['files']['trajectory']['fname'];
 $index = $data['files']['index']['fname'];
 $specified_nodes = $data['index']['specified_nodes'];
 $econf = $data['files']['energy_conf'];
 $emdp = $data['files']['energy_mdp'];

 $step_cmd['namd']['step0'] = "/bin/bash splitres.sh $ticket $dir $coord $index $netindex 2>&1; echo $?";
 $step_cmd['namd']['step1'] = "/usr/bin/python nodes.py $ticket $dir/$ticket-netindex.ndx 2>&1; echo $?";
 $step_cmd['namd']['step2'] = "/usr/bin/python make_conf.py $ticket 2>&1; echo $?";
 $step_cmd['namd']['step3'] = "cd $dir; $bin/namd2 $econf 2>&1; echo $?";
 $step_cmd['namd']['step4'] = "/usr/bin/python enerd.py $ticket; echo $?";
 $step_cmd['namd']['step5'] = "/usr/bin/python netadj.py $ticket $dir/$ticket-adj.npy; echo $?";

 $step_cmd['gromacs']['step0'] = "/bin/bash splitres.sh $ticket $dir $coord $index $netindex 2>&1; echo $?";
 $step_cmd['gromacs']['step1'] = "/usr/bin/python nodes.py $ticket $dir/$ticket-netindex.ndx 2>&1; echo $?";
 $step_cmd['gromacs']['step2'] = "cd $dir; $bin/grompp -f $emdp -c $coord -p $top -o $ticket-job.tpr -n $ticket-netindex.ndx -maxwarn 1 2>&1; echo $?";
 $step_cmd['gromacs']['step3'] = "cd $dir; $bin/mdrun -deffnm $ticket-job -rerun $traj -nt 4 2>&1; echo $?";
 $step_cmd['gromacs']['step4'] = "cd $dir; $bin/gmxdump -e $ticket-job.edr 1> $ticket-enematrix.dat; echo $?";
 $step_cmd['gromacs']['step5'] = "/usr/bin/python enerd.py $ticket; echo $?";
 $step_cmd['gromacs']['step6'] = "/usr/bin/python netadj.py $ticket $dir/$ticket-adj.npy; echo $?";

 $step_head['namd']['step0'] = "<p><b>Error creating index</b></p>\n";
 $step_head['namd']['step1'] = "<p><b>Error creating energy groups</b></p>\n";
 $step_head['namd']['step2'] = "<p><b>Error preparing configuration file</b></p>\n";
 $step_head['namd']['step3'] = "<p><b>Error calculating energies</b></p>\n";
 $step_head['namd']['step4'] = "<p><b>Error creating energy matrix</b></p>\n";
 $step_head['namd']['step5'] = "<p><b>Error creating adjacency matrix</b></p>\n";

 $step_head['gromacs']['step0'] = "<p><b>Error creating index</b></p>\n";
 $step_head['gromacs']['step1'] = "<p><b>Error creating energy groups</b></p>\n";
 $step_head['gromacs']['step2'] = "<p><b>Error creating tpr file</b></p>\n";
 $step_head['gromacs']['step3'] = "<p><b>Error calculating energies</b></p>\n";
 $step_head['gromacs']['step4'] = "<p><b>Error creating extracting energies</b></p>\n";
 $step_head['gromacs']['step5'] = "<p><b>Error creating energy matrix</b></p>\n";
 $step_head['gromacs']['step6'] = "<p><b>Error creating adjacency matrix</b></p>\n";

 $steps = array();

 $list = $data['network']['steps_nr'];

 foreach ($list as $item)
 {
  $steps[$item]['cmd']    = $step_cmd[$software][$item];
  $steps[$item]['header'] = $step_head[$software][$item];
 }

 if($specified_nodes)
 {
  $steps['step0']['cmd'] = "cp $dir/$index $dir/$ticket-netindex.ndx; echo $?";
 }

 #$steps['step1']['cmd'] = "/usr/bin/python nodes.py $ticket $dir/$ticket-netindex.ndx $dir/$mdp $dir/$ticket-md.mdp 2>&1; echo $?";

 return $steps;
}

function do_log($ticket,$step,$out,$header)
{

 $data = get_data($ticket);


 $count = count($out);
 $nerr = $out[$count-1];

 $key = "step$step";

 $nstep = $step+1;
 $nkey = "step$nstep";


 if($nerr == 0)
 {
  $data['network'][$key]['success'] = True;
 }
 else
 { 
  $data['network'][$key]['success'] = False;
  $data = clear_status($data);
  echo $data['network']['running'];
  update_data($ticket,$data);
  exit();
 }
 $data['network'][$key]['output'] = $out;
 $data['network'][$key]['done']     = True;
 $data['network'][$key]['running']  = False;

 $data['network'][$nkey]['running'] = True;

 unset($GLOBALS['out']);

 update_data($ticket,$data);

 $data = null;
}

function status_running($ticket,$chosen,$data)
{
 $data['network']['running'] = True;
 $data['network']['chosen_group'] = $chosen;

 if($data['software']['name'] == 'namd')
 {
  $list = ['step0','step1','step2','step3','step4','step5'];
 }
 if($data['software']['name'] == 'gromacs')
 {
  $list = ['step0','step1','step2','step3','step4','step5','step6'];
 }

 $data['network']['steps_nr'] = $list;

 $net = $data['network'];

 if($data['software']['name'] == 'namd')
 {
  $net['step0']['title'] = "Creating Index";
  $net['step1']['title'] = "Creating Energy Groups";
  $net['step2']['title'] = "Preparing Configuration File";
  $net['step3']['title'] = "Calculating Energies";
  $net['step4']['title'] = "Creating Energy Matrix";
  $net['step5']['title'] = "Creating Adjacency Matrix";
 }

 if($data['software']['name'] == 'gromacs')
 {
  $net['step0']['title'] = "Creating Index";
  $net['step1']['title'] = "Creating Energy Groups";
  $net['step2']['title'] = "Creating TPR File";
  $net['step3']['title'] = "Calculating Energies";
  $net['step4']['title'] = "Extracting Energies";
  $net['step5']['title'] = "Creating Energy Matrix";
  $net['step6']['title'] = "Creating Adjacency Matrix";
 }
 $data['network'] = $net;


 update_data($ticket,$data);

 return $data;

}

function clear_status($data)
{
 $data['network']['running'] = False;
 $data['network']['done'] = True;

 echo $data['network']['running'];

 $list = ['step0','step1','step2','step3','step4','step5'];

 $bOk = True;
 foreach ($list as $item)
 {
  if(!$bOk)
  {
   $data['network'][$item]['success'] = False;
   $data['network'][$item]['done'] = True;
   $data['network'][$item]['running'] = False;
  }
  if(!$data['network'][$item]['success'])
  {
   $bOk = False;
   $data['network'][$item]['done'] = True;
   $data['network'][$item]['running'] = False;
  }
 }
 $data['network']['success'] = $bOk;
 return $data;
}

function status_done($ticket)
{

 $data = get_data($ticket);

 $data = clear_status($data);


 update_data($ticket,$data);

 $data = null;
}



$ticket = $argv[1];
$netindex = $argv[2];


$data = get_data($ticket);
$dir = $data['base_dir'];







$data = status_running($ticket,$netindex,$data);


$steps = make_steps($data);


$list = $data['network']['steps_nr'];
$data = null;

for($ii=0;$ii<count($list);$ii++)
{
 $item = "step".$ii;
 print "$item\n";
 exec($steps[$item]['cmd'],$out,$err);
 do_log($ticket,$ii,$out,$steps[$item]['header']);
}

array_map('unlink', glob("$dir/$ticket-job.*"));

chmod("$dir/$ticket-enerd.npy",0664);
chmod("$dir/$ticket-adj.npy",0664);
chmod("$dir/$ticket-netindex.ndx",0664);

status_done($ticket);


?>

</body>
</html>
