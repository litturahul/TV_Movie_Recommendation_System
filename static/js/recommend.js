$(function(){
    $('#movie-button').on('click',function(){
		var moviename = $('#moviename').val();
		console.log(moviename)
		var data = {name:moviename};
		console.log(data)
		$.ajax({
			url: '/similarity',
			data: data,
			cache: false,
			type: 'POST',
			success: function(response){
			    var resp=response.split(",")
			    $('#results').html('')
			    $('#results').append('<div class="card-header">Recommendations</div><ul class="list-group list-group-flush" id="result_data">')
			    $.each(resp,function ( index, repo ) {
			        console.log(index,repo)
			        $('#result_data').append('<li class="list-group-item">'+repo+'</li>');
			    });
			    $('#results').append('</div')
			},
			error: function(error){
				console.log(error);
			}
		});
	})
});