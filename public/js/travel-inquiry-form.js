$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    $.validator.addMethod("notNone", function(value, element) {
        return value !== "";
    }, "Please select a valid reference.");

    // validate travelinquiryform
    $(function() {
        $('#travelinquiryform').validate({
            rules: {
                email: {
                    minlength: 0
                },
                destination: {
                    required: true,
                    minlength: 0
                },
                departure: {
                    required: true,
                    minlength: 0
                },
                start_date: {
                    required: true,
                    minlength: 0
                },
                end_date: {
                    required: true,
                    minlength: 0
                },
                valid_passport: {
                    required: true,
                    minlength: 0
                },
                num_travelers: {
                    required: true,
                    minlength: 0
                },
                under_18_travelers: {
                    required: true,
                    minlength: 0
                },
                under_18_traveler_count: {
                    minlength: 0
                },
                accommodations: {
                    required: true,
                    minlength: 0
                },
                rooms: {
                    required: true,
                    minlength: 0
                },
                payment: {
                    required: true,
                    minlength: 0
                },
                atmosphere: {
                    required: true,
                    minlength: 0
                },
                budget: {
                    required: true,
                    minlength: 0
                },
                activities: {
                    required: true,
                    minlength: 0
                },
                reference: {
                    required: true,
                    minlength: 0,
                    notNone: true
                }
            },
            messages: {
                destination: {
                    required: "",
                    minlength: ""
                },
                departure: {
                    required: "",
                    minlength: ""
                },
                start_date: {
                    required: "",
                    minlength: ""
                },
                end_date: {
                    required: "",
                    minlength: ""
                },
                valid_passport: {
                    required: "",
                    minlength: ""
                },
                num_travelers: {
                    required: "",
                    minlength: ""
                },
                under_18_travelers: {
                    required: "",
                    minlength: ""
                },
                under_18_traveler_count: {
                    minlength: ""
                },
                accommodations: {
                    required: "",
                    minlength: ""
                },
                rooms: {
                    required: "",
                    minlength: ""
                },
                payment: {
                    required: "",
                    minlength: ""
                },
                atmosphere: {
                    required: "",
                    minlength: ""
                },
                budget: {
                    required: "",
                    minlength: ""
                },
                activities: {
                    required: "",
                    minlength: ""
                },
                reference: {
                    required: "",
                    notNone: ""
                }
            },
            submitHandler: function(form) {

                var atmosphere = [];
                $('input[name="atmosphere"]:checked').each(function() {
                    atmosphere.push($(this).val());
                });

                var activities = [];
                $('input[name="activities"]:checked').each(function() {
                    activities.push($(this).val());
                });

                var formData = {
                    email: $('#email').val(),
                    destination: $('#destination').val(),
                    departure: $('#departure').val(),
                    start_date: $('#start_date').val(),
                    end_date: $('#end_date').val(),
                    is_passport_valid: $('input[name="valid_passport"]:checked').val(),
                    num_travelers: $('#num_travelers').val(),
                    underage_travelers: $('input[name="under_18_travelers"]:checked').val(),
                    num_underage_travelers: $('#under_18_traveler_count').is(':visible') ? $('#under_18_traveler_count input').val() : "0",
                    accommodations: $('input[name="accommodations"]:checked').val(),
                    rooms: $('#rooms').val(),
                    payment_date: $('#payment').val(),
                    atmosphere: atmosphere.join(', '),
                    budget: $('#budget').val(),
                    activities: activities.join(', '),
                    reference: $('#reference').val()
                };

                $.ajax({
                    type: "POST",
                    url: "http://localhost:5000/travelinquiryformsubmit",
                    contentType: "application/json", 
                    data: JSON.stringify(formData), 
                    success: function() {
                        $('#travelinquiryform :input').attr('disabled', 'disabled');
                        $('#travelinquiryform').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');

                            setTimeout(function() {
                                location.reload();
                            }, 5000)
                        })
                    },
                    error: function() {
                        $('#travelinquiryform').fadeTo( "slow", 1, function() {
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