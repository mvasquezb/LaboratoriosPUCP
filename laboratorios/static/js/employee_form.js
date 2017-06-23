$('#myForm').on('submit', function(evt){
  $('input.checkbox_role:checkbox:checked').each(function() {
    var role = $('<input>', {
      name: 'roles',
      type: 'hidden'
    }).val($(this).attr('name'));
    $('#myForm').append(role);
  });
  $('input.checkbox_laboratory:checkbox:checked').each(function() {
    var laboratory = $('<input>', {
      name: 'laboratories',
      type: 'hidden'
    }).val($(this).attr('name'));
    $('#myForm').append(laboratory);
    console.log('test');
  });
});
