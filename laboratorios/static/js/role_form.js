$('#myForm').on('submit', function(evt){
  $('input:checkbox[id^="checkbox_permission"]:checked').each(function(){
    var permission = $('<input>', {
      name: 'permissions',
      type: 'hidden'
    }).val($(this).attr('name'));
    $('#myForm').append(permission);
  });
});