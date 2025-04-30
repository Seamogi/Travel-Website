$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                email: {
                    minlength: 0
                },
                subject: {
                    required: true,
                    minlength: 0
                },
                message: {
                    required: true,
                    minlength: 0
                }
            },
            messages: {
                subject: {
                    required: "Subject field is required",
                    minlength: ""
                },
                message: {
                    required: "Message field is required",
                    minlength: ""
                }
            },
            submitHandler: function(form) {

                var formData = {
                    email: $('#email').val(),
                    subject: $('#subject').val(),
                    message: $('#message').val()
                };

                $.ajax({
                    type: "POST",
                    url: "http://localhost:5000/contact",
                    contentType: "application/json", 
                    data: JSON.stringify(formData), 
                    success: function() {
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');

                            setTimeout(function() {
                                location.reload();
                            }, 5000)
                        });
                    },
                    error: function() {
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $('#error').fadeIn()
                            $('.modal').modal('hide');
		                	$('#error').modal('show');
                        })
                    }
                })
            }
        })
    })
        
 })(jQuery)
})