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
    $.get(url, {'inventory_pk': inventory_pk},function(data){
      //General Data
      $('div.inventory_name').replaceWith("<div class='inner inventory_name'>" + data['inventory_name'] +"</div>");
      $('div.inventory_location').replaceWith("<div class='inner inventory_location'>" + data['inventory_location'] + "</div>");
      $('div.inventory_type').replaceWith("<div class='inner inventory_type'>" + data['inventory_type'] + "</div>");
      //Inventory Content Data
      var element_list = data['inventory_matches'];
      var element;
      var i;
      
      /*
      if data['inventory_type'] == 'Equipos' {
        $('.header_table').append();
      }
      else if data['inventory_type'] == 'Insumos'{

      }
      else{

      }
      */

      for (i=0;i<element_list.length;i++){
        element = element_list[i];
        $('.content_table').append("<tr>" + "<th>" + (i+1) + "</th>" + "<th>" + element[0] + "</th>" +"<th>" + element[1] + "</th>" + "</tr>");
        //$('.content_table').append("<th>" + (i+1) + "</th>");
        //$('.content_table').append("<th>" + element[0] + "</th>");
        //$('.content_table').append("<th>" + element[1] + "</th>");
        //$('.content_table').append("</tr>");
      }
      
    });
    //console.log("pasa el ajax")
    //
    //$('div.inventory_name').replaceWith("<div class='inner inventory_name'>" + data['inventory_name'] +"</div>");
    //$('div.inventory_pk').replaceWith("<div class='inner inventory_pk'>" + inventory_pk + "</div>");
  });
