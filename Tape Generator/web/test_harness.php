<?php

$db = new SQLite3('mca.db');

$db_row_id = 2;

$stm = $db->prepare('SELECT mcacase FROM mca WHERE id = ?');
$stm->bindValue(1, $db_row_id, SQLITE3_INTEGER);
$res = $stm->execute();
$row = $res->fetchArray(SQLITE3_NUM);

$case = $row[0];

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

    <!-- https://github.com/bramstein/hypher -->

    <script src="js/hypher/hypher.js"></script>
    

    <script>
        var jsoncase;
        jsoncase = JSON.parse('<?php echo str_replace("'","\'", $case); ?>');
    </script>

</head>
<body>

    <p>Test Harness Important</p>

    <div class="container">
            <!-- Table that will be replaced by javascript to display the matrix -->
            <table id="matrixcase"></table>
    </div>

    <script src="js/bootstrap/bootstrap.bundle.min.js"></script>
    <script src="js/matrix_search.js"></script>
    
    <script src="js/mcaeditor_func.js"></script>
    <script src="js/matrix_transform.js"></script>

    <script src="js/matrix_test.js"></script>
    <script src="js/tape_func.js"></script>
    <script src="js/galley_func.js"></script>

    <script src="js/FileSaver.js"></script>

    <script>
        //generateTable(document.getElementById("matrixcase"), jsoncase, false);
        //var trie = createTrie(hypher_en_gb["patterns"]);
        console.log(hyphenate("Documentation"));
        //console.log(hyphenate("Documentation"));
        var simplecase = mcatransform_simplecase(jsoncase);
        
        // //console.log(tape_draw(['A','N','0005'],"A","This is an a"));

        // let tape = galley_separator(simplecase, 100, true);
        // //console.log(tape);

        var thetext = "The quick brown fox jumps over documentation the lazy dog.";
        tape = paragraph_generator(thetext, 50, simplecase);
        console.log(tape);

        function saveDynamicDataToFile() {

            //var userInput = document.getElementById("myText").value;

            var blob = new Blob([tape], { type: "text/plain;charset=utf-8" });
            saveAs(blob, "dynamic.txt");
        }

        //console.log(besthyphenation("Documentation", 80, simplecase, "roman"));
    </script>

    <button type="button" onclick="saveDynamicDataToFile();">Click to Save</button>

</body>
</html>
