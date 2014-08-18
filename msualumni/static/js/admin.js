$('#browse_csv_button').click(function(e){
	$('#hidden_upload').click()
	e.preventDefault()
})

$('#hidden_upload').change(function(){
	$('#dummy-text-field').val($('#hidden_upload').val())
	if ($('#go_upload').attr('disabled') == 'disabled')

		if ($('#hidden_upload').val() != '')
			$('#go_upload').attr('disabled', false)
})
