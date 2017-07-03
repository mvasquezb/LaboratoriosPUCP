function validateNumber(txt) {
  return $.isNumeric(txt);
}

function validatePositiveNumber(txt) {
  return $.isNumeric(txt) && Number(txt) > 0;
}

function validatePositiveInteger(txt) {
  try {
    return $.isNumeric(txt) && parseInt(txt) > 0;
  } catch (e) {
    return false;
  }
}

function numberValidator($el) {
  if (!validateNumber($el.val())) {
    return 'Ingrese un número válido';
  }
}

function positiveNumberValidator($el) {
  var validateNumber = $el.data('validate-positive-number');
  if (validateNumber !== 'undefined') {
    if (!validatePositiveNumber($el.val())) {
      return 'Ingrese un número válido';
    }
  }
}

function validateRUC(txt) {
  if (txt.length != 11)
    return false;
  if (!validatePositiveInteger(txt)) {
    return false;
  }
  return true;
}

function validateDNI(txt) {
  if (txt.length != 8)
    return false;
  if (!validatePositiveInteger(txt)) {
    return false;
  }
  return true;
}

function docNumberValidator($el) {
  if ($el.data('validate-doc-number') !== 'undefined') {
    var type = $el.data('type');
    var valid = false;
    if (type == 'ruc') {
      valid = validateRUC($el.val());
    } else if (type == 'dni') {
      valid = validateDNI($el.val());
    }
    if (!valid) {
      return 'El número de documento no es válido';
    }
  }
}
