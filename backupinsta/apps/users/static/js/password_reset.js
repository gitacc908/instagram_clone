  

$('#send-reset-link-button').click(
    function(e){
        e.preventDefault();
        let formData = $('#email-submission-form').serialize();
        $.ajax({
            url : $('#send-reset-link-button').attr('data-url-target'),
            type : "POST", 
            data : formData, 

            success : function(data) {
                    $('.alert-success').html(data.success).fadeIn('slow');
                    $('.alert-success').delay(8000).fadeOut('slow'); 
            },
            error : function(data) {
                $('.alert-danger').html(data.responseJSON.form_errors['email']).fadeIn('slow');
                $('.alert-danger').delay(8000).fadeOut('slow'); 
            }
    });
})
