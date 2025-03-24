// Functions related to the Galley

// Note, tape_func.js must be imported before this can be used.

// globals
const ONE_UNIT_OF_ONE_SET = 0.0007685; //inches
const SIG_0005 = 0.0005; //width of a 0005 signal
const SIG_0075 = 0.0075; //width of a 0007 signal
const SIZE_MULTIPLIER = 12;
const LOWERLIMIT_SPACE = 4;
const NORMAL_SPACE = 6;

// ----------------------------------------------------------
/**
 * Convert mm to pica (default pica is 0.1660 (New British Pica)
 * @param {number} mm - the mm length
 * @param {number} pica - the size of the pica (default 0.1660)
 * @returns - number of picas
 */
function mm2picas(mm, pica = 0.1660) {
    return Math.round(mm/25.4/pica)
}

// ----------------------------------------------------------
/**
 * Convert pica to mm (default pica is 0.1660 (New British Pica)
 * @param {number} pica - the mm length
 * @param {number} picasize - the size of the pica (default 0.1660)
 * @returns - number of picas
 */
function picas2mm(pica, picasize = 0.1660) {
    return Math.round(pica * 25.4 * picasize)
}


// ----------------------------------------------------------
/**
 * Calculate the word width (excluding any spaces)
 * @param {string} word 
 * @param {object} simplecase 
 * @param {string} style 
 * @returns {number}
 */
function galley_wordwidth(word, simplecase, style = "roman") {
    let width = 0;
    for (let the_char of word) {
        chardata = simplecase[style][the_char] || [null, null, null];
        //special case for hyphen, revert to roman if not found
        if (the_char == "-" && chardata[2] == null){
            chardata = simplecase["roman"]["-"] || [null, null, null];
        }
        //special case for padding
        if (the_char == "█") {
            chardata = simplecase.special.padding || [null, null, null];
        }
        if (chardata[2] != null) {
            width += chardata[2];
        } else {
            console.log(`Character ${the_char} not found - skipping....`);
        }
    }
    return width;
}

// ----------------------------------------------------------
/**
 * Split up the word 
 * If the word contains control characters, need to split this up
 * into individual characters and relevant styles
 * if "T<sc>est</sc>" then this would be split into 
 * [['T','roman'],['e','smallcap'],['s','smallcap'],['t','smallcap']]
 * @param {string} word 
 * @returns {object}
 */
function splitupaword(word) {
    //TODO - need to implement this

    //Problem is that then need to reimplement all the hypernation
    //code to support this too... sigh
}

// ----------------------------------------------------------
/**
 * Calculate the word width (excluding any spaces)
 * In this case 'word' is an array of characters and styles
 * something like [['A','roman'],['B','italic'],['C','smallcap']]
 * @param {object} word 
 * @param {object} simplecase 
 * @returns {number}
 */
function galley_splitwordwidth(word, simplecase) {
    let width = 0;
    for (let the_char of word) {
        chardata = simplecase[style[1]][the_char[0]] || [null, null, null];
        //special case for hyphen, revert to roman if not found
        if (the_char == "-" && chardata[2] == null){
            chardata = simplecase["roman"]["-"] || [null, null, null];
        }
        //special case for padding
        if (the_char == "█") {
            chardata = simplecase.special.padding || [null, null, null];
        }
        if (chardata[2] != null) {
            width += chardata[2];
        } else {
            console.log(`Character ${the_char} not found - skipping....`);
        }
    }
    return width;
}

// --------------------------------------------------------------------
/**
 * Draw the justification spaces.
 * This is always two lines on the final tape
 * @param {number} total_space_remaining - the units of set that is remaining in the line (ie unset)
 * @param {number} numspaces - the number of spaces used on that line
 * @returns {string} - the tape commands
 */
