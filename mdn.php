<?php

 function update_data($ticket,$data)
 {
  $mongo = new MongoClient();
  $db = $mongo->selectDB("MDN");
  $col = $db->jobs;

  $qticket = array('ticket' => $data['ticket']);
  $options = array('upsert' => 1);
  $col->update($qticket,$data,$options);
  #$col->insert($data);

 }
 function get_data($ticket)
 {
  $mongo = new MongoClient();
  $db = $mongo->selectDB("MDN");
  $col = $db->jobs;
  $qticket = array('ticket' => $ticket);
  #$project = array('topology' => 0);
  $data = $col->findOne($qticket);
  return $data;
 }
 function check_ticket($ticket,$data)
 {
  if(!isset($ticket))
  {
   return False;
  }

  if(!isset($data))
  {
   $data = get_data($ticket);
  }

  if(!isset($data["ticket"]))
  {
   return False;
  }
  if($data["ticket"] != $ticket)
  {
   return False;
  }
  return True;
 }
 function check_email($email)
 {
  $mongo = new MongoClient();
  $db = $mongo->selectDB("MDN");
  $col = $db->allowed_emails;
  $qemail = array('email' => $email);
  $data = $col->findOne($qemail);
  if(isset($data))
  {
   return True;
  }
  else
  {
   return False;
  }
 }
 function do_header($ticket)
 {
  echo "<link href=\"site.css\" media=\"all\" rel=\"stylesheet\" type=\"text/css\">";
  echo "<header>\n";
  echo '<a href="documentation.php?ticket='.$ticket.'" id="box-link2"></a>'."\n";
  echo '<a href="main.php?ticket='.$ticket.'" id="box-link"></a>'."\n";
  echo "</header>\n";
 }
 function do_cmd($cmd)
 {
  unset($out);
  exec($cmd,$out,$err);
  return $out;
 }
?>
