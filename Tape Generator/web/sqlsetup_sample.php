<?php

$db = new SQLite3('mca.db');

$db->exec("CREATE TABLE IF NOT EXISTS mca(id INTEGER PRIMARY KEY, macname TEXT, mcacase TEXT)");

$db->exec("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT, pwd TEXT)");

$stm = $db->prepare("INSERT INTO users (email, pwd) VALUES (?, ?)");
$stm->bindValue(1, "sample@sample.com");
$stm->bindValue(2, password_hash("sample", PASSWORD_DEFAULT));
$res = $stm->execute();

?>