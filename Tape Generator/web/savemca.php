<?php
// https://stackoverflow.com/questions/50152966/post-method-to-send-form-data-with-ajax-without-jquery
// https://zetcode.com/php/sqlite3/
// Handling data in JSON format on the server-side using PHP

session_start();

header("Content-Type: application/json");
// build a PHP variable from JSON sent using POST method

if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {

    $thedat = file_get_contents("php://input");
    //error_log($thedat);
    $v = json_decode(($thedat),true);
    

    $db = new SQLite3('mca.db');
    $db->exec("CREATE TABLE IF NOT EXISTS mca(id INTEGER PRIMARY KEY, mcaname TEXT, mcacase TEXT)");

    if ($v["db_row_id"] == "-1") {
        // this is a new item for the database
        $case = json_encode($v["case"]);
        $case_title = $v["case"]["title"];

        $stm = $db->prepare('INSERT INTO mca(mcaname, mcacase) VALUES (?, ?)');
        $stm->bindParam(1, $case_title);
        $stm->bindParam(2, $case);
        $result = $stm->execute();

        // find the last inserted rowID
        $last_row_id = $db->lastInsertRowID();

    } else {
        // need to update the database row
        $case = json_encode($v["case"]);
        $case_title = $v["case"]["title"];

        $stm = $db->prepare('UPDATE mca SET mcaname = ?, mcacase = ? WHERE id = ?');
        $stm->bindParam(1, $case_title);
        $stm->bindParam(2, $case);
        $stm->bindParam(3, $v["db_row_id"]);
        $result = $stm->execute();
        
        $last_row_id = $v["db_row_id"];

    }
    echo json_encode(array('db_error' => $db->lastErrorMsg(), "db_row_id" => $last_row_id));

} else {
    echo json_encode(array('db_error' => "user not logged in", "db_row_id" => -1));
}

?>