function galley_justifyspaces(total_space_remaining, numspaces) {

    console.log(`Justification - Unset Units: ${total_space_remaining}, ${numspaces} spaces`);

    let tape = "";

    if (total_space_remaining > 0 && numspaces > 0) {
        if (numspaces > 0) {
            var interword_space = total_space_remaining / numspaces;
        } else {
            var interword_space = 0;
        }

        var units_of_set_to_add_to_spaces = interword_space + LOWERLIMIT_SPACE - NORMAL_SPACE;
        console.log(`Units of Set to add to ${numspaces} j-spaces: ${units_of_set_to_add_to_spaces}`);

        var total_required_0005_steps = Math.round(units_of_set_to_add_to_spaces * SIZE_MULTIPLIER * (ONE_UNIT_OF_ONE_SET/SIG_0005));
        console.log(`total_required_0005_steps: ${total_required_0005_steps} = round(${units_of_set_to_add_to_spaces} * ${SIZE_MULTIPLIER} * ${ONE_UNIT_OF_ONE_SET/SIG_0005})`);
        
        if (total_required_0005_steps + 53 <= 16 || total_required_0005_steps + 53 >= 240) {
            console.log("total_required_0005_steps: " + total_required_0005_steps)
            console.log("Error, can't justify this amount");
            tape += "! Tape Error - can't justify " + total_required_0005_steps + " 0005 steps!\n";
            return tape;
        };

        var justification_0075 = Math.floor((total_required_0005_steps + 53) / 15);
        var justification_0005 = (total_required_0005_steps + 53) % 15;
        console.log(`Justification: (${total_required_0005_steps} + 53) / 15 = ${justification_0075}/${justification_0005}`);

        let comment = `Unset: ${total_space_remaining.toFixed(1)}, Units to ${numspaces} j-spaces: ${units_of_set_to_add_to_spaces.toFixed(1)}, req_0005_steps: ${total_required_0005_steps} = round(${units_of_set_to_add_to_spaces.toFixed(1)} * ${SIZE_MULTIPLIER} * ${ONE_UNIT_OF_ONE_SET/SIG_0005})`;
        tape += tape_draw(['0075',justification_0075], "0075", comment);

        comment = `Justification: (${total_required_0005_steps} + 53) / 15 = ${justification_0075}/${justification_0005}`;
        tape += tape_draw(['0005','0075', justification_0005], "0005/0075", comment);


    } else {
        // 1/1 justification
        console.log("1/1 Justification");
        tape += tape_draw(['0075', "1"], "0075", "1/1 justification - unset="+total_space_remaining+" spaces="+numspaces);
        tape += tape_draw(['0005','0075', "1"], "0005/0075", "1/1 justification")
    }

    return tape;
}

// --------------------------------------------------------------------
/**
 * Generate a line seperator of quads
 * @param {object} simplecase - the simplifed case layout
 * @param {number} galleywidth - the width of the galley
 * @param {boolean} pad - do we want the line padded with quads
 * @returns {array} - tape
 */
function galley_separator(simplecase, galleywidth_mm, pad = false) {

    let usedline = 0 // how much of the line have we used?
    let numspaces = 0 // how many spaces have we used?

    let linewidth = mm2picas(galleywidth_mm);
    let units_of_set_per_line = linewidth * 12 * 18 / simplecase.special.setwidth

    let tape = "";

    // quads and jspaces must exist
    if (!("quad" in simplecase.special) || !("jspace" in simplecase.special)) {
        console.log("No quad or jspace found");
        return "! No quad or jspace";
    } else {
        var padding_column = simplecase.special.quad[0];
        var padding_row = simplecase.special.quad[1];
        var quad_width = simplecase.special.quad[2];
        var sspace_column = simplecase.special.jspace[0];
        var sspace_row = simplecase.special.jspace[1];
    }

    if (pad) {
        // to make life easier for the person casting the galley we are going to pad each line
        // with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        units_of_set_per_line -= 4 * quad_width;
        // cast the initial padding quads
        tape += tape_draw([padding_column, padding_row],"QUAD", "Padding Quad");
        tape += tape_draw([padding_column, padding_row],"QUAD", "Padding Quad");
    }

    while (usedline + quad_width + LOWERLIMIT_SPACE <= units_of_set_per_line) {
        // add as many quads as we can to fill
        tape += tape_draw([padding_column,padding_row], "QUAD", "Separator Quad");
        usedline += quad_width;
    }

    while (usedline + LOWERLIMIT_SPACE <= units_of_set_per_line) {
        // add as many justification spaces as we can to fill
        tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "Padding JSpace");
        usedline += LOWERLIMIT_SPACE;
        numspaces += 1;
    }

    if (pad) {
        tape += tape_draw([padding_column, padding_row],"QUAD", "Padding Quad");
        tape += tape_draw([padding_column, padding_row],"QUAD", "Padding Quad");
    }

    // now justify
    tape += galley_justifyspaces(units_of_set_per_line - usedline, numspaces);

    return tape;
}


