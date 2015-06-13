<?php
include 'mdn.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>MDN Documentation</title>
<link rel="stylesheet" type="text/css" media="all" href="styles.css" />
<script src="jquery.min.js">
</script>
<script>
$(document).ready(function(){
  $("button").click(function(){
    $("#div1").load("demo_test.txt");
  });
});
</script>
</head>
<body>

<script type="text/javascript">
function recp(id) {
  $('#myStyle').load('data.php?id=' + id);
}
</script>

<!--
<div id='myStyle'>
</div>
-->

<?php
 $ticket = $_GET["ticket"];

 $data = get_data($ticket);
 

 if(!isset($data['ticket']))
 {
  $ticket = 'INVALID';
 }
 
 $software = $data['software']['name'];

  do_header($ticket);

  echo "<p><b><h3>References:</h3></b></p>\n";

  echo "<p><u>Determination of Signaling Pathways in Proteins through Network Theory: Importance of the Topology</u>
        <br>Ribeiro A.A.S.T., Ortiz V. Journal of Chemical Theory and Computation 10, 1762-1769 (2014).";
  echo '<br><a href="http://dx.doi.org/10.1021/ct400977r">DOI: 10.1021/ct400977r</a>';
  echo "\n</p>";

  echo "<p><u>Energy Propagation and Network Energetic Coupling in Proteins</u>
        <br>Ribeiro A.A.S.T., Ortiz V. Journal of Physical Chemistry B 119, 1835-1846 (2015).";
  echo '<br><a href="http://dx.doi.org/10.1021/jp509906m">DOI: 10.1021/jp509906m</a>';
  echo "\n</p>";

  echo "<p><b><h3>MDN Usage:</h3></b></p>\n";

  echo '<p><a href="documentation/file-upload.php?ticket='.$ticket.'&software='.$software.'">File Upload</a></p>';
  echo '<p><a href="documentation/choosing-groups.php?ticket='.$ticket.'&software='.$software.'">Choosing Groups</a></p>';
  echo '<p><a href="documentation/custom-nodes.php?ticket='.$ticket.'&software='.$software.'">Custom Network Definition</a></p>';
  echo '<p><a href="documentation/network-construction.html">Network Construction</a></p>';
  echo '<p><a href="documentation/pathways.html">Selecting Pathways</a></p>';
  echo '<p><a href="documentation/output.html">MDN Output</a></p>';

  echo "<p><b><h3>Network Theory Concepts:</h3></b></p>\n";
  echo '<p><a href="documentation/network-analysis.html">Network Centrality, Node Betweenness, and Network Coupling</a></p>';

?>


<script src="filedrag.js"></script>
</body>
</html>
