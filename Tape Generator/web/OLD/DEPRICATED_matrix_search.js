// Utilities for dealing with the matrix case

// ------------------------------------------------------------
function get_char(mcase, the_char_to_find, the_style_to_find) {
    // Search the case for the character.
    // Returns an array of two items [col, row]
    for (let row = 0; row < mcase.rows.length; row++) {
        for (let col = 0; col < mcase.rows[row].columns.length; col++) {
            if (mcase.rows[row].columns[col].character == the_char_to_find && mcase.rows[row].columns[col].style == the_style_to_find) {
                return [col, row];
            }
        }
    }
    return [null,null]; // could not find
}

// ------------------------------------------------------------
function get_char_matrixcoord(mcase, the_char_to_find, the_style_to_find) {
    // Search the case for the character.
    // Returns an array of two items [col, row]
    // Return is in the matrix cordinates (eg alphabetical column and numerical row)
    let columns = "ABCDEFGHIJKLMNO"
    let pos = get_char(mcase, the_char_to_find, the_style_to_find);
    if (pos[0] != null) {
        return [columns.charAt(pos[0]), pos[1]+1]
    }
    return pos; // will be [null,null] if not found
}

// ------------------------------------------------------------
function get_quad(mcase) {
    // Search the case for the quad character
    for (let row = 0; row < mcase.rows.length; row++) {
        for (let col = 0; col < mcase.rows[row].columns.length; col++) {
            if (mcase.rows[row].columns[col].special == "quad") {
                return [col, row];
            }
        }
    }
    return [null,null]; // could not find
}

// ------------------------------------------------------------
function get_quad_matrixcode(mcase) {
    // Search the case for the quad character
    let columns = "ABCDEFGHIJKLMNO";
    let pos = get_quad(mcase);
    if (pos[0] != null) {
        return [columns.charAt(pos[0]), pos[1]+1]
    }
    return pos;
}

// ------------------------------------------------------------
function get_jspace(mcase) {
    // Search the case for the justification space
    for (let row = 0; row < mcase.rows.length; row++) {
        for (let col = 0; col < mcase.rows[row].columns.length; col++) {
            if (mcase.rows[row].columns[col].special == "jspace") {
                return [col, row];
            }
        }
    }
    return [null,null]; // could not find
}

// ------------------------------------------------------------
function get_jspace_matrixcode(mcase) {
    // Search the case for the quad character
    let columns = "ABCDEFGHIJKLMNO";
    let pos = get_jspace(mcase);
    if (pos[0] != null) {
        return [columns.charAt(pos[0]), pos[1]+1]
    }
    return pos; // will be [null, null] if not found
}

// ------------------------------------------------------------
function get_width(mcase, position_yx) {
    // Return the unit width of the row
    // position_yx is an array [y, x] returned from get_char
    if (position_yx[1] != null) {
        return mcase.units[position_yx[1]+1];
    }
    return null;
}

// ------------------------------------------------------------
function get_width_matrixcoord(mcase, position_yx) {
    // Return the unit width of the row
    // position_yx is an array [y, x] returned from get_char_matrixcoords
    if (position_yx[1] != null) {
        return mcase.units[position_yx[1]];
    }
    return null;
}