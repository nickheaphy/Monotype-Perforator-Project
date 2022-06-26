// setup the event listeners
var matrixModalEl = document.getElementById('matrixModal');
if (matrixModalEl !== null) {
    matrixModalEl.addEventListener('show.bs.modal', function (event) {
        var td = event.relatedTarget;
        var id = td.getAttribute('id');
        var chardata = getProperties(jsoncase, id);
        matrixModal.querySelector('#matrixpos').value = id
        if (chardata.character !== undefined) {
            matrixModal.querySelector('#character').value = chardata.character;
        } else {
            matrixModal.querySelector('#character').value = "";
        }
        if (chardata.desc !== undefined) {
            matrixModal.querySelector('#description-text').value = chardata.desc;
        } else {
            matrixModal.querySelector('#description-text').value = "";
        }
        if (chardata.style == "italic") {
            matrixModal.querySelector('#charstyle2').checked = true;
            console.log(chardata.style)
        } else if (chardata.style == "smallcap") {
            matrixModal.querySelector('#charstyle3').checked = true;
        } else {
            matrixModal.querySelector('#charstyle1').checked = true;
        }
        if (chardata.weight == "bold") {
            matrixModal.querySelector('#charweight2').checked = true;
        } else {
            matrixModal.querySelector('#charweight1').checked = true;
        }
        if (chardata.special == "jspace") {
            matrixModal.querySelector('#specialjspace').checked = true;
        } else if (chardata.special == "quad") {
            matrixModal.querySelector('#specialquad').checked = true;
        } else if (chardata.special == "blank") {
            matrixModal.querySelector('#specialblank').checked = true;
        } else {
            matrixModal.querySelector('#specialnormal').checked = true;
        }
        matrixModal.querySelector('#character').focus();
    });
};

var unitModalEl = document.getElementById('unitModal');
if (unitModalEl !== null) {
    unitModalEl.addEventListener('show.bs.modal', function (event) {
        var td = event.relatedTarget;
        var id = td.getAttribute('id');
        var row = id.split(/(\d+)/)[1]
        unitModal.querySelector('#rowpos').value = row
        unitModal.querySelector('#units').value = jsoncase.units[row]
    });
};

var validateModalEl = document.getElementById('validateModal')
if (validateModalEl !== null) {
    validateModalEl.addEventListener('show.bs.modal', function (event) {
        validateModal.querySelector('#errorreport').innerHTML = validateMCA(jsoncase);
    });
};

var modelMatrixSaveButton = document.getElementById('matrixSaveButton');
if (modelMatrixSaveButton !== null) {
    modelMatrixSaveButton.addEventListener("click", function (event) {
        var charpos = matrixModal.querySelector('#matrixpos').value;
        var updatedata = {};
        updatedata["character"] = matrixModal.querySelector('#character').value;
        updatedata["desc"] = matrixModal.querySelector('#description-text').value;
        if (matrixModal.querySelector('#charstyle2').checked) {
            updatedata["style"] = "italic";
        } else if (matrixModal.querySelector('#charstyle3').checked) {
            updatedata["style"] = "smallcap";
        } else {
            updatedata["style"] = "roman";
        }
        if (matrixModal.querySelector('#charweight2').checked) {
            updatedata["weight"] = "bold";
        } else {
            updatedata["weight"] = "";
        }
        if (matrixModalEl.querySelector('#specialjspace').checked) {
            updatedata["special"] = "jspace";
        } else if (matrixModalEl.querySelector('#specialquad').checked) {
            updatedata["special"] = "quad";
        } else if (matrixModalEl.querySelector('#specialblank').checked) {
            updatedata["special"] = "blank";
        } else {
            updatedata["special"] = "";
        }
        setProperties(jsoncase, charpos, updatedata);
    });
};


var modelUnitSaveButton = document.getElementById('unitSaveButton');
if (modelMatrixSaveButton !== null) {
    modelUnitSaveButton.addEventListener("click", function (event) {
        var row = unitModal.querySelector('#rowpos').value;
        var units = unitModal.querySelector('#units').value;
        setUnitProperties(jsoncase, row, units);
    });
};
