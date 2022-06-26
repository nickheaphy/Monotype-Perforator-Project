// This is just some testing....

//var thetext = tinymce.get("texttoconvert").getContent({ format: "text" });
var thetext = "The quick brown fox. ♥"
console.log(thetext);
console.log(jsoncase);

var jspace_pos = get_jspace_matrixcode(jsoncase);
var pos = [];
var width = -1;

for (let c of thetext) {
    if (c == " ") {
        pos = jspace_pos;
    } else {
        pos = get_char_matrixcoord(jsoncase,c,"roman");
    }

    width = get_width_matrixcoord(jsoncase,pos);

    //console.log("Col:"+pos[0]+" Row:"+pos[1]+" Width:"+width);
}

var newmc = mcatransform_simplecase(jsoncase);
for (let c of thetext) {
    if (c == " ") {
        pos = newmc.special.jspace || [null, null, null];
    } else {
        pos = newmc.roman[c] || [null, null, null];
    }
    //console.log("Col:"+pos[0]+" Row:"+pos[1]+" Width:"+pos[2]);
}
