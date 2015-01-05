window.onload = function() {
	$('.replyBtn').click(function(){
		if (!$('#response').length) {
            var form = $('<form></form>').attr({
				'id': 'response',
	            'method': 'post',
	            'action': '/response'
	        });
			form.append(
	        	$('<textarea></textarea>').attr({
	        		'class': 'jumbotron reply col-sm-10 col-sm-offset-2',
	        		'name': 'responsetext',
	        		'id': 'responsetext'
	        	}),
	        	$('<input/>').attr({
                    'name': 'author',
                    'style': 'display:none',
                    'value': $(this).prevAll('.author').text()
	        	}),
	        	$('<button></button>').attr({
	        		'class': 'replyBtn btn btn-primary',
	        		'type': 'submit'
	        	}).text('回复'),
	        	$('<button></button>').attr({'class': 'replyBtn btn btn-primary'}).text('解密'),
	        	$('<button></button>').attr({'class': 'replyBtn btn btn-primary'}).text('加密')
	        );
	        $(this).parent().append(form);
		}
	});
}