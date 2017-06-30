$(document).ready(function() {
    var table = $('#inv-table');
    $('#register_button').click( function() {
      table.find("tr.data_row").each(function () {
        var current_value = parseInt($(this).find('td.current_value').text());
        var change_value = parseInt($(this).find('td.display_item').text());
        var id = parseInt($(this).find('td.display_item').attr('id'));

        if(parseInt(change_value)!=0){ //only if there are changes
          $.ajax({
            url: 'save_article/',
            type: "POST",
            data: {current_value: current_value, change_value:change_value, id:id}
          })
        }
      });
      //delete last part of url to get show_url
      var show_url= window.location.href.substring(0, window.location.href.lastIndexOf('/'));
      window.location.replace(show_url);
    });

} );
