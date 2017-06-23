
$('#form').on('submit', function (evt) {
  //evt.preventDefault();
  var $form = $(this);
  var name = $('<input>', {
    name: 'name',
    type: 'hidden',
    value: $('#inventory_name').val(),
  });
  $form.append(name);
  var location = $('<input>', {
    name: 'location',
    type: 'hidden',
    value: $('#inventory_name').val(),
  });
  $form.append(name);

  
  
  $('#comboBox').each(function () {
    var type = $('<input>', {
      name: 'inventory_type',
      type: 'hidden',
      value: $('#comboBox option:selected').text(),
    });
    $form.append(supervisor);
  }
  
});