const column_names = ["NI","NL","A","B","C","EF/D","E","F","G","H","I","J","K","L","M","N","O"]
const row_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

// -----------------------------------------------------------
/**
 * Ensure that we have the right size
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
        jsoncase.units = {"1":5,"2":6,"3":7,"4":8,"5":9,"6":9,"7":10,"8":10,"9":11,"10":12,"11":13,"12":14,"13":15,"14":17,"15":18, "16":0};
    }
    
    for (let i = 0; i < row_numbers.length; i++) {
        try {
            var rows = jsoncase.rows[i];

            for (let j = 0; j < column_names.length; j++) {
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
                columns: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
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
    let splitpos = position.split(/(\d+)/);
    let col = splitpos[0];
    //console.log("getProperties: "+splitpos);
    var chardata = null;

    // rewrite to perform a search rather than absolute address
    var coldata = jsoncase.rows[splitpos[1] - 1].columns;

    for (let i=0; i < coldata.length; i++) {
        if (coldata[i].columnname == col) {
            chardata = coldata[i];
            break;
        } else if ((col == "EF" || col == "EF/D" || col == "D") && (coldata[i].columnname == "EF" || coldata[i].columnname == "EF/D" || coldata[i].columnname == "D")) {
            chardata = coldata[i];
            break;
        }
    }
    
    if (chardata == null) {
        chardata = {
            "character": "",
            "style": "roman",
            "weight": "",
            "desc": "",
            "unitshift": false,
            "padding": false,
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
    let col = splitpos[0];
    let col_pos_index = -1;
    console.log(splitpos);
    if (col == "EF" || col == "D" || col == "EF/D") {
        col = "EF/D"
        col_pos_index = 5;
    } else {
        col_pos_index = column_names.indexOf(col);
    }

    update["column"] = col_pos_index
    update["columnname"] = column_names[col_pos_index]

    //jsoncase.rows[splitpos[1] - 1].columns[col_pos_index] = update;

    // rewrite to perform a search rather than absolute address
    let didweupdate = false;
    var coldata = jsoncase.rows[splitpos[1] - 1].columns;
    for (let i=0; i < coldata.length; i++) {
        if (coldata[i].columnname == col || (col == "EF/D" && (coldata[i].columnname == "EF" || coldata[i].columnname == "D"))) {
            jsoncase.rows[splitpos[1] - 1].columns[i] = update;
            didweupdate = true;
            break;
        } 
    }
    if (!didweupdate) {
        //if the position exists, update this
        if (Object.keys(jsoncase.rows[splitpos[1] - 1].columns[col_pos_index]).length === 0) {
            jsoncase.rows[splitpos[1] - 1].columns[col_pos_index] = update;
        } else {
            jsoncase.rows[splitpos[1] - 1].columns.push(update);
        }
    }


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
    if (parseInt(units) == NaN) {
        jsoncase.units[row] = 0;
    } else {
        jsoncase.units[row] = parseInt(units);
    }

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

    const numrows = row_numbers.length+2;
    const numcols = column_names.length+2;

    for (let i = 0; i < numrows; i++) {
        let row = table.insertRow();

        for (let j = 0; j < numcols; j++) {
            if (i == 0 || i == numrows-1 || j == 0 || j == numcols-1) {
                var coltype = document.createElement("th");
            } else {
                var coltype = document.createElement("td");
            }

            if (i == 0 || i == numrows-1) {
                if (j > 0 && j < numcols-1) {
                    var text = document.createTextNode(column_names[j-1])
                } else if (j == 0) {
                    var text = document.createTextNode("UNIT");
                    coltype.className = "unit_title";
                } else {
                    var text = document.createTextNode("")
                }
            } else if (j == numcols-1) {
                var text = document.createTextNode(i)
            } else if (j == 0) {
                var text = document.createTextNode(jsoncase.units[i])
                coltype.id = "unit" + i;
                coltype.className = "unit";
                if (addlistener) {
                    coltype.addEventListener("click", clickUnitHandler);
                }
            } else {
                nodeid = column_names[j-1] + i
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
                if (chardata.unitshift) {
                    coltype.style.borderTop = "solid 3px black";
                }
                switch (chardata.special) {
                    case 'quad':
                        coltype.style.backgroundColor = "rgb(200, 200, 200)";
                        break;
                    case 'sspace':
                        coltype.style.backgroundColor = "rgb(190, 190, 255)";
                        break;
                    case 'blank':
                    case 'lowspace':
                        coltype.style.backgroundColor = "rgb(240, 240, 240)";
                        break;
                    case 'na':
                        coltype.style.backgroundImage = `
                        repeating-linear-gradient(
                            45deg,
                            #AAAAAA,
                            #AAAAAA 10px,
                            #CCCCCC 10px,
                            #CCCCCC 20px)`;
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
            let stylecombined = col.style + "-" + col.weight;
            // don't validate undefined styles
            if (stylecombined.indexOf("undefined") == -1) {
                if (!(stylecombined in charmap)) {
                    charmap[stylecombined] = [];
                    charmap[stylecombined].push(col.character);
                } else {
                    charmap[stylecombined].push(col.character);
                }
            }
            if (!sspace && col.special == "sspace") {
                sspace = true;
            }
            if (!padding && col.padding) {
                padding = true;
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