// ------------------------------------------------------------
/**
 * Convert a paragraph of text into punch tape
 * @param {array} paragraph - an array of paragraphs of strings to cast
 * @param {number} galleywidth_mm - the width of the galley in mm
 * @param {object} simplecase - This is the matrix case (resulting from mcatransform)
 * @param {string} style - the style of the text
 * @param {boolean} pad - do we want the line padded with quads
 * @param {boolean} justifytext - do we want to full justify (or ragged right)
 * @returns tape
 */
function paragraph_generator(paragraph_array, galleywidth_mm, simplecase, style = "roman", pad = false, hyphenatetext = false, justifytext = true) {

    const initialstyle = style;
    const initialjustification = justifytext;

    if (paragraph_array == undefined || paragraph_array == null || paragraph_array.length == 0) {
        console.log("paragraph_array Error");
        return "! Paragraph Error";
    }

    let linewidth = mm2picas(galleywidth_mm);
    let units_of_set_per_line = linewidth * 12 * 18 / simplecase.special.setwidth
    console.log("Line Width: "+linewidth);
    console.log("Units of Set Per Line: "+units_of_set_per_line);
    
    let tape = "";

    // quads and jspaces must exist
    if (!("padding" in simplecase.special) || !("sspace" in simplecase.special)) {
        console.log("No padding or sspace found");
        return "! No padding or sspace found";
    } else {
        var padding_column = simplecase.special.padding[0];
        var padding_row = simplecase.special.padding[1];
        var padding_width = simplecase.special.padding[2];
        var sspace_column = simplecase.special.sspace[0];
        var sspace_row = simplecase.special.sspace[1];
    }

    // if we are not justifing then spaces must exist
    if (!justifytext && !("lowspace" in simplecase.special)) {
        console.log("No lowspace space found");
        return "! No lowspace space found";
    } else {
        var normal_space_column = simplecase.special.lowspace[0];
        var normal_space_row = simplecase.special.lowspace[1];
        console.log("Normal Space " + normal_space_column + normal_space_row)
    }

    if (pad) {
        // to make life easier for the person casting the galley we are going to pad each line
        // with four quads (2 at beginning and end), this helps to ensure that the sorts don't fall over
        units_of_set_per_line -= 4 * padding_width;
    }

    // loop though all the text provided
    for (let pcounter = 0; pcounter < paragraph_array.length; pcounter++) {
        
        //current paragraph
        let paragraph = paragraph_array[pcounter];
        // some variables that we will use
        let usedline = 0; // how much of the line have we used?
        let missing_chars = ""; // how many missing characters did we hit?
        let numspaces = 0; // track the number of spaces in a line
        let wordwidth = 0;

        // clean up the paragraph
        // replace all the &gt; and &lt; with the actual characters
        paragraph = paragraph.replace(/&gt;/g, ">");
        paragraph = paragraph.replace(/&lt;/g, "<");
        // remove all new lines and replace with a placeholder
        paragraph = paragraph.replace(/\r?\n|\r/g, "💩");
        console.log(paragraph);
        // remove any spaces before or after the placeholder
        paragraph = paragraph.replace(/\s*💩\s*/g, "💩");
        console.log(paragraph);
        // replace the placeholder with a space
        paragraph = paragraph.replace(/💩/g, " ");
        // set the justiification
        if (paragraph.startsWith("<j>")) {
            justifytext = true;
            paragraph = paragraph.slice(3);
        } else if (paragraph.startsWith("<lj>")) {
            justifytext = false;
            paragraph = paragraph.slice(4);
        } else {
            justifytext = initialjustification;
        }
        console.log(paragraph);


        // split the paragraph into words (on the space)
        let words = paragraph.trim().split(' ');
        //note that — is an em-dash (ie U+2014)
        //let words = paragraph.match(/[^\s—]+—?/g);
        // TODO - need better logic around how to split on text that contains em dash as the moby-dick
        // sample text with galley width 100mm exhibits problems where it hyphenates a word with an em-dash

        console.log("Begin Paragraph: Justification = " + justifytext)

        let i = 0; // this is a pointer to the word we are up to
        while (i < words.length) {
            
            var word = words[i]

            //store the full word as we will need to use this as it may contain command codes
            var fullword = word

            console.log(fullword);
            // need to ensure that the whole word will fit on the line
            // if there are already words in the line then ensure a space
            // is prepended
            if (usedline == 0) {
                wordwidth = 0
                if (pad) { //Cast the initial 2 quads
                    tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                    tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                }
            } else {
                wordwidth = LOWERLIMIT_SPACE;
            }

            //handle some really basic HTML to change the word styles
            if (word.startsWith("<i>")) {
                style = "italic";
                word = word.slice(3);
            } else if (word.startsWith("<sc>")) {
                style = "smallcap";
                word = word.slice(4);
            } else if (word.startsWith("<r>")) {
                style = "roman";
                word = word.slice(3);
            }

            //we will need to return to the base style at the end of the word
            if (word.endsWith("</i>")) {
                word = word.slice(0,-4);
            } else if (word.endsWith("</sc>")) {
                word = word.slice(0,-5);
            } else if (word.endsWith("</r>")) {
                word = word.slice(0,-4);
            }

            //if user has forgotton to cap the small cap, fix it for them
            if (style == "smallcap") {
                word = word.toUpperCase();
            }

            // loop though the word
            


            wordwidth += galley_wordwidth(word, simplecase, style);

            // can we fit this word (and maybe the space) into the line?
            if (usedline + wordwidth < units_of_set_per_line) {
                if (usedline != 0) {
                    if (justifytext) {
                        tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "SSpace");
                        numspaces += 1
                    } else {
                        tape += tape_draw([' ',normal_space_column,normal_space_row], "SPACE", "Low Space");
                        // don't increase the numspaces when not performing justification
                    }
                }
                for (let the_char of word) {
                    let pos = simplecase[style][the_char] || [null, null, null];
                    //special case for hyphen, revert to roman if not found
                    if (the_char == "-" && pos[2] == null){
                        pos = simplecase["roman"]["-"] || [null, null, null];
                    }
                    //special case for quads
                    if (the_char == "█") {
                        pos = simplecase.special.padding || [null, null, null];
                    }
                    if (pos[0] == null) {
                        missing_chars += the_char;
                    } else {
                        // handle multiple punch requirements by splitting (ie EF, NI, NL)
                        tape += tape_draw(pos[0].split("").concat([pos[1]]),the_char);
                    }
                }
                usedline += wordwidth
                // increment word counter
                i += 1
            

            // what about if we hyphenate, can we fit the hyphenated word?
            // } elif Utils.besthyphenation(word,self.case,self.wedge,style,units_of_set_per_line-usedline-self.lowerlimit_space)[0] != "":
            } else if (hyphenatetext && besthyphenation(word, units_of_set_per_line-usedline-LOWERLIMIT_SPACE, simplecase, style)[0] != "") {
                console.log(`Space remaining on line ${Math.round(units_of_set_per_line-usedline-LOWERLIMIT_SPACE)} (picas)`);
                console.log(`'${word}' too big (${galley_wordwidth(word, simplecase, style)} picas)`);
                let hypenation_options = besthyphenation(word, units_of_set_per_line-usedline-LOWERLIMIT_SPACE, simplecase, style);
                wordwidth = galley_wordwidth(hypenation_options[0], simplecase, style);
                console.log(`Using hyphenation: '${hypenation_options[0]}' (${wordwidth} picas) and '${hypenation_options[1]}' (${galley_wordwidth(hypenation_options[1], simplecase, style)} picas)`);
                
                if (usedline != 0) {
                    // draw a space before adding the word
                    if (justifytext) {
                        tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "SSpace");
                        numspaces += 1
                    } else {
                        tape += tape_draw([' ',normal_space_column,normal_space_row], "SPACE", "Low Space");
                    }
                }
                for (let the_char of hypenation_options[0]) {
                    let pos = simplecase[style][the_char] || [null, null, null];
                    //special case for hyphen, revert to roman if not found
                    if (the_char == "-" && pos[2] == null){
                        pos = simplecase["roman"]["-"] || [null, null, null];
                    }
                    if (pos[0] == null) {
                        missing_chars += the_char;
                    } else {
                        tape += tape_draw([pos[0],pos[1]],the_char);
                    }
                }
                usedline += wordwidth
                // replace the current word with the hypenation and don't increament the counter
                words[i] = hypenation_options[1]

            // no hyernation options and can't fit, justify the line, put the word on the newline
            // TODO - what if the word is too long to fit on a line at all?
            } else {
                // we need at least one justification space at the end for ragged right
                tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "SSpace");
                numspaces += 1
                // TODO - Problem is that what about if a single justification space is too small?
                // we might need a couple of spaces to allow them to expand enough to fill the line.
                if (!justifytext) {
                    //this is a horrible hack
                    console.log("Hack to add spaces for Ragged Right");
                    while (galley_justifyspaces(units_of_set_per_line - usedline, numspaces).endsWith("!\n")) {
                        tape += tape_draw(['S',sspace_column,sspace_row], "SPACE", "SSpace");
                        numspaces += 1
                    }
                }
                //cast the quads at the end of the line
                if (pad) {
                    tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                    tape += tape_draw([padding_column, padding_row],"PAD", "Padding");
                }
                
                tape += galley_justifyspaces(units_of_set_per_line - usedline, numspaces);

                usedline = 0
                numspaces = 0
                // don't increment the word counter (so the current word
                // will be processed again on the new line)
            }

            //do we need to revert the style?
            if (new RegExp("<\/.+>$").test(fullword)) {
                style = initialstyle
            }
        }
        
        // we are out of words, so end the paragraph.
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
            tape += `! Missing Chars from Paragraph: ${missing_chars.length} = "${missing_chars}\n"`;
        }
    }
    return tape;
};


