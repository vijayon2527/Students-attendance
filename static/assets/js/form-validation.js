(function($) {
  'use strict';
  $.validator.setDefaults({
    submitHandler: function() {
      alert("Form successfully submitted!");
    }
  });

  $(function() {
    $("#signupForm").validate({
      rules: {
        firstname: {
          required: true
        },
        lastname: {
          required: true
        },
        username: {
          required: true,
          minlength: 2
        },
        email: {
          required: true,
          email: true
        },
        password: {
          required: true,
          minlength: 5
        },
        confirm_password: {
          required: true,
          minlength: 5,
          equalTo: "#password"
        },
        agree: {
          required: true
        }
      },
      messages: {
        firstname: "Please enter your first name",
        lastname: "Please enter your last name",
        username: {
          required: "Please enter a username",
          minlength: "Username must be at least 2 characters long"
        },
        email: {
          required: "Please enter your email",
          email: "Please enter a valid email address"
        },
        password: {
          required: "Please provide a password",
          minlength: "Password must be at least 5 characters long"
        },
        confirm_password: {
          required: "Please confirm your password",
          minlength: "Password must be at least 5 characters long",
          equalTo: "Passwords do not match"
        },
        agree: "Please accept our policy"
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element) {
        $(element).closest('.form-group').addClass('has-danger');
        $(element).addClass('form-control-danger');
      },
      unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-danger');
        $(element).removeClass('form-control-danger');
      }
    });
  });
})(jQuery);
