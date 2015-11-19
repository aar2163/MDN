<?php
 include 'mdn.php'
?>

<html>
 <head>
    <title>Network Overview</title>
    <link href="c3.css" rel="stylesheet" type="text/css">
<script src="d3.min.js" charset="utf-8"></script>
<script src="c3.min.js"></script>
  </head>
 <body>
<?php
 if(isset($_GET["ticket"]))
 {
  $ticket = $_GET["ticket"];

  $data = get_data($ticket);

  if(!isset($data['ticket']))
  {
   echo "<p>Invalid ticket</p>";
  }
  else
  {
   do_header($ticket);
   $json_string = `python prep_histogram.py $ticket`;
   $hist = json_decode($json_string);

   $counts = $hist->{'counts'};
   $edges  = $hist->{'edges'};

   $mean = $hist->{'mean'};
   $std  = $hist->{'std'};

   $nnodes = $hist->{'nnodes'};
   $nbonds = $hist->{'nbonds'};
?>
<center>
<h2>Network Overview</h2>
<p>The network contains <?php print $nnodes?> nodes, and <?php print $nbonds; ?> edges represent chemical bonds.</p>
<p><u>Network edge weights are based on interaction energies.</u></p>
<h2>Interaction Energy Distribution (non-bonded interactions)</h2>
<div id="chart"></div></center>
<h2>Statistics (kcal/mol)</h2>
<p>Mean: <?php print $mean; ?><p>
<p>Std. Dev.: <?php print $std; ?></p>
<p><u>These values are used as parameters for determining network edge weights</u>, according to</p>
<div><img src="formula1.png" width=400></div>
<div><img src="formula2.png" width=400></div>
<p>see <b>Ribeiro and Ortiz, J. Chem. Theo. Comput. 10, 1762-1769 (2014)</b></p>


<?php
  if (isset($_GET["setparams"]))
  {
   if (isset($_GET["mean"]) and isset($_GET["std"]))
   {
    $mean = floatval($_GET["mean"]);
    $std  = floatval($_GET["std"]);
    if ($std > 0)
    {
     $data = get_data($ticket);
     $data["network"]["params"]["mean"] = $mean;
     $data["network"]["params"]["std"]  = $std;
     unset($data['output_files']);
     update_data($ticket, $data);
?>
     <h3>Updating network.</h3>
<?php
    }
    else
    {
?>
     <h3>Invalid values. <a href="?ticket=<?php print $ticket;?>&setparams">Try again</a></h3>
<?php
    }
   }
   else
   {
?>
    <form action="" method="get">
    <input type="hidden" name="ticket" value ="<?php print $ticket;?>">
    <input type="hidden" name="setparams">
    <p>Mean: <input type="text" name="mean"></p>
    <p>Std. Dev.: <input type="text" name="std"></p>
    <p><input type="submit"></p>

<?php
   }
  }
  else
  {
?>
   <h3><a href="?ticket=<?php print $ticket;?>&setparams">Click here to specify different parameter values</a></h3>
<?php
  }
  if(isset($data["network"]["params"]))
  {
   $mean = $data["network"]["params"]["mean"];
   $std  = $data["network"]["params"]["std"];
?>
   <h3>You chose to use the values <?php print $mean;?> (mean) and <?php print $std;?> (std dev).</h3>
<?php
  }
?>
  <script>
var counts = ['count'];
var edges  = ['bins'];

<?php
 foreach ($counts as $item)
 {
  ?>
  counts.push(<?php print $item;?>);
  <?php 
 }
 foreach ($edges as $item)
 {
  ?>
  edges.push(<?php print $item;?>);
  <?php 
 }
?>


var chart = c3.generate({
    legend: { show: false },
    size: {width: 500},
    data: {
        x: 'bins',
        columns: [
            counts, edges
        ],
        type: 'bar'
    },
    bar: {
        width: {
            ratio: 0.5 // this makes bar width 50% of length between ticks
        }
        // or
        //width: 100 // this makes bar width 100px
    },
    axis: {
     x: {
      label: { 
       text: 'Energy (kcal/mol)',
       position: 'outer-center'
      }
     },
     y: {
      label: { 
       text: 'Count',
       position: 'outer-middle'
      }
     }
    }
});
<?php
  }
 }
?>
 </script>
 </body>
</html>