// ----------------------------------------------------------
/**
 * Find the longest option for hyphenation into the available space (ie minimise
 * the justification spaces required)
 * Note that trie is a global variable built when hypher imported.
 * @param {array} wordlist - a list of the ways you can breakup a word (eg ['hy', 'phen', 'ation'])
 * @param {number} remainingspace - the amount of space available to try and fit the word into
 * @param {object} simplecase - This is the matrix case (resulting from mcatransform)
 * @param {string} style - the style of the word
 * @returns 
 */
function besthyphenation(word, remainingspace, simplecase, style) {

    hyp_options = hyphenate(word);
    console.log("Hyphenation Options: "+hyp_options);
    if (hyp_options.length > 1) {
        return _besthyphenation(hyp_options, remainingspace, simplecase, style);
    } else {
        return ["", hyp_options[0]];
    }
}

// ----------------------------------------------------------
/**
 * Recursively find the longest option for hyphenation into the available space
 * @param {array} wordlist - a list of the ways you can breakup a word (eg ['hy', 'phen', 'ation'])
 * @param {number} remainingspace - the amount of space available to try and fit the word into
 * @param {object} simplecase - This is the matrix case (resulting from mcatransform)
 * @param {string} style - the style of the word
 * @returns 
 */
function _besthyphenation(wordlist, remainingspace, simplecase, style) {

    if (wordlist.length > 1) {
        //theword = ''.join(wordlist[:-1]) + "-"
        let theword = wordlist.slice(0,-1).join('') + "-";
        //console.log(`Testing Hypenation of Word: ${theword}, ${galley_wordwidth(theword, simplecase, style)}`);
        if (galley_wordwidth(theword, simplecase, style) <= remainingspace) {
            return [theword, wordlist.pop()];
        } else {
            new_wordlist = wordlist.slice(0,-2);
            new_wordlist.push(wordlist.slice(-2).join(''));
            //console.log(new_wordlist);
            //#print(new_wordlist)
            //#print(wordlist[:-2].append(''.join(wordlist[-2:])))
            return _besthyphenation(new_wordlist, remainingspace, simplecase, style);
        }
    } else {
        return ["", wordlist[0]];
    }
}

// ----------------------------------------------------------
/**
 * When in poetry mode, calculate the width of the galley based on the longest
 * line in the poem
 * @param {array} lines - an array of the lines in the poem
 * @returns 
 */
function calculate_galley_width(lines, simplecase, style = "roman", pad = false) {
    let longestline = "";
    for (let line of lines) {
        if (line.length > longestline.length) {
            longestline = line
        }
    }
    console.log("Longest Line: " + longestline)

    //Now how wide is the longest line?
    let length = 0;
    let words = longestline.trim().split(' ');
    for (let i = 0; i < words.length; i++) {
        length += galley_wordwidth(words[i], simplecase, style);
        length += LOWERLIMIT_SPACE;
    }

    if (pad) {
        length += (4 * simplecase.special.padding[2])
    }

    console.log("Length (units of set): " + length)
    //let units_of_set_per_line = linewidth * 12 * 18 / simplecase.special.setwidth
    length_picas = length * simplecase.special.setwidth / (12 * 18);
    console.log("Length (picas): " + length_picas)
    return picas2mm(length_picas);
}