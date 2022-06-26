// Useful Functions when dealing with the tape

// ---------------------------------------------------------
/**
 * Draw the codes suitable for punching
 * @param {array} codes - a List of the punch codes to punch on this line
 * @param {string} the_char - optional text to printout on the line
 * @param {string} commenttext - optional text to printout on the line
 * @param {string} end - the line end
 * @returns {string} - |----------o------------o-------| 'the_char' [codes] comment end
 */
function tape_draw(codes, the_char = "", commenttext = "", end = "\n") {

    function setCharAt(str,index,chr) {
        // replace a character at a specific position
        if (index >= str.length || index < 0) return str;
        return str.substring(0,index) + chr + str.substring(index+1);
    }

    const punchpositions = ['N','M','L','K','J','I','H','G','F','S','E','D','0075','C','B','A','1','2','3','4','5','6','7','8','9','10','11','12','13','14','0005'];
    let fullline = "-------------------------------"; // 31 hyphens

    for (code of codes) {
        pos = punchpositions.indexOf(code.toString());
        fullline = setCharAt(fullline,pos,"o");
    }

    // build the line
    let line = "|" + fullline + "|";

    if (the_char != "") {line += " " + the_char;}

    //display the code
    line += " (" + codes.join() + ")";
    line += " " + commenttext + end;
    
    return line;
}


// ---------------------------------------------------------
/**
 * Calculate the amount of roll required
 * 
 * @param {number} length_mm - the length of the tape required (mm)
 * @returns {number} - the diameter of roll (mm)
 */
function tape_roll_amount(length_mm) {
    
    /*
    L = length of material
    t = thickness
    D = outside diameter
    d = hole diameter

    pi(D*D - d*d)/4 = L t
    L = pi(D*D - d*d)/4t
    D = SQRT((L4t/pi)+d*d)
    */

    const PAPER_THICKNESS_MM = 0.08;
    const CORE_DIAMETER_MM = 22;

    let L = length_mm
    let t = PAPER_THICKNESS_MM
    let d = CORE_DIAMETER_MM

    let D = Math.sqrt((L*4*t/Math.PI)+d*d)
    return D
}

// ----------------------------------------------
/**
 * Print the stop casting commands.
 * Also dumps a couple of extra quads to physically stop the caster
 * 
 * @param {object} simplecase - This is the matrix case (resulting from mcatransform)
 * @return {string} - The commands to stop casting
 */
function stop_casting(simplecase) {
    if (!("padding" in simplecase.special)) {
        console.log("No padding quads found");
        return "! No padding quads found\n";
    } else {
        var padding_column = simplecase.special.padding[0];
        var padding_row = simplecase.special.padding[1];
    }
    let tape = "";
    tape += tape_draw(['0005'], "0005", "Caster Stopping");
    tape += tape_draw(['0005','0075'], "0005/0075", "Caster Stopping");
    tape += tape_draw([padding_column, padding_row], "QUAD", "Caster Stopping");
    tape += tape_draw([padding_column, padding_row], "QUAD", "Caster Stopping");
    return tape;
}

