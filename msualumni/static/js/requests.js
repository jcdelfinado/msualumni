
function take_action(id, action){
	alert(id + " " +action)
	
	$.post(
		'/admin/profiles/requests/commit',
		{'applicant_id':id, 'action_taken':action, 'csrf_token':csrftoken},
		function(){
			alert('Success!')
		}
	)
}

function commit(action){
	var total = $('input[class="selector"]:checked').length
	var current = 0
	$('input[class="selector"]:checked').each(function(){
		var id = $(this).data('id')
		take_action(id, action)
	})
}
