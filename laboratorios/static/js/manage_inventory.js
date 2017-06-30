$(document).ready(function() {
    var table = $('#inv-table');
    $('button').click( function() {
      table.find("tr.data_row").each(function () {
        var current_value = $(this).find('td.current_value').text();
        var change_value = $(this).find('td.display_item').text();
        var id = $(this).find('td.display_item').attr('id');

        if(parseInt(change_value)!=0){ //only if there are changes
          $.ajax({
            url: '/inventory/save_articles/',
            type: "GET",
            data: {current_value: current_value, change_value:change_value, id:id, article_type:article_type, inventory_id:inventory_id}
          }).done(function (data) {
            alert(data); //
          });
        }
      });
      return false;
    });
} );
