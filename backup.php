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

 $list = ['step0','step1','step2','step3','step4','step5','step6'];

 $data['network']['steps_nr'] = $list;

 $net = $data['network'];
 $net['step0']['title'] = "Creating Index";
 $net['step1']['title'] = "Creating Energy Groups";
 $net['step2']['title'] = "Creating TPR File";
 $net['step3']['title'] = "Calculating Energies";
 $net['step4']['title'] = "Extracting Energies";
 $net['step5']['title'] = "Creating Energy Matrix";
 $net['step6']['title'] = "Creating Adjacency Matrix";
 $data['network'] = $net;

 update_data($ticket,$data);
 $data = null;
}

function clear_status($data)
{
 $data['network']['running'] = False;
 $data['network']['done'] = True;

 echo $data['network']['running'];

 $list = ['step0','step1','step2','step3','step4','step5','step6'];

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


$bin = "/home/andre/gromacs463/bin";

$ticket = $argv[1];
$netindex = $argv[2];


$data = get_data($ticket);
$dir = $data['base_dir'];


$top   = $data['files']['topology']['fname'];
$conf  = $data['files']['coordinates']['fname'];
$mdp   = $data['files']['mdp']['fname'];
$traj  = $data['files']['trajectory']['fname'];
$index = $data['files']['index']['fname'];
$specified_nodes = $data['index']['specified_nodes'];


status_running($ticket,$netindex,$data);






#This step creates a $ticket-netindex.ndx file
$f = "$dir/$ticket-prepenergy-step0";
if($specified_nodes)
{
 $cmd = "cp $dir/$index $dir/$ticket-netindex.ndx; echo $?";
}
else
{
 $cmd = "/bin/bash splitres.sh $ticket $dir $conf $index $netindex 2>&1; echo $?";
}
exec($cmd,$out,$err);
$header = "<p><b>Error creating index</b></p>\n";
do_log($ticket,0,$out,$header);


$f = "$dir/$ticket-prepenergy-step1";
#$cmd = "/usr/bin/perl grp.pl $dir/$ticket-netindex.ndx $dir/$mdp && mv $dir/$mdp-b $dir/$mdp; echo $?";
$cmd = "/usr/bin/python nodes.py $ticket $dir/$ticket-netindex.ndx $dir/$mdp $dir/$ticket-md.mdp 2>&1; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error creating energy groups</b></p>\n";
do_log($ticket,1,$out,$header);



#This step creates a $ticket-job.tpr file
$f = "$dir/$ticket-prepenergy-step2";
$cmd = "cd $dir; $bin/grompp -f $ticket-md.mdp -c $conf -p $top -o $ticket-job.tpr -n $ticket-netindex.ndx -maxwarn 1 2>&1; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error creating tpr file</b></p>\n";
do_log($ticket,2,$out,$header);


$f = "$dir/$ticket-prepenergy-step3";
$cmd = "cd $dir; $bin/mdrun -deffnm $ticket-job -rerun $traj -nt 4 2>&1; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error calculating energies</b></p>\n";
do_log($ticket,3,$out,$header);

$f = "$dir/$ticket-prepenergy-step4";
$cmd = "cd $dir; $bin/gmxdump -e $ticket-job.edr 1> $ticket-enematrix.dat; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error extracting energies</b></p>\n";
do_log($ticket,4,$out,$header);

$f = "$dir/$ticket-prepenergy-step5";
#$cmd = "/usr/bin/perl enerd.pl $dir/$ticket-eneout $dir/$ticket-netindex.ndx $dir/$ticket-enerd.pld; echo $?";
$cmd = "/usr/bin/python enerd.py $ticket; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error creating energy matrix</b></p>\n";
do_log($ticket,5,$out,$header);

$f = "$dir/$ticket-prepenergy-step6";
#$cmd = "/usr/bin/perl netadj.pl $dir/$ticket-adj.pld $dir/$ticket-netindex.ndx $dir/$top $string 1> $dir/$ticket-netout; echo $?";
$cmd = "/usr/bin/python netadj.py $ticket $dir/$ticket-adj.npy; echo $?";
exec($cmd,$out,$err);
$header = "<p><b>Error creating adjacency matrix</b></p>\n";
do_log($ticket,6,$out,$header);

array_map('unlink', glob("$dir/$ticket-job.*"));

chmod("$dir/$ticket-enerd.npy",0664);
chmod("$dir/$ticket-adj.npy",0664);
chmod("$dir/$ticket-netindex.ndx",0664);

status_done($ticket);


?>

</body>
</html>
