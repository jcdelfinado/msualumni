function approve(action){
	var total = $('input[class="selector"]:checked').length
	var current = 0
	$('input[class="selector"]:checked').each(function(){
		var id = $(this).data('id')
		take_action(id, action)
	})
}

function take_action(id, action){
	$.post(
		'/profiles/requests/action',
		{'applicant_id':id, 'action_taken':action},
		function(){
			alert('Success!')
		}
	)
}