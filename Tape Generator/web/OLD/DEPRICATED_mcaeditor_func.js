// -----------------------------------------------------------
/**
 * Ensure that we have a 15x15 array
 * This is a bit rude as you can have larger matrix cases, but at the moment only
 * concerned with 15x15 (this will probably bite me later)
 * @param {object} jsoncase - a case in the json format used to store in the db 
 */
function fixProperties(jsoncase) {

    if (!("title" in jsoncase)) {jsoncase.title = "";}
    if (!("description0" in jsoncase)) {jsoncase.description0 = "";}
    if (!("description1" in jsoncase)) {jsoncase.description1 = "";}
    if (!("description2" in jsoncase)) {jsoncase.description2 = "";}
    if (!("wedge" in jsoncase)) {jsoncase.wedge = "";}
    if (!("setwidth" in jsoncase)) {jsoncase.setwidth = "";}

    // check to see if we have units (if we do, assume they are correct)
    if (!("units" in jsoncase)) {
        jsoncase.units = {"1":5,"2":6,"3":7,"4":8,"5":9,"6":9,"7":10,"8":10,"9":11,"10":12,"11":13,"12":14,"13":15,"14":17,"15":18};
    }

    for (let i = 0; i < 15; i++) {
        try {
            var rows = jsoncase.rows[i];

            for (let j = 0; j < 15; j++) {
                try {
                    var column = rows.columns[0][j]
                } catch {
                    var column = {}
                    rows.columns.push(column)
                }
            }
        } catch {
            var rows = {
                "row": i + 1,
                columns: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
            }
            if ("rows" in jsoncase) {
                jsoncase.rows.push(rows);
            } else {
                jsoncase.rows = [rows];
            }
        }
    }
    console.log(jsoncase);
}

// -----------------------------------------------------------
/**
 * Get the properties in the data at the position
 * @param {object} jsoncase - a case in the json format used to store in the db 
 * @param {string} position - formatted like A13 (letter, number)
 * @returns 
 */
function getProperties(jsoncase, position) {
    let splitpos = position.split(/(\d+)/)
    let col = splitpos[0].charCodeAt(0) - 65
    // now splitpos[0] will be the column and splitpos[1] will be the row
    try {
        var chardata = jsoncase.rows[splitpos[1] - 1].columns[col]
    }
    catch {
        var chardata = {
            "character": "",
            "style": "roman",
            "weight": "",
            "desc": "",
            "special": ""
        }
    }
    return chardata;
}

// -----------------------------------------------------------
/**
 * show the modal dialog when clicking in the matrix
 */
function clickMatrixHandler() {
    // Here, `this` refers to the element the event was hooked on
    var myModal = new bootstrap.Modal(document.getElementById('matrixModal'))
    myModal.show(this);
}

// -----------------------------------------------------------
/**
 * show the modal dialog when clicking in the unit
 */
function clickUnitHandler() {
    var myModal = new bootstrap.Modal(document.getElementById('unitModal'))
    myModal.show(this);
}

// -----------------------------------------------------------
/**
 * Save the data back into the jsoncase
 * @param {object} jsoncase - a case in the json format used to store in the db 
 * @param {string} position - formatted like A13 (letter, number)
 * @param {object} update - the new data to put back into the jsoncase
 */
function setProperties(jsoncase, position, update) {
    let splitpos = position.split(/(\d+)/);
    let col = splitpos[0].charCodeAt(0) - 65;

    update["column"] = col + 1
    update["columnname"] = splitpos[0]

    jsoncase.rows[splitpos[1] - 1].columns[col] = update;

    bootstrap.Modal.getInstance(document.getElementById('matrixModal')).hide();
    document.getElementById("matrixcase").innerHTML = '';
    generateTable(document.getElementById("matrixcase"), jsoncase);
    console.log(jsoncase);
    document.getElementById("savemca").disabled = false;
}

// -----------------------------------------------------------
/**
 * Save the unitdata back into the dictionary
 * @param {object} jsoncase - a case in the json format used to store in the db 
 * @param {number} row - the row that is being updated
 * @param {number} units - the new unit value
 */
function setUnitProperties(jsoncase, row, units) {
    console.log(units)
    console.log(row)
    jsoncase.units[row] = units;

    bootstrap.Modal.getInstance(document.getElementById('unitModal')).hide();
    document.getElementById("matrixcase").innerHTML = '';
    generateTable(document.getElementById("matrixcase"), jsoncase);
    document.getElementById("savemca").disabled = false;
}

