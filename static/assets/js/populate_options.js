function populateDropdown(selector, options) {
    var element = document.getElementById(selector);
    Object.keys(options).forEach( text => {
        element.innerHTML += '<option value='+options[text]+'>'+text+'</option>'
    });
}

function populateRadioButtons(selector, options) {
    var element = document.getElementById(selector);
    Object.keys(options).forEach( (text, index) => {
        if (index ==0) {
            element.innerHTML += '<input type="radio" name='+selector+' id=radio-'+selector+'-'+options[text]+' value='+options[text]+' checked/>'
        } else {
            element.innerHTML += '<input type="radio" name='+selector+' id=radio-'+selector+'-'+options[text]+' value='+options[text]+' />'
        }
        
        element.innerHTML += '<label for=radio-'+selector+'-'+options[text]+'>'+text+'</label>'
    });
}
