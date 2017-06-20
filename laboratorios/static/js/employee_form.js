$('#myForm').on('submit', function(evt){
  $('input:checkbox[id^="checkbox_role"]:checked').each(function(){
    var role = $('<input>', {
      name: 'roles',
      type: 'hidden'
    }).val($(this).attr('name'));
    $('#myForm').append(role);
  });
});