// -----------------------------------------------------------
/**
 * Builds the table from the data dictionary that displays the case
 * @param {HTMLTableElement} table - the table element where the data is going
 * @param {object} jsoncase - a case in the json format used to store in the db 
 * @param {boolean} addlistener - do we add the eventlisters (ie editable or not)
 */
function generateTable(table, jsoncase, addlistener = true) {
    for (let i = 0; i < 17; i++) {
        let row = table.insertRow();

        for (let j = 0; j < 17; j++) {
            if (i == 0 || i == 16 || j == 0 || j == 16) {
                var coltype = document.createElement("th");
            } else {
                var coltype = document.createElement("td");
            }

            if (i == 0 || i == 16) {
                if (j > 0 && j < 16) {
                    var text = document.createTextNode(String.fromCharCode(65 + j - 1))
                } else {
                    var text = document.createTextNode("")
                }
            } else if (j == 16) {
                var text = document.createTextNode(i)
            } else if (j == 0) {
                var text = document.createTextNode(jsoncase.units[i])
                coltype.id = "unit" + i;
                if (addlistener) {
                    coltype.addEventListener("click", clickUnitHandler);
                }
            } else {
                nodeid = String.fromCharCode(65 + j - 1) + i
                chardata = getProperties(jsoncase, nodeid)
                if (chardata.character === undefined) {
                    var text = document.createTextNode("")
                } else {
                    var text = document.createTextNode(chardata.character)
                }
                if (chardata.style == "italic") {
                    coltype.style.fontStyle = "italic";
                    coltype.style.backgroundColor = "rgb(255, 230, 230)";
                } else if (chardata.style == "smallcap") {
                    coltype.style.fontVariant = "small-caps";
                    coltype.style.backgroundColor = "rgb(230, 255, 230)";
                }
                if (chardata.weight == "bold") {
                    coltype.style.fontWeight = "bold";
                }
                // style the cells
                switch (chardata.special) {
                    case 'quad':
                        coltype.style.backgroundColor = "rgb(200, 200, 200)";
                        break;
                    case 'sspace':
                        coltype.style.backgroundColor = "rgb(190, 190, 255)";
                        break;
                    case 'blank':
                        coltype.style.backgroundColor = "rgb(240, 240, 240)";
                        break;
                }
                coltype.id = nodeid;
                if (addlistener) {
                    coltype.addEventListener("click", clickMatrixHandler);
                }
            }
            coltype.appendChild(text);
            row.appendChild(coltype);
        }
    }
}



// -----------------------------------------------------------
/**
 * Check the case for problems
 * Jspace exists
 * Quad Exists
 * Any missing characters
 * @param {object} jsoncase - a case in the json format used to store in the db 
 * @returns {string} - a report on the validity of the case
 */
function validateMCA(jsoncase) {
    // this is really ugly and should be refactored...
    var sspace = false;
    var padding = false;
    var charmap = {};
    
    var errorreport = "";
    
    let lc_alphabet = "abcdefghijklmnopqrstuvwxyz";
    let uc_alphabet = lc_alphabet.toUpperCase();

    for (const row of jsoncase.rows) {
        for (const col of row.columns) {
            if (!(col.style in charmap)) {
                charmap[col.style] = [];
                charmap[col.style].push(col.character);
            } else {
                charmap[col.style].push(col.character);
                if (!sspace && col.special == "sspace") {
                    jspace = true;
                }
                if (!padding && col.special == "padding") {
                    padding = true;
                }
            }
        }
    }

    if (!sspace) {
        errorreport += "Missing S-Space<br>";
    }

    if (!padding) {
        errorreport += "Missing Padding Character<br>";
    }
    
    for (var key in charmap) {
        if (charmap.hasOwnProperty(key)) {
            charmap[key].sort();
            errorreport += "<b>Style: " + key + "</b><br>";
            lc_remainchar = lc_alphabet;
            uc_remainchar = uc_alphabet;
            previouschar = "";
            for (const c of charmap[key]) {
                lc_remainchar = lc_remainchar.replace(c, "");
                uc_remainchar = uc_remainchar.replace(c,"");
                if (c != "" && c != undefined && previouschar == c) {
                    errorreport += "Duplicate " + c + "<br>";
                }
                previouschar = c;
            }
            errorreport += "Missing LC characters: " + lc_remainchar + "<br>";
            errorreport += "Missing UC characters: " + uc_remainchar + "<br>";
        }
    }
    return errorreport;
}