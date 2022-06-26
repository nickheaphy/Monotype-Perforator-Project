<?php

//Download the MCA database as a JSON file

session_start();

header("Content-Type: application/json");
// build a PHP variable from JSON sent using POST method

$db = new SQLite3('../mca.db');

$stm = $db->prepare('SELECT mcaname, mcacase FROM mca');
$result = $stm->execute();

if ($result->numColumns()) {
    while ($row = $result->fetchArray()) {
        $dbdata = array('mcaname' => $row['mcaname'], 'mcacase' => ($row['mcacase']));
    }
} else {
    $dbdata = array('db_error' => $db->lastErrorMsg());
}


echo json_encode($dbdata);

?>