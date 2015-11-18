<html>
 <head>
    <title>Energy Histogram</title>
    <link href="c3.css" rel="stylesheet" type="text/css">
<script src="d3.min.js" charset="utf-8"></script>
<script src="c3.min.js"></script>
  </head>
 <body>
<?php
 $ticket = $_GET["ticket"];
 $json_string = `python prep_histogram.py $ticket`;
 $data = json_decode($json_string);

 $hist  = $data->{'hist'};
 $edges = $data->{'edges'};

?>
<div id="chart"></div>
  <script>
var hist  = ['data'];
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
    }
});


 </script>
 </body>
</html>

