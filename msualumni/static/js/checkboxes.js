$('#check-all').click(function(){
      $('.selector').prop('checked', this.checked);
    })
    $('.selector').click(function(){
      var check = ($('.selector').filter(':checked').length == $('.selector').length);
      $('#check-all').prop('checked', check);
    })