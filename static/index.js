



document.addEventListener("DOMContentLoaded", function(){
  showUserNav()
  showMenuNav()
  }
)

function togglePassword() {
  var pass_inputs = document.getElementsByName("signup_password")
  var pass_imgs = document.getElementsByClassName("pass_img")
  if (pass_inputs[0].type === "password") {
      pass_inputs[0].type = "text";
      pass_imgs[0].src = "../static/website_images/hidepass.png"
  }
  else {
      pass_inputs[0].type = "password";
      pass_imgs[0].src = "../static/website_images/showpass.png"
  }
}y

function showUserNav(){
      var pfp = document.getElementById("pfp_div")

      pfp.addEventListener("click", function(event){
          // makes it so eventListener for click on 'pfp' doesnt activate parent event listener (body)
          event.stopPropagation();
          var user_nav_div = document.getElementById("user_navigation");
          var pfp_nav_info = document.getElementById("pfp_nav_info");
          var body = document.getElementById("homepage_body")
          user_nav_div.classList.remove("hidden")
          pfp_nav_info.style.display = "none";
          body.addEventListener("click", hideUserNav)
          pfp.addEventListener("mouseleave", showPfpNavInfo)
     }
  )
}

function hideUserNav(){
    var user_nav_div = document.getElementById("user_navigation");
    user_nav_div.classList.add("hidden")
    document.getElementById("homepage_body").removeEventListener("click", showUserNav)

}

function showPfpNavInfo(){
    // when calling showUserNav we make the pfp_nav_info to display:none, so when mouse leaves pfp - we remove that style
    var pfp_nav_info = document.getElementById("pfp_nav_info");
    pfp_nav_info.style.removeProperty('display')
}

function showMenuNav(){
    var menu = document.getElementById("menu_div")
    menu.addEventListener("click", function(event){
      event.stopPropagation(); // Again - dont want menu's onclick to trigger parents 'main_navigation' or 'nav_menu' onclick through Bubbling
      var menu_nav_div = document.getElementById("menu_navigation")
      var close_icon_div = document.getElementById("close_icon_div")
      var backdrop = document.getElementById("backdrop")

      menu_nav_div.classList.remove("hidden")
      close_icon_div.addEventListener("click", hideMenuNav)
      backdrop.style.display = "block"
      backdrop.addEventListener("click", hideMenuNav)


    }
  )
}

function hideMenuNav(){
    var menu_nav_div = document.getElementById("menu_navigation");
    var backdrop = document.getElementById("backdrop")
    menu_nav_div.classList.add("hidden")
    backdrop.style.display = "none"
    backdrop.removeEventListener("click", hideMenuNav)
    document.getElementById("homepage_close_icon_div").removeEventListener("click", hideMenuNav)
}