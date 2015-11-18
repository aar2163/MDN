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
   $data = json_decode($json_string);

   $hist  = $data->{'hist'};
   $edges = $data->{'edges'};

   $mean = $data->{'mean'};
   $std  = $data->{'std'};

   $nnodes = $data->{'nnodes'};
   $nbonds = $data->{'nbonds'};
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
<p><u>These values will be used for determining network edge weights</u>, according to</p>
<div><img src="formula1.png" width=400></div>
<div><img src="formula2.png" width=400></div>
<p>see <b>Ribeiro and Ortiz, J. Chem. Theo. Comput. 10, 1762-1769 (2014)</b></p>
  <script>
var hist  = ['count'];
var edges = ['edges'];

<?php
 foreach ($hist as $item)
 {
  ?>
  hist.push(<?php print $item;?>);
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
        x: 'edges',
        columns: [
            hist, edges
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

