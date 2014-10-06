//ajax for simple string search
$('.alum-row').on('click', function() {
  var id = $(this).attr('id');
  
  $.get('/admin/profiles/get_profile', {'id' : id}, function(data){
    $('#profile').html(data);
    $('#profile_preview_modal').modal();
  });
});

$(':checkbox').on('change', function(){
  var field = $(this).data('toggle')
  $(field).attr('disabled',!this.checked);
  if ($(field).attr('disabled')){
    $(field).val('')
  }
  if ($(field).val().length == 0)
    $('#go_advanced').attr('disabled', true)
  else $('#go_advanced').attr('disabled', false)
});

$('#more').on('click', function(){
  $('#more_filters').slideToggle(500)
  if ($(this).text()=='Show more')
    $(this).text('Hide')
  else
    $(this).text('Show more') 
});

$('.advanced').on('keyup', function(){
  if ($(this).val().length == 0)
    $('#go_advanced').attr('disabled', true)
  else $('#go_advanced').attr('disabled', false)
});



