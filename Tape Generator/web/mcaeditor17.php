<?php

session_start();

$db = new SQLite3('mca.db');

// what are we doing?
// check to see if mode is set, otherwise default to new
$mode = $_GET["mode"] ?? 'new';
$db_row_id = $_GET["mca"] ?? -1;

if ($mode == "duplicate" && $db_row_id != '-1') {
    // duplicate the entry in the database and then edit this new one
    // get the existing entry
    $stm = $db->prepare('SELECT mcacase FROM mca WHERE id = ?');
    $stm->bindValue(1, $db_row_id, SQLITE3_INTEGER);
    $res = $stm->execute();
    $row = $res->fetchArray(SQLITE3_NUM);

    $case = $row[0];

    $casedata = json_decode($case, false, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK);
    $mcatitle = $casedata->title . " (Copy)";
    $mcadescription0 = $casedata->description0;
    $mcadescription1 = $casedata->description1;
    $mcadescription2 = $casedata->description2;
    $mcawedge = $casedata->wedge;
    $mcasetwidth = $casedata->setwidth;

    //$case = json_encode(json_decode($case,false, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK));

    //$case = json_encode($case, JSON_HEX_QUOT | JSON_HEX_APOS);
    // reset the dbrow so when saving it will create a new row in the db
    $db_row_id = "-1";

} elseif (($mode == "edit" || $mode == "show") && $db_row_id != '-1') {
    // get the existing entry
    $stm = $db->prepare('SELECT mcacase FROM mca WHERE id = ?');
    $stm->bindValue(1, $db_row_id, SQLITE3_INTEGER);
    $res = $stm->execute();
    //error_log("Cols = " . $res->numColumns() . " Type = " . $res->columnType(0) . " >" . $stm->getSQL());

    if ($res->numColumns() && $res->columnType(0) != SQLITE3_NULL) {
        $row = $res->fetchArray(SQLITE3_NUM);
        
        if ($row) {
            $case = $row[0];
            $casedata = json_decode($case, false, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK);
            $mcatitle = $casedata->title;
            $mcadescription0 = $casedata->description0;
            $mcadescription1 = $casedata->description1;
            $mcadescription2 = $casedata->description2;
            $mcawedge = $casedata->wedge;
            $mcasetwidth = $casedata->setwidth;
            //$case = json_encode(json_decode($case,false, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_NUMERIC_CHECK));

        } else {
            // create a blank if error
            $db_row_id = -1;
            $mcatitle = "";
            $mcadescription0 = "";
            $mcadescription1 = "";
            $mcadescription2 = "";
            $mcawedge = "";
            $mcasetwidth = "";
            $case = '{}';
        }
    }

} else {
    // default is to create a new MCA
    $db_row_id = -1;

    $mcatitle = "";
    $mcadescription0 = "";
    $mcadescription1 = "";
    $mcadescription2 = "";
    $mcawedge = "";
    $mcasetwidth = "";

    $case = '{}';
}

//fix the slashes
$case = str_replace("\\", "\\\\", $case);

function latest_version($file_name){
    echo $file_name."?".filemtime($_SERVER['DOCUMENT_ROOT']."/".dirname($_SERVER['PHP_SELF'])."/".$file_name);
}

?>
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="css/bootstrap/bootstrap.min.css" rel="stylesheet">
    
    <link href="<?php latest_version('css/mono.css'); ?>" rel="stylesheet">

    <title>Monotype Punch Tape Builder</title>

    <script>
        // store the row ID for later use when updating
        var db_row_id = <?php echo $db_row_id; ?>;
        var editmode = "<?php echo $mode; ?>";
    </script>

</head>

