<?php
include 'mdn.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>MDN File Upload</title>
<link rel="stylesheet" type="text/css" media="all" href="styles.css" />

<script src="jquery.min.js"></script>

<script>
$(window).load(function(){
$(".tiptext").mouseover(function() {
    $(this).children(".description").show();
}).mouseout(function() {
    $(this).children(".description").hide();
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
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/
$fn = (isset($_SERVER['HTTP_X_FILENAME']) ? $_SERVER['HTTP_X_FILENAME'] : false);

if ($fn) {

	// AJAX call
	file_put_contents(
		'uploads/' . $fn,
		file_get_contents('php://input')
	);
	echo "$fn uploaded";
	exit();

}
else {
 $ticket = $_GET["ticket"];
 $data = get_data($ticket);
 // form submit
 $file = $_FILES['fileselect'];
 $bUpload = 1;
 /*foreach ($files['error'] as $id => $err) 
 {*/
 $err = $file['error'];
 if (isset($err) and $err == UPLOAD_ERR_OK) 
 {
  $fn = $file['name'];
  $ticket = $_POST['ticket'];
  $dir = $data['base_dir'];
  $type = $_POST['type'];
  $cmd = "python valid_upload.py $ticket $type $fn; echo $?";
  unset($out);
  exec($cmd,$out,$err);
  $valid = ($out[count($out)-1] == 0);
 
 
  if($valid)
  {
   
   /* Move uploaded files to job directory specified in the base_dir database variable */
   move_uploaded_file($file['tmp_name'], $dir . $fn);
   $post_out = "<p>File $fn uploaded.</p>\n";

   $cmd = "/usr/bin/python update_file.py $ticket upload $type $fn; echo $?";
   unset($out);
   exec($cmd,$out,$err);
  
   if($type == "topology")
   { 
    $cmd = "/usr/bin/python readtop.py $ticket 2> $dir/saida; echo $?";
    unset($out);
    exec($cmd,$out,$err);
   }
   if($type == "coordinates" and $data['software']['name'] == "namd")
   { 
    $bindir = $data['software']['gromacs_bindir'];
    $input =  $dir . $fn;
    $output = $dir . $ticket . "-groups.ndx";

    do_cmd("echo q|$bindir/make_ndx -f $input -o $output; echo $?");

    $file =  $ticket . "-groups.ndx";
    do_cmd("/usr/bin/python update_file.py $ticket upload index $file; echo $?");
   }
  }
  else
  {
   $post_out = "<p>Invalid file $fn</p>";
  }
 }
 if (isset($err) and $err == UPLOAD_ERR_INI_SIZE) 
 {
   $limit = ini_get('upload_max_filesize');
   $post_out = "<p>File $fn exceeds $limit</p>";
 }
 
 #}
}     
?>

<?php
 $ticket = $_GET["ticket"];
 if(!check_ticket($ticket,$data))
 {
  echo "<p>Invalid ticket.</p>";
 }
 else
 {
  #$data = get_data($ticket);

  $dir = $data['base_dir'];

  $cmd = "python filesinfo.py $ticket; echo $?";
  unset($out);
  exec($cmd,$out,$err);
  $count = count($out);

  for($ii=0;$ii<$count-1;$ii++)
  {
   $v[$ii] = split(' ',$out[$ii]);
   #echo $out[$ii]."\n";
  }

  do_header($ticket);
  echo '<p><b>Job name: '.$data['jobname'].'</b></p>'."\n";
  echo '<p>Need help? <a href="documentation/file-upload.html">Click here</a></p>'."\n";



   echo '<div id="files">
	<div id="file_index" class="file">
		<h2>Index</h2>
		<ul>';
                  for($ii=0;$ii<$count-1;$ii++)
                  {
                        $popup = "Possible extensions: ";
                        for($jj=4;$jj<count($v[$ii]);$jj++)
                        {
                         $string = preg_replace('/\[/','',$v[$ii][$jj]);
                         $string = preg_replace('/\]/','',$string);
                         $string = preg_replace('/u\'/','',$string);
                         $string = preg_replace('/\'/','',$string);
                         $popup = $popup . $string;
                        }
			echo '<li><span class="tip"><span><div class="tiptext">'. $v[$ii][1] .'<div class="description"><b>'.$popup.'</b></div></div></span></li>';
                  }
  echo '      </ul>
        </div>

        <div id="file_file" class="file">
		<h2>Group</h2>
		<ul>';
                  for($ii=0;$ii<$count-1;$ii++)
                  {
                        if($v[$ii][2] == "False")
                        {
                         echo '<li><span class="tip"><a href="files.php?ticket='. $ticket .'&type='. $v[$ii][0] .'">Upload File</a></span></li>';
                        }
                        else
                        {
                         $name = $v[$ii][3];
                         if (strlen($name) > 20) 
                         {
                          $name = "..." . substr($name, -20);
                         }
			 echo '<li><span class="tip">'. $name .'</span></li>';
                        }
                  }
  echo '      </ul>
        </div>

        <div id="file_delete" class="file">
                <h2>Group</h2>
		<ul>';
                  for($ii=0;$ii<$count-1;$ii++)
                  {
                       if($v[$ii][2] == "True")
                       {
			echo '<li><span class="tip"><a href="files.php?ticket='.$ticket.'&type='.$v[$ii][0].'&delete=yes"><img width="10px" src="images/delete.png"></a></span></li>';
                       }
                       else
                       {
			echo '<li><span class="tip"><img width="10px" src="images/null.png"></span></li>';
                       }
                  }
  echo '      </ul>
        </div>';
  $type = $_GET["type"];
  $ticket = $_GET["ticket"];
  $delete = $_GET["delete"];

  if(isset($type) and $delete == "yes")
  {
   $cmd = "python valid_type.py $ticket $type; echo $?";
   unset($out);
   exec($cmd,$out,$err);
   $valid = ($out[count($out)-1] == 0);

   if($valid)
   {
    $v = $data['files'][$type]['fname'];

    $cmd = "/usr/bin/python update_file.py $ticket delete $type $v 2> $dir/saida; echo $?";
    unset($out);
    exec($cmd,$out,$err);
    

    echo "<p>Deleted file $v</p>";
    echo '<p><a href="files.php?ticket='. $ticket .'">Update List</a></p>';
   }
  }
  else if (isset($type) and !isset($_FILES['fileselect']))
  {
   $cmd = "python valid_type.py $ticket $type; echo $?";
   unset($out);
   exec($cmd,$out,$err);
   $valid = ($out[count($out)-1] == 0);

   if ($valid)
   {
    /*$key = array_search($type,$file_t);*/

    echo "<div><form id=\"upload\" action=\"\" method=\"POST\" enctype=\"multipart/form-data\">";

    $extension = $data['files'][$type]['extension'];
    $popup = "Possible extensions: ";
    foreach ($extension as $value)
    {
     $string = preg_replace('/\[/','',$value);
     $string = preg_replace('/\]/','',$string);
     $string = preg_replace('/u\'/','',$string);
     $string = preg_replace('/\'/','',$string);
     $popup = $popup . " $string,";
    }
    $popup = preg_replace('/,$/','',$popup);

    echo "<fieldset>";
    echo "<legend>File Upload: $type</legend>";
    echo "<p><b>$popup</b></p>\n";
 
    echo "<input type=\"hidden\" id=\"MAX_FILE_SIZE\" name=\"MAX_FILE_SIZE\" value=\"100000000\" />";

    echo "<input type=\"hidden\" name=\"ticket\" value=\"$ticket\" />";

    echo "<input type=\"hidden\" name=\"type\" value=\"$type\" />";

    echo "<input type=\"hidden\" id=\"FNAME\" name=\"FNAME\" value=\"$fname\">";
 
/*    echo '<div class="fileUpload">';
    #echo 	"<label for=\"fileselect\" type=\"file\">Choose Files:</label>";
    #echo 	'<input class="upload" type="file" id="fileselect" name="fileselect[]" multiple="multiple">';
    echo  '<span>Upload</span>';
    echo 	'<input class="upload" type="file">';
    echo "</div>";*/

    echo '

<input id="uploadFile" placeholder="Choose File" disabled="disabled" />
<div class="fileUpload btn btn-primary">
    <span><img src="images/select.gif"></span>
    <input id="uploadBtn" type="file" name="fileselect" class="upload" />
</div>';

/*<div class="fileinputs">
<input id="uploadFile" placeholder="Choose File" disabled="disabled" />
	<input type="file" class="file" id="fileselect" name="fileselect">
	<div class="fakefile">
                <input>
		<img src="images/select.gif">
	</div>
     </div>*/

    echo "<div id=\"submitbutton\">";
    echo "	<input type=\"submit\" value=\"Upload Files\">";
    echo "</div>";
    echo "</fieldset>";

    echo "</form>";

    echo "<div id=\"progress\"></div>";

    #echo "<div id=\"messages\">";
    echo "</div></div>";
   }
   else
   {
    echo "<div>Incorrect Type</div></div>";
   }
  }
 }
?>

<?php
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/

if (isset($post_out)) 
{

 echo $post_out;

}

$cmd = "python check_files.py $ticket 2> /dev/null; echo $?";
unset($out);
exec($cmd,$out,$err);
$valid = ($out[count($out)-1] == 0);
$error = ($out[count($out)-1] == 2);

if($valid)
{
 $data = get_data($ticket);
 echo "<p><b>Files successfully uploaded</b></p>\n";
 echo "<p><b>Here is a brief overview of your files: </b></p>\n";
 $out = $data['files']['upload_log'];
 for($ii=0;$ii<count($out);$ii++)
 {
  $s = $out[$ii];
  echo "<p><b>$s</b></p>\n";
 }
}
elseif($error)
{
 echo "<p><b>There are some errors with your files:</b></p>\n";
 $out = $data['files']['upload_log'];
 for($ii=0;$ii<count($out);$ii++)
 {
  $s = $out[$ii];
  echo "<p><b>$s</b></p>\n";
 }
}


?>


<script src="filedrag.js"></script>
</body>
</html>
<script>
document.getElementById("uploadBtn").onchange = function () {
 var filePath  = this.value;
 if(filePath.match(/fakepath/)) 
 {
  // update the file-path text using case-insensitive regex
  filePath = filePath.replace(/C:\\fakepath\\/i, '');
 }
 document.getElementById("uploadFile").value = filePath;

};
</script>
