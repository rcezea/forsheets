/**
 * User Authentication Form Handling
 *
 * This script handles form submissions for user signup and login using AJAX requests.
 * It prevents the default form submission, sends data to the server, and redirects
 * the user to the dashboard on successful authentication.
 *
 * Note: Assumes the presence of HTML forms with names 'signup_form' and 'login_form',
 * and error elements with the class 'error'.
 */

// Signup Form Submission Handling
$("form[name=signup_form]").submit(function(e) {
  if (!validateSignUp()){
    return false;
  }
  const $form = $(this);
  const $error = $form.find(".error");
  const data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

// Login Form Submission Handling

$("form[name=login_form]").submit(function(e) {
  if (!validateSignIn()){
    return false;
  }
  const $form = $(this);
  const $error = $form.find(".error");
  const data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});
