<?php
define('UPLOAD_DIR', '/Users/xtian/Documents/GitHub/coca_coda_app/app/uploads/');
$img = $_POST['fileToUpload'];
$img = str_replace('data:fileToUpload/jpeg;base64,', '', $img);
$img = str_replace(' ', '+', $img);
$data = base64_decode($img);
$file = UPLOAD_DIR . uniqid() . '.png';
$success = file_put_contents($file, $data);
print $success ? $file : 'Unable to save the file.';
?>
