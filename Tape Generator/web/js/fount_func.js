// Functions for generating a fount for a case (ie lots of individual characters)

// globals
// const ONE_UNIT_OF_ONE_SET = 0.0007685; //inches
// const SIG_0005 = 0.0005; //width of a 0005 signal
// const SIG_0075 = 0.0075; //width of a 0007 signal
// const SIZE_MULTIPLIER = 12;
// const LOWERLIMIT_SPACE = 4;
// const NORMAL_SPACE = 6;


// ------------------------------------------------------------
/**
 * Convert a huge list of characters into punch tape
 * @param {array} fount_string - an string of characters to cast
 * @param {number} galleywidth_mm - the width of the galley in mm
 * @param {object} simplecase - This is the matrix case (resulting from mcatransform)
 * @param {string} style - the style of the text
 * @param {boolean} pad - do we want the line padded with quads
 * @param {boolean} justifytext - do we want to full justify (or ragged right)
 * @returns tape
 */
function fount_generator(fount_string, galleywidth_mm, simplecase, style = "roman", pad = false) {

    let linewidth = mm2picas(galleywidth_mm);
    let units_of_set_per_line = linewidth * 12 * 18 / simplecase.special.setwidth
    console.log("Line Width: "+linewidth);
    console.log("Units of Set Per Line: "+units_of_set_per_line);
    
    let tape = "";

    // quads, jspaces and spaces must exist
    if (!("padding" in simplecase.special) || !("sspace" in simplecase.special)) {
        console.log("No padding, sspace or lowspace found");
        return "! No padding or sspace found";
    } else {
        var padding_column = simplecase.special.padding[0];
        var padding_row = simplecase.special.padding[1];
        var padding_width = simplecase.special.padding[2];
        var sspace_column = simplecase.special.sspace[0];
        var sspace_row = simplecase.special.sspace[1];
    }

    if (pad) {
        // to make life easier for the person casting the galley we are going to pad each line
        // with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        // need to subtract this from the galley width
        units_of_set_per_line -= 4 * padding_width;
    }

    // some variables that we will use
    let usedline = 0; // how much of the line have we used?
    let missing_chars = ""; // how many missing characters did we hit?
    let numspaces = 0; // track the number of spaces in a line

    // loop though all the characters provided
    for (let i = 0; i < fount_string.length; i++) {

        let the_char = fount_string[i]
        let chardata = simplecase[style][the_char] || [null, null, null];
        let charwidth = chardata[2]
        //chardata contains the position and width (the width is chardata[2])

        // did we find the character?
        if (chardata[0] == null) {
            if (missing_chars.slice(-1) != the_char) missing_chars += the_char
            continue
        }

        // are we at the beginning of the line?
        if (usedline == 0) {
            if (pad) { //Cast the initial 2 quads
                tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
            }
        }

        // can we fit this character into the line?
        if (usedline + charwidth < units_of_set_per_line) {
            // yes we can.
            tape += tape_draw(chardata[0].split("").concat([chardata[1]]),the_char);
            usedline += charwidth

        } else {
            // pad out the left over line with spaces, we do need at least one
            while (usedline < units_of_set_per_line) {
                tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "SSpace");
                numspaces += 1
                usedline += LOWERLIMIT_SPACE
            }
            
            //cast the quads at the end of the line
            if (pad) {
                tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
            }
            
            tape += galley_justifyspaces(units_of_set_per_line - usedline, numspaces);

            usedline = 0
            numspaces = 0
            // decrement the counter so that this character will be processed again
            i--;
        }
    }

    // we are out of characters, so end the paragraph.
    // Only need to do this if the line has words on it
    if (usedline != 0) {
        console.log("End of paragraph: Padding with PAD and s-spaces");

        // need to pad the remaining line with quads and spaces then justify
        while (usedline + padding_width + LOWERLIMIT_SPACE <= units_of_set_per_line) {
            // add as many quads as we can to fill
            tape += tape_draw([padding_column, padding_row],"PAD", "Buffering Pad");
            usedline += padding_width;
            console.log(usedline);
        }

        while (usedline + LOWERLIMIT_SPACE <= units_of_set_per_line) {
            // add as many justification spaces as we can to fill

            tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "Padding SSpace");
            usedline += LOWERLIMIT_SPACE
            numspaces += 1
        }

        // add two quads at the end
        if (pad) {
            tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
            tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
        }
    
        // now justify
        tape += galley_justifyspaces(units_of_set_per_line - usedline, numspaces);
    }
    if (missing_chars.length != 0) {
        tape += `! Missing Chars from Fount: ${missing_chars.length} = "${missing_chars}"`;
    }
    
    return tape;
}
