<?php
// https://stackoverflow.com/questions/50152966/post-method-to-send-form-data-with-ajax-without-jquery
// https://zetcode.com/php/sqlite3/
// Handling data in JSON format on the server-side using PHP

session_start();

header("Content-Type: application/json");
// build a PHP variable from JSON sent using POST method

$v = json_decode(stripslashes(file_get_contents("php://input")),true);

$db = new SQLite3('mca.db');

$stm = $db->prepare('SELECT mcacase FROM mca WHERE id = ?');
$stm->bindParam(1, $v["db_row_id"]);
$result = $stm->execute();

if ($result->numColumns()) {
    while ($row = $result->fetchArray()) {
        echo json_encode(array('db_error' => "not an error", 'jsoncase' => ($row['mcacase'])));
        break;
    }
} else {
    echo json_encode(array('db_error' => $db->lastErrorMsg(), 'jsoncase' => ""));
}
?>