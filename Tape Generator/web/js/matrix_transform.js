/**
 * Take a MCA in the normal json format and reorder it for easier searching
 * new format will be a object with [column, row, unitwidth]
 * {
 *  "roman" : {
 *     "A" : ['H', 13, 8],
 *     "B" : ['D', 3, 8],
 *      ...
 * },
 *  "italic" : {
 *     "a" : ['C', 14, 5],
 *      ...
 * }}
 * @param {object} jsoncase - case in the json format used to store in the db
 * @returns - new case in a format that makes searching easier
 */
function mcatransform_simplecase(jsoncase) {

    let simplecase = {};

    //store some fixed items
    simplecase["special"] = {};
    simplecase.special.units = jsoncase.units;
    //default set width if unknown
    if (jsoncase.setwidth == undefined || jsoncase.setwidth == null || jsoncase.setwidth == "" || jsoncase.setwidth == 0) {
        simplecase.special.setwidth = 10;
    } else {
        simplecase.special.setwidth = jsoncase.setwidth;
    }

    for (let row = 0; row < jsoncase.rows.length; row++) {
        for (let col = 0; col < jsoncase.rows[row].columns.length; col++) {
            let style = jsoncase.rows[row].columns[col].style;
            let columnname = jsoncase.rows[row].columns[col].columnname;
            // need to handle the stupid EF/D column depending on the matrix size
            // basically if any entry in the last row is na then it will be a 15x15 or 15x17
            if (columnname == "EF/D" && jsoncase.rows.length == 16) {
                for (let i = 0; i < jsoncase.rows[16-1].columns.length; i++) {
                    if (jsoncase.rows[16-1].columns[i].special == "na") {
                        columnname = "D";
                        break;
                    }
                }
            }
            // if we didn't replace EF/D with D then it must be an EF
            if (columnname == "EF/D") {
                columnname = "EF";
            }
            let rownumber = jsoncase.rows[row]["row"];
            let character = jsoncase.rows[row].columns[col].character;
            let special = jsoncase.rows[row].columns[col].special;
            // let padding = jsoncase.rows[row].columns[col].padding;
            // let unitshift = jsoncase.rows[row].columns[col].unitshift;
            let width = jsoncase.units[rownumber];
            // store the special characters (as need to know the jspace and quad)
            if (special != null && special != "" && special != "blank") {
                simplecase["special"] = simplecase["special"] || {}; // create special if does not exist
                // only store the first occurrence of a low-space space
                if (special == 'lowspace') {
                    if (!("lowspace" in simplecase.special)) {
                        simplecase["special"][special] = [columnname, rownumber, width];
                    }
                } else {
                    // store everything else
                    simplecase["special"][special] = [columnname, rownumber, width];
                }
            } else {
                // characters
                if (character != undefined && character != null && character != "" && special != "blank") {
                    simplecase[style] = simplecase[style] || {}; //create the style if it does not exist
                    simplecase[style][character] = [columnname, rownumber, width];
                }
            }
            if (jsoncase.rows[row].columns[col].padding) {
                simplecase["special"]["padding"] = [columnname, rownumber, width];
            }
        }
    }

    console.log(simplecase);
    return simplecase;
}