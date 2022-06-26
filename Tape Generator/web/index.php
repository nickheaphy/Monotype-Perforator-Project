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
    <link href="css/mono.css" rel="stylesheet">
    <title>Monotype Punch Tape Builder</title>

    <script>
        //dummy jsoncase
        var jsoncase = {};
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
                    <li class="nav-item"><a href="index.php" class="nav-link active" aria-current="page">Home</a></li>
                    <li class="nav-item"><a href="mcaselect.php" class="nav-link">MCA Editor</a></li>
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
                    <label class="col-form-label" for="mca">Font/Matrix Case (MCA):</label>
                    <select class="form-select form-select-sm" aria-label=".form-select-sm example" id="mca">
                        <option value="-1" selected>Choose...</option>
                        <?php
                            while ($row = $res->fetchArray(SQLITE3_NUM)) {
                                echo "<option value='$row[0]'>$row[1]</option>\n";
                            }
                        ?>
                    </select>
                </div>
                
                <div class="row">
                    
                    <div class="col">
                        <div class="form-floating mb-3">
                            <input class="form-control" id="galleywidth" placeholder="9.5" value="100" type="number">
                            <label for="setwidth">Galley Width (mm)</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="padgalley" checked>
                            <label class="form-check-label" for="padgalley">Pad Galley with Quads</label>
                        </div>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="allowhyphens" checked>
                            <label class="form-check-label" for="allowhyphens">Hyphenate Text</label>
                        </div>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="justify" checked>
                            <label class="form-check-label" for="justify">Justify Text</label>
                        </div>
                    </div>
                </div>
                
                <!--
                <div class="mb-3 mt-3">
                    <label for="texttoconvert" class="form-label">Text to Punch</label>
                    <textarea class="form-control" id="texttoconvert" rows="6">TODO - this still needs to be developed...</textarea>
                </div>
                        -->

                <div class="mb-3 mt-3">
                    <label class="col-form-label" for="sampletext">Sample Text:</label>
                    <select class="form-select form-select-sm" aria-label=".form-select-sm example" id="sampletext">
                        <option value="-1" selected>Choose...</option>
                    </select>
                </div>

                <div class="mb-3 d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="button" class="btn btn-primary" id="gobabygo" disabled>Generate Tape</button>
                </div>
            </form>
            <div style="display:none;" class="alert alert-danger" role="alert" id="tapeerror">
                <p>There was a tape error. Please check the tape file.</p>
            </div>
        </div>
    </main>

    <script src="js/bootstrap/bootstrap.bundle.min.js"></script>
    <script src="js/tinymce/tinymce.min.js"></script>
    <script src="js/sampletext.js"></script>

    <!-- <script src="js/matrix_search.js"></script> -->
    
    <!--<script src="js/mcaeditor_func.js"></script>-->
    <script src="js/matrix_transform.js"></script>

    <script src="js/tape_func.js"></script>
    <script src="js/galley_func.js"></script>

    <script src="js/FileSaver.js"></script>
    <script src="js/hypher/hypher.js"></script>

    <script>

        // build the options for the sample text
        let st = document.getElementById('sampletext');
        for (let id in sampletext) {
            var opt = document.createElement('option');
            opt.value = id;
            opt.innerHTML = sampletext[id].title + " by " + sampletext[id].author;
            st.appendChild(opt);
            
        }

        // ------ Setup for TinyMCE --------
        tinymce.init({
            selector: 'textarea#texttoconvert',
            toolbar: true,
            menubar: false,
            formats: {
                smallcaps: {
                    inline: 'span',
                    styles: {
                        'font-variant': 'small-caps'
                    },
                    attributes: {
                        title: 'smallcaps'
                    }
                },
            },
            toolbar: 'undo redo | bold italic smallcaps',
            setup: function (editor) {
                //Adds smallcaps button to the toolbar
                editor.ui.registry.addButton('smallcaps', {
                    icon: 'text-color',
                    tooltip: 'Smallcaps',
                    onAction: function (evt) {
                        editor.focus();
                        editor.undoManager.beforeChange();//Preserve highlighted area for undo
                        editor.formatter.toggle('smallcaps');
                        editor.undoManager.add();//Add an undo point
                    },
                    onPostRender: function () {
                        var ctrl = this;
                        editor.on('NodeChange', function (e) {
                            //Set the state of the smallcaps button to match the state of the selected text.
                            ctrl.active(editor.formatter.match('smallcaps'));
                        });
                    }
                });
            }
        });
        // ---------------------------------
        //event listener for changing the font
        //load it from the database and replace jsoncase
        var fontselect = document.getElementById("mca");
        fontselect.addEventListener("change", function(event) {

            if (event.target.value != "-1") {
                event.preventDefault();
                var request = new XMLHttpRequest();
                var url = "loadmca.php";
                request.open("POST", url, true);
                request.setRequestHeader("Content-Type", "application/json");
                request.onreadystatechange = function () {
                    if (request.readyState === 4 && request.status === 200) {
                        //console.log(request.response);
                        var jsonData = JSON.parse(request.response);
                        //console.log(jsonData);
                        if (jsonData.db_error == "not an error") {
                            jsoncase = JSON.parse(jsonData.jsoncase);
                            check_and_enabled_generate_button();
                        }
                        console.log(jsoncase);
                    }
                };

                var data = JSON.stringify({"db_row_id" : event.target.value});

                request.send(data);
            } else {
                jsoncase = {};
                check_and_enabled_generate_button();
            }
        });

        // ---------------------------------
        // event listener for selecting sample text
        var sampletextdropdown = document.getElementById("sampletext");
        sampletextdropdown.addEventListener("change", function(event) {
            check_and_enabled_generate_button();
        });

        // ---------------------------------
        // event listener for the generate tape button
        var generatetablebutton = document.getElementById("gobabygo");
        generatetablebutton.addEventListener("click", function(event) {

            var selectedsampletext_arraypos = document.getElementById('sampletext').value;
            var texttoconvert = sampletext[selectedsampletext_arraypos].paragraphs;
            var galleywidth_mm = document.getElementById('galleywidth').value;
            var padgalley = document.getElementById('padgalley').checked;
            var hyptext = document.getElementById('allowhyphens').checked;
            var justify = document.getElementById('justify').checked;

            var simplecase = mcatransform_simplecase(jsoncase);
            console.log(texttoconvert);
            
            // add the initial information
            var mca_selected = document.getElementById("mca");
            var mca_text = mca_selected.options[mca_selected.selectedIndex].text;
            tape = "MCA: " + mca_text + "\n\n";
            // send the initial 'stop casting' commands
            tape += stop_casting(simplecase);
            tape += paragraph_generator(texttoconvert, galleywidth_mm, simplecase, "roman", padgalley, hyptext, justify);
            console.log(tape);
            var blob = new Blob([tape], { type: "text/plain;charset=utf-8" });
            saveAs(blob, "tape.txt");

            //check for any tape errors
            document.getElementById('tapeerror').style.display = "none";
            var tapelines = tape.split("\n");
            for (var i=0; i<tapelines.length; i++) {
                if (tapelines[i].charAt(0) == "!") {
                    //bugger, there was an error
                    document.getElementById('tapeerror').style.display = "block";
                    break;
                }
            }
        });

        //------ enabled the generate tape button
        function check_and_enabled_generate_button() {
            var genbutton = document.getElementById("gobabygo");
            console.log("Checking button")
            //things to check
            var sampletext = document.getElementById('sampletext');
            if (Object.keys(jsoncase).length !== 0 && sampletext.options[sampletext.selectedIndex].value != "-1" && document.getElementById('galleywidth').value != "") {
                genbutton.disabled = false;
            } else {
                genbutton.disabled = true;
            }

        }

    </script>
</body>