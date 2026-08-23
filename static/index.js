

function togglePassword() {
  var pass_inputs = document.getElementsByName("signup_password")
  var pass_imgs = document.getElementsByClassName("pass_img")
  if (pass_inputs[0].type === "password") {
      pass_inputs[0].type = "text";
      pass_imgs[0].src = "../static/hidepass.png"
  }
  else {
      pass_inputs[0].type = "password";
      pass_imgs[0].src = "../static/showpass.png"
  }

}