<?php
// Initialize the session
session_start();

$db = new SQLite3('mca.db');

if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    $enableedit = true;
} else {
    $enableedit = false;
}

// get the list of MCAs
$res = $db->query('SELECT id, mcaname, mcacase FROM mca');

?>
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="css/bootstrap/bootstrap.min.css" rel="stylesheet">

    <title>Monotype Punch Tape Builder</title>

    <script>
        //dummy jsoncase
        var jsoncase = {};
    </script>

</head>

<body>
    <main>
        <div class="container">
            <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
                <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dice-6-fill" viewBox="0 0 16 16">
                        <path d="M3 0a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V3a3 3 0 0 0-3-3H3zm1 5.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm8 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5 6.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM12 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM5.5 12a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM4 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                      </svg>
                    <span class="ms-1 fs-4">Monotype Punch Tape Builder</span>
                </a>

                <ul class="nav nav-pills">
                    <li class="nav-item"><a href="index.php" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="mcaselect.php" class="nav-link">MCA Editor</a></li>
                    <li class="nav-item"><a href="tools.php" class="nav-link">Tools</a></li>
                    <li class="nav-item"><a href="about.php" class="nav-link active" aria-current="page">About</a></li>
                    <?php
                    if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
                        echo '<li class="nav-item"><a href="login.php" class="nav-link text-danger">Logout</a></li>';
                    } else {
                        echo '<li class="nav-item"><a href="login.php" class="nav-link">Login</a></li>';
                    }
                    ?>
                </ul>
            </header>
        </div>
        <div class="container">
            <p>Still to write this...
        </div>
    </main>
    <script src="js/bootstrap/bootstrap.bundle.min.js"></script>

    <script>
    </script>
</body>
</html>