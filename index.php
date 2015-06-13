<?php
include 'mdn.php';
?>

<html>
<!DOCTYPE html>

<html lang="en">



<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">

<head>

<title>Ortiz Research Group - Chemical Engineering, Columbia University</title>

  <meta charset="utf-8">

  <link rel="stylesheet" href="reset000.css" type="text/css" media="all">

  <link rel="stylesheet" href="style000.css" type="text/css" media="all">

  <script type="text/javascript" src="scripts/jquery-1.js"></script>

  <script type="text/javascript" src="scripts/cufon-yu.js"></script>

  <script type="text/javascript" src="scripts/Colabora.js"></script>

  <script type="text/javascript" src="scripts/cufon-re.js"></script>

  <script type="text/javascript" src="scripts/jquery00.js"></script>

  <!--[if lt IE 7]>

  	<link rel="stylesheet" href="css/ie/ie6.css" type="text/css" media="screen">

    <script type="text/javascript" src="js/ie_png.js"></script>

    <script type="text/javascript">

        ie_png.fix('.png, nav ul img, header nav');

    </script>

  <![endif]-->

</head>



<body id="page1">

  <div id="main">

  	<!-- header -->

    <header>

      <section class="top">

      	<h1><a href="http://www.columbia.edu/cu/cheme/fac-bios/ortiz/faculty.html">Ortiz Research Group</a></h1>

        <form action id="search-form">

          <fieldset>

          	<input type="text" class="text" value>

          </fieldset>

        </form>

      </section>


    </header>

	
    <!--<div class="wrapper">-->

    	<!-- content -->

      <section id="content">





<h2> Welcome to the MDN Server</h2>

<p>MDN is based on an automated protocol for performing network analysis of molecular dynamics trajectories.</p>

<p>We employ customized versions of the widely used <a href="http://www.gromacs.org">GROMACS</a> and <a href="http://www.ks.uiuc.edu/Research/namd/">NAMD</a> programs, along with other computational routines implemented by our group to perform this analysis.</p>

<p>Using MDN is extremely simple: all that is needed is a GROMACS or NAMD trajectory and input files. Check out the <a href="documentation.php">documentation</a>.</p>


<p>Please fill out the form to begin</p>

<form action="" method="post">
Name: <input type="text" name="name"><br>
E-mail: <input type="text" name="email"><br>
<input type="submit">
</form>
<br>
<p><b>Please cite this work as:</b> Ribeiro, AAST; Ortiz, V. Journal of Chemical Theory and Computation, 10, 1762-1769 (2014).</p>



</div>

<?php
/*
Server-side PHP file upload code for HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/

if(isset($_POST["email"]))
{

 $email =  $_POST["email"];
 $name =  $_POST["name"];

 $not_allow[0] = '/\.com/';
 $not_allow[1] = '/\.org/';
 $not_allow[2] = '/\.co\.uk$/';
 $not_allow[3] = '/gmail\./';
 $not_allow[4] = '/yahoo\./';
 $not_allow[5] = '/hotmail\./';

 $nallow = count($not_allow);

 for($ii=0;$ii<$nallow;$ii++)
 {
  $match = preg_match($not_allow[$ii],$email,$matches);
  if($match != 0)
  {
   break;
  }
 }

 if($match != 0)
 {
  if (check_email($email) != True)
  {
   print "<p>Automatic access to MDN is only available to researchers that have access to an email account hosted by an University or other research-related institution, and your email address was not recognized as such.</p>";
   print "<p>Contact us at aar2163@columbia.edu to request MDN access. Please state your name and affiliation.</p>";
   exit;
  }
 }

 #exit;
 $ticket = uniqid();

 $dir = "uploads/$ticket";


 $subject = 'MDN Ticket';
 $message = "Dear $name,\r\rYou have requested to use the MDN server.\r\rYour ticket is: $ticket\r\rPlease access the URL http://mdn.cheme.columbia.edu/validate.php?ticket=$ticket to validate your ticket.\r\rHappy simulating,\rMDN Crew";
 $headers = 'From: aar2163@columbia.edu' . "\r\n" .
    'Reply-To: aar2163@columbia.edu' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();

 $message = wordwrap($message, 100, "\r\n");

 mail($email, $subject, $message, $headers);

 echo "<p>An email has been sent to $email</p>";

 system("mkdir -m 775 $dir");

 $data["ticket"] = $ticket;
 $data["user_name"] = $name;
 $data["user_email"] = $email;


 update_data($ticket,$data);
  
}

?>

</body>
</html>
