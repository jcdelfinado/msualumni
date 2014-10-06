var current = 0

function updateProgress(full){
	var offset = (100/full)
	var width = $('#bar').data('valuenow')
	var goal = width + offset
	while(width < goal){
		width++
		$('#bar').css('width', width+'%')
	}
	$('#bar').data('valuenow', width)
}

function take_action(id, action, total){
	
	$.post(
		'/admin/profiles/requests/commit',
		{'applicant_id':id, 'action_taken':action, 'csrf_token':csrftoken},
		function(data){
			current++
			updateProgress(total)
			$('#'+id).remove()
			return true
		}
	)
}

function commit(action){
	showProgress()
	var total = $('input[class="selector"]:checked').length
	var success
	$('input[class="selector"]:checked').each(function(){
		var id = $(this).data('id')
		success = take_action(id, action, total)
	})
	if (success) {alert('OK ' + current)}
}
function showProgress(){
	$('.progress').show()
}