<body>
    <main>
        <div class="container">
            <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom d-print-none">
                <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dice-6-fill" viewBox="0 0 16 16">
                        <path d="M3 0a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V3a3 3 0 0 0-3-3H3zm1 5.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm8 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5 6.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM12 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zM5.5 12a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM4 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                      </svg>
                    <span class="ms-1 fs-4">Monotype Punch Tape Builder</span>
                </a>

                <ul class="nav nav-pills">
                    <li class="nav-item"><a href="index.php" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="mcaselect.php" class="nav-link active" aria-current="page">MCA Editor</a></li>
                    <li class="nav-item"><a href="tools.php" class="nav-link">Tools</a></li>
                    <li class="nav-item"><a href="about.php" class="nav-link">About</a></li>
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
            <form>
                <div class="mb-3">
                    <label for="mcatitle" class="col-form-label">Font Title:</label>
                    <input type="text" class="form-control" id="mcatitle" value="<?php echo $mcatitle; ?>" disabled>
                </div>
                <div class="mb-3">
                    <label for="mcadescription" class="col-form-label">MCA/Font Description:</label>
                    <input type="text" class="form-control mb-1" id="mcadescription0" value="<?php echo $mcadescription0; ?>" disabled>
                    <input type="text" class="form-control mb-1" id="mcadescription1" value="<?php echo $mcadescription1; ?>" disabled>
                    <input type="text" class="form-control" id="mcadescription2" value="<?php echo $mcadescription2; ?>" disabled>
                </div>
                <div class="row">
                    <div class="col">
                        <div class="form-floating mb-3">
                            <input class="form-control" id="mcawedge" placeholder="MCA Wedge" value="<?php echo $mcawedge; ?>" disabled>
                            <label for="mcawedge">MCA Wedge</label>
                        </div>  
                    </div>
                    <div class="col">
                        <div class="form-floating mb-3">
                            <input class="form-control" id="setwidth" placeholder="Set Width" value="<?php echo $mcasetwidth; ?>" disabled>
                            <label for="setwidth">Set Width</label>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        <div class="container">
            <!-- Table that will be replaced by javascript to display the matrix -->
            <table id="matrixcase"></table>

            <!-- Save and validate buttons -->
            <div class="mb-3 start-50">
                <button type="button" class="btn btn-success" id="validatemca">Validate</button>
                <?php
                    if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true && ($mode == "edit" || $mode == "new" || $mode == "duplicate")) {
                        echo '<button type="button" class="btn btn-primary" id="savemca" disabled>Save MCA</button>';
                    }
                ?>
            </div>
            
            <!-- Modal Dialog allowing you to edit the properties of the individual cells in the matrix -->
            <div class="modal fade" id="matrixModal" tabindex="-1" aria-labelledby="matrixModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="matrixModalLabel">Edit Matrix Item</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="matrixpos" class="col-form-label">Matrix Position:</label>
                            <input type="text" class="form-control" id="matrixpos" disabled>
                        </div>
                        <div class="mb-3">
                        <label for="character" class="col-form-label">Character:</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="character" maxlength="1" autofocus>
                            <button onClick="window.open('https://unicode-table.com/en/');" class="btn btn-outline-secondary" type="button" for="character">UniCode</button>
                        </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="charstyle" id="charstyle1" checked>
                                    <label class="form-check-label" for="charstyle1">
                                        Roman
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="charstyle" id="charstyle2">
                                    <label class="form-check-label" for="charstyle2">
                                        Italic
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="charstyle" id="charstyle3">
                                    <label class="form-check-label" for="charstyle3">
                                        Small Caps
                                    </label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="charweight" id="charweight1" checked>
                                    <label class="form-check-label" for="charweight1">
                                        Normal
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="charweight" id="charweight2">
                                    <label class="form-check-label" for="charweight2">
                                        Bold
                                    </label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="special" value="" id="specialnormal" checked>
                                    <label class="form-check-label" for="specialnormal">
                                        Normal
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="special" value="sspace" id="specialsspace">
                                    <label class="form-check-label" for="specialsspace">
                                        S-Space
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="special" value="lowspace" id="speciallowspace">
                                    <label class="form-check-label" for="lowpsace">
                                        Low Space
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="special" value="blank" id="specialblank">
                                    <label class="form-check-label" for="specialblank">
                                        Blank
                                    </label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="special" value="na" id="specialna">
                                    <label class="form-check-label" for="specialna">
                                        Not Available
                                    </label>
                                </div>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="unitshift">
                                    <label class="form-check-label" for="unitshift">Unit Shift</label>
                                </div>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="padding">
                                    <label class="form-check-label" for="padding">Padding</label>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                        <label for="description-text" class="col-form-label">Description and/or Notes:</label>
                        <textarea class="form-control" id="description-text"></textarea>
                        </div>
                    </form>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <?php
                        if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true && ($mode == "edit" || $mode == "new" || $mode == "duplicate")) {
                            echo '<button type="button" class="btn btn-primary" id="matrixSaveButton">Store</button>';
                        }
                    ?>
                    </div>
                </div>
                </div>
            </div>

            <!-- Modal Dialog allowing you to edit the unit values of the case -->
            <div class="modal fade" id="unitModal" tabindex="-1" aria-labelledby="unitModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="unitModalLabel">Edit Unit</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="rowpos" class="col-form-label">Row Position:</label>
                            <input type="text" class="form-control" id="rowpos" disabled>
                        </div>
                        <div class="mb-3">
                        <label for="units" class="col-form-label">Units:</label>
                        <input type="text" class="form-control" id="units">
                        </div>
                    </form>
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    
                    <?php
                        if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true && ($mode == "edit" || $mode == "new" || $mode == "duplicate")) {
                            echo '<button type="button" class="btn btn-primary" id="unitSaveButton">Store</button>';
                        }
                    ?>
                    </div>
                </div>
                </div>
            </div>

            <!-- Validation Report Model Dialog -->
            <div class="modal fade" id="validateModal" tabindex="-1" aria-labelledby="validateModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="unitModalLabel">Validation Report</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div id="errorreport" class="modal-body">
                    
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
                </div>
            </div>
            <!-- ------------------------------ -->
        </div>
    </main>
    <script src="js/bootstrap/bootstrap.bundle.min.js"></script>
    
    <script src="<?php latest_version('js/mcaeditor_func17.js'); ?>"></script>
    <script src="<?php latest_version('js/mcaeditor_el17.js'); ?>"></script>

    <script>
        var jsoncase;
        jsoncase = JSON.parse('<?php echo str_replace("'","\'", $case); ?>');
        fixProperties(jsoncase);
        generateTable(document.getElementById("matrixcase"), jsoncase);

        //event listener for saving
        var savebutton = document.getElementById("savemca");
        if (savebutton != null) {
            savebutton.addEventListener("click", function(event) {

                //update the case with the entered data
                //the rows, columns and units are updated already
                jsoncase.title = document.getElementById("mcatitle").value;
                jsoncase.description0 = document.getElementById("mcadescription0").value;
                jsoncase.description1 = document.getElementById("mcadescription1").value;
                jsoncase.description2 = document.getElementById("mcadescription2").value;
                jsoncase.wedge = document.getElementById("mcawedge").value;
                jsoncase.setwidth = document.getElementById("setwidth").value;

                event.preventDefault();
                var request = new XMLHttpRequest();
                var url = "savemca.php";
                request.open("POST", url, true);
                request.setRequestHeader("Content-Type", "application/json");
                request.onreadystatechange = function () {
                    if (request.readyState === 4 && request.status === 200) {
                        console.log(request.response);
                        var jsonData = JSON.parse(request.response);
                        console.log(jsonData);
                        if (jsonData.db_error == "not an error") {
                            db_row_id = jsonData.db_row_id;
                            // disable the save button after save successful
                            document.getElementById("savemca").disabled = true;
                        }
                    }
                };

                var data = JSON.stringify({"db_row_id" : db_row_id, "case" : jsoncase});

                request.send(data);
            });
        }

        //event listener for validation
        var validatebutton = document.getElementById("validatemca");
        validatebutton.addEventListener("click", function(event) {
            var myModal = new bootstrap.Modal(document.getElementById('validateModal'))
            myModal.show(this);
        });

        if (editmode == "edit" || editmode == "new" || editmode == "duplicate") {
            // enable editing
            document.getElementById("mcatitle").disabled = false;
            document.getElementById("mcadescription0").disabled = false;
            document.getElementById("mcadescription1").disabled = false;
            document.getElementById("mcadescription2").disabled = false;
            document.getElementById("mcawedge").disabled = false;
            document.getElementById("setwidth").disabled = false;
            //change event
            document.getElementById("mcatitle").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
            document.getElementById("mcadescription0").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
            document.getElementById("mcadescription1").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
            document.getElementById("mcadescription2").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
            document.getElementById("mcawedge").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
            document.getElementById("setwidth").addEventListener("keyup", function() {
                document.getElementById("savemca").disabled = false;
            });
        }

    </script>
</body>
</html>