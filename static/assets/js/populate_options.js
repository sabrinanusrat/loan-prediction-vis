function populateDropdown(selector, options, selection) {
    var element = document.getElementById(selector);
    Object.keys(options).forEach( text => {
        if (!!selection && options[text] == selection) {
            element.innerHTML += '<option value="'+options[text]+'" selected>'+text+'</option>'
        } else {
            element.innerHTML += '<option value="'+options[text]+'">'+text+'</option>'
        }
    });
}

function populateRadioButtons(selector, options, selection) {
    var element = document.getElementById(selector);
    Object.keys(options).forEach( text => {
        if (!!selection && options[text] == selection) {
            element.innerHTML += '<input type="radio" name="'+selector+'" id="radio-'+selector+'-'+options[text]+'" value="'+options[text]+'" checked/>'
        } else {
            element.innerHTML += '<input type="radio" name="'+selector+'" id="radio-'+selector+'-'+options[text]+'" value="'+options[text]+'" />'
        }
        element.innerHTML += '<label for="radio-'+selector+'-'+options[text]+'">'+text+'</label>'
    });
}
