//var selected_users = [];
//var capacity_users;
//var counting = $('.checkbox_users:checked').length;
//var to_out;

/*
function handlePaste(e) {
  var clipboardData, pastedData;

  // Get pasted data via clipboard API
  clipboardData = e.clipboardData || window.clipboardData;
  pastedData = clipboardData.getData('Text').toUpperCase();

  if (pastedData.indexOf('E') > -1) {
    //alert('found an E');
    e.stopPropagation();
    e.preventDefault();
  }
};

function FilterNmberInput(event) {
  var keyCode = ('which' in event) ? event.which : event.keyCode;

  isNotWanted = (keyCode == 69 || keyCode == 101);
  return !isNotWanted;
};

*/  
  /*
//cuando se invalida data
$('#capacity').on('invalid.bs.validator', function () {
  //$('#users_selection').hide();
  $('input.checkbox_users:checkbox').prop('checked', false);
  //selected_users.length = 0;
  $('input.checkbox_users:checkbox').prop('disabled', true);
  counting = 0;
  //borrar todos los campos en responsable de laboratorio
  $('#comboBox').empty();
  $('#comboBox').append($('<option>', {
    text: "Ningún Responsable Seleccionado"
  }));
});
  */
  /*
//cuando se valida la data
$('#form').on('valid.bs.validator', function () {
  //$('#users_selection').show();
  $('input.checkbox_users:checkbox').prop('disabled', false);
  capacity_users = $("#capacity").val();
});
*/

/*
var value = $('#capacity').val();
$('#capacity').on('keyup change click', function () {
  if (this.value !== value) {
    $('input.checkbox_users:checkbox').prop('checked', false);
    counting = 0;
    $('#comboBox').empty();
    $('#comboBox').append($('<option>', {
      text: "-- Ningún Responsable Seleccionado --"
    }));
    capacity_users = $(this).val();
  }
});
*/


//cuando se clickea en los checkboxes de usuarios de laboratorio
$('input.checkbox_users:checkbox').on('ifChanged', function () {
  if ($(this).is(':checked')) {
      $('#comboBox').append($('<option>', {
        text: $(this).data('name'),
        'data-id': $(this).data('id'),
      }));
  } else {
    to_out = $(this).data('name');
    var to_remove = $('#comboBox option').filter(function () {
      return $(this).text() == to_out;
    });
    $(to_remove).remove();
  }
});


//cuando se clickea en el boton registrar primero se arma la estructura de django para que se
//reciba en el view
$('#form').on('submit', function (evt) {
  //evt.preventDefault();
  var $form = $(this);
  var name = $('<input>', {
    name: 'name',
    type: 'hidden',
    value: $('#laboratory_name').val(),
  });
  $form.append(name);

  /*
  var capacity = $('<input>', {
    name: 'capacity',
    type: 'hidden',
    value: $('#capacity').val(),
  });
  $form.append(capacity);
  */
  
  $('input.checkbox_users:checkbox:checked').each(function () {
    var employee = $('<input>', {
      name: 'employees',
      type: 'hidden',
      value: $(this).data('id'),
    });
    $form.append(employee);
  });
  
  
  if ($('#comboBox option:selected').text() == 'Ningún Responsable Seleccionado') {
    //$form.append($('<input>').attr('name', 'supervisor').val());
  } else {
    var supervisor = $('<input>', {
      name: 'supervisor',
      type: 'hidden',
      value: $('#comboBox option:selected').data('id'),
    });
    $form.append(supervisor);
  }
  

  $('input.checkbox_inventory:checkbox:checked').each(function () {
    var inventory = $('<input>', {
      name: 'inventory',
      type: 'hidden',
      value: $(this).data('id'),
    });
    $form.append(inventory);
  });

  $('input.checkbox_essay:checkbox:checked').each(function () {
    var essay = $('<input>', {
      name: 'essay_methods',
      type: 'hidden',
      value: $(this).data('id'),
    });
    $form.append(essay);
  });

});

  $('.inventory_modal').on('click',function(){
    var inventory_pk = $(this).data('pk');
    var url = $(".page_title").data("url");
    $('.content_table').empty();
    $('.header_table').empty();
    $('.inventory_empty').empty();
    $('.inventory_table').show();
    $.get(url, {'inventory_pk': inventory_pk},function(data){
      //General Data
      $('div.inventory_name').replaceWith("<div class='inner inventory_name'>" + data['inventory_name'] +"</div>");
      $('div.inventory_location').replaceWith("<div class='inner inventory_location'>" + data['inventory_location'] + "</div>");
      $('div.inventory_type').replaceWith("<div class='inner inventory_type'>" + data['inventory_type'] + "</div>");
      //Inventory Content Data
      var element_list = data['inventory_matches'];
      var element;
      var i;
      
      if (element_list.length == 0){
        $('.inventory_empty').append("<h4>No hay contenido en este inventario</h4>");
        $('.inventory_table').hide();
      }
      else {
        if (data['inventory_type'] == 'Equipos') {
          $('.header_table').append("<tr>" + "<th>#</th>" + "<th>Nombre</th>" + "<th>Unidad de tiempo</th>" + "<th>Tiempo de vida</th>" + "<th>Rango de error</th>" + "<th>Cantidad</th>" + "</tr>");
        }
        else if (data['inventory_type'] == 'Insumos'){
          $('.header_table').append("<tr>" + "<th>#</th>" + "<th>Nombre</th>" + "<th>Unidad métrica</th>" + "<th>Cantidad</th>" + "</tr>");
        }
        else{
        //$('.header_table').append("<thead><tr>" + "<th>#</th>" + "<th>Nombre</th>" + "<th>Unidad de tiempo vida</th>" + "<th>Tiempo de vida</th>" + "<th>Rango de error</th>" + "</tr></thead>");
        }

        for (i=0;i<element_list.length;i++){
          element = element_list[i];
          if (data['inventory_type'] == 'Equipos'){
            $('.content_table').append("<tr>" + "<th>" + (i+1) + "</th>" + "<th>" + element[0] + "</th>" +"<th>" + element[1] + "</th>" + "<th>" + element[2] + "</th>" + "<th>" + element[3] + "</th>" + "<th>" + element[4] + "</th>" + "</tr>");
          }
          else if (data['inventory_type'] == 'Insumos'){
            $('.content_table').append("<tr>" + "<th>" + (i+1) + "</th>" + "<th>" + element[0] + "</th>" +"<th>" + element[1] + "</th>" + "<th>" + element[2] + "</th>" + "</tr>");
          }
          else {
            //
          }
        }
      }
      
    });
  });

  $('.employee_modal').on('click',function(){
    var employee_pk = $(this).data('pk');
    var url = $('.page_title').data('emp');
    $('.roles_content').empty();
    $('.empty_message').empty();
    $('.roles_table').show();
    $.get(url, {'employee_pk': employee_pk}, function(data){
      var element_list = data['roles_data'];
      var element;
      var i;
      if (element_list.length == 0){
        $('.empty_message').append("<h4>No hay roles asociados a este empleado</h4>");
        $('.roles_table').hide();
      }
      else {
        for (i=0;i<element_list.length;i++){
          element = element_list[i];
          $('.roles_content').append("<tr>" + "<th>" + (i+1) + "</th>" + "<th>" + element[0] + "</th>" + "<th>" + element[1] + "</th>" + "</tr>");
        }
      }
    });
  });
