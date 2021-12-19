var loadFile = function(event) {

	var data = new FormData($('#avatar_form').get(0));
	var output = document.querySelector('.upload_image_element');
	var profImage = document.querySelector('#prof-image');
	var navIcon = document.querySelector('#nav-icon');

	$.ajax({
		url: $("#avatar_form").attr("data-avatar-url"),
		data: data,
		type: 'post',
		contentType: 'multipart/form-data',
		processData: false,
		contentType: false,
		success: function () {
			let file = event.target.files[0]
			let src = URL.createObjectURL(file);
			output.src = src
			profImage.src = src
			navIcon.src = src
			output.onload = function() {
				URL.revokeObjectURL(output.src) // free memory
			}
			profImage.onload = function() {
				URL.revokeObjectURL(profImage.src) // free memory
			}
			navIcon.onload = function() {
				URL.revokeObjectURL(navIcon.src) // free memory
			}
			$('.notification-text').html("Profile photo updated!");
			$('#notify').fadeIn('slow')
			$('#notify').delay(5000).fadeOut('slow');
	
		},
		error: function () {
			$('.notification-text').html("Something is wrong!");
			$('#notify').fadeIn('slow')
			$('#notify').delay(5000).fadeOut('slow');
		}
	});
};
