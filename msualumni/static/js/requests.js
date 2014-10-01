var approved = 0
var recommended = 0
var rejected = 0

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
			if (data == 'Approved'){
				approved++
				return true
			}
			if (data == 'Recommended'){
				recommended++
				updateProgress(total)
				$('#'+id).remove()
				return true
			}
			if (data == 'Rejected'){
				rejected++
				return true
			}
			return false
		}
	)
}

function commit(action){
	var total = $('input[class="selector"]:checked').length
	var current = 0
	var success
	$('input[class="selector"]:checked').each(function(){
		var id = $(this).data('id')
		success = take_action(id, action, total)
	})
	if (success) alert('OK ' + recommended)
}
function showProgress(){
	$('#progress').show()
}

