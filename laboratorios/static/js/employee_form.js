$('#myForm').on('submit', function(evt){
  $('input.checkbox_role:checkbox:checked').each(function() {
    var role = $('<input>', {
      name: 'roles',
      type: 'hidden'
    }).val($(this).attr('name'));
    $('#myForm').append(role);
  });
});
