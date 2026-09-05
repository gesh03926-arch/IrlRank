
// Global variables
let backdrop
let hours_worked =0
let mark_dict
const months = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

//DOM_LOAD
document.addEventListener("DOMContentLoaded", function(){

    if(document.getElementById("nav_menu")){
        backdrop = document.getElementById("backdrop")
        showUserNav()
        showMenuNav()
    }
    if(document.getElementById("landing_page_body")){
        textTyping()
    }
    if(document.getElementById("calendar")){
        mark_dict_json = document.getElementById("mark_dict_input").value
        mark_dict = JSON.parse(mark_dict_json)
        console.log(mark_dict)
        calendarNavigation()
    }
  }
)
//PASSWORD
function togglePassword() {
    const pass_inputs = document.getElementsByName("signup_password")
    const pass_imgs = document.getElementsByClassName("pass_img")
    if (pass_inputs[0].type === "password") {
      pass_inputs[0].type = "text";
      pass_imgs[0].src = "../static/website_images/hidepass.png"
    }
    else {
      pass_inputs[0].type = "password";
      pass_imgs[0].src = "../static/website_images/showpass.png"
    }
}

//NAVIGATION
function showUserNav(){
    const pfp = document.getElementById("pfp_div")

    pfp.addEventListener("click", function(event){

      // makes it so eventListener for click on 'pfp' doesnt activate parent event listener (body)
      event.stopPropagation();
      const user_nav_div = document.getElementById("user_navigation");
      const pfp_nav_info = document.getElementById("pfp_nav_info");
      const body = document.getElementById("homepage_body")
      user_nav_div.classList.remove("hidden")
      pfp_nav_info.style.display = "none";

      body.addEventListener("click", hideUserNav)
      pfp.addEventListener("mouseleave", showPfpNavInfo)

      user_nav_div.addEventListener("click", (event)=>{
          // body's click closes user_nav.
          // Since user_nav is part of body => clicking on it leads to body's click (Propagation / Bubbling)
          // We stop propagation so user_nav's click doesn't activate body's click => doesn't close it
          event.stopPropagation()
          }
      )
    }
    )
}

function hideUserNav(){
    const user_nav_div = document.getElementById("user_navigation");
    user_nav_div.classList.add("hidden")
    document.getElementById("homepage_body").removeEventListener("click", showUserNav)
}

function showPfpNavInfo(){
    // when calling showUserNav we make the pfp_nav_info to display:none, so when mouse leaves pfp - we remove that style
    const pfp_nav_info = document.getElementById("pfp_nav_info");
    pfp_nav_info.style.removeProperty('display')
}
function showMenuNav(){
    const menu = document.getElementById("menu_div")
    menu.addEventListener("click", function(event){
    //  event.stopPropagation(); // Again - dont want menu's onclick to trigger parents 'main_navigation' or 'nav_menu' onclick through Bubbling
        const menu_nav_div = document.getElementById("menu_navigation")
        const close_icon_div = document.getElementById("close_icon_div")
        menu_nav_div.classList.remove("hidden")
        close_icon_div.addEventListener("click", hideMenuNav)
        backdrop.classList.remove("hidden")
        backdrop.addEventListener("click", hideMenuNav)
        }
    )
}

function hideMenuNav(){
    document.getElementById("close_icon_div").removeEventListener("click", hideMenuNav)
    const menu_nav_div = document.getElementById("menu_navigation");
    menu_nav_div.classList.add("hidden")
    backdrop.classList.add("hidden")
    backdrop.removeEventListener("click", hideMenuNav)

}

//LANDING_PAGE
function textTyping(){
    const header = document.getElementById("entername_header")
    const header_text = header.textContent
    header.textContent = ""
    let iterationTime = 100
    for (let i = 0; i < header_text.length; i++) {
        setTimeout(() => {
        header.textContent += header_text[i]
        }, iterationTime)
        iterationTime += 40
    }
    setTimeout(()=>{
    const entername_input = document.getElementById("entername_input")
    entername_input.classList.remove("hidden")
    entername_input.focus()
    }, iterationTime+100)
    for (let j =0; j < 1000; j++){
        setTimeout(()=>{
        if (j>=0 && j%4!=0){
            header.textContent += "."
        }
        else{
            header.textContent = header_text
        }
        }, iterationTime +=500)
    }
}

//CALENDAR
function calendarNavigation(){
    // IZCHISTI TAZI FUNKCIQ. intializeDates(), i prosto smenqi month_index na -1 i +1 za left i right. drugoto e copy paste

    let current_date = new Date();
    generateCalendarContent(current_date)

    const left_arrow = document.getElementById("calendar_prev")
    const right_arrow = document.getElementById("calendar_next")

    left_arrow.addEventListener("click", () => {
        current_date = new Date(current_date.getFullYear(), current_date.getMonth()-1)
        generateCalendarContent(current_date)
      }
    )
    right_arrow.addEventListener("click", () => {
        current_date = new Date(current_date.getFullYear(), current_date.getMonth()+1)
        generateCalendarContent(current_date)
      }
    )
}
function generateCalendarContent(date){
    const date_info = getDateInfo(date)
    const month_and_year_text = date_info.get("month_and_year_text")
    document.getElementById("month_and_year").textContent = month_and_year_text

    const calendar_total_dates = 42
    const calendar_dates = document.getElementById("calendar_dates_list")
    let arr = date_info.get("arr")
    const current_month_index = arr[0]
    const current_year = arr[1]
    arr = String(arr)

    let inner_dict
    if(!mark_dict[arr]){
        inner_dict = {"left":[], "current":[], "right":[]}
        mark_dict[arr] =  inner_dict
    }
    else{
        inner_dict = mark_dict[arr]
    }
    const left_marks = inner_dict["left"]
    const current_marks = inner_dict["current"]
    const right_marks = inner_dict["right"]

    calendar_dates.innerHTML = ""
    const first_day_index = date_info.get("first_day_index")
    const previous_month_final_date = date_info.get("previous_final_date")
    const final_date = date_info.get("final_date")
    const already_added_dates = first_day_index + final_date
    const remaining_dates = calendar_total_dates - already_added_dates


    for (let i=0; i<first_day_index; i++){
        const month_date = document.createElement("li")
        const previous_month_date = previous_month_final_date-first_day_index+1+i
        const date_text = document.createTextNode(String(previous_month_date))
        month_date.appendChild(date_text)
        month_date.classList.add("calendar_date", "left_date")
        if(left_marks.includes(month_date.textContent)){
            month_date.style.backgroundColor = "green"
        }
        calendar_dates.appendChild(month_date)
    }
    for(let i=1; i<=final_date; i++){
        const month_date = document.createElement("li")
        const date_text = document.createTextNode(String(i))
        month_date.appendChild(date_text)
        month_date.classList.add("calendar_date", "current")
        if(current_marks.includes(month_date.textContent)){
            month_date.style.backgroundColor = "green"
        }
        calendar_dates.appendChild(month_date)
    }
    for(let i =0; i<remaining_dates; i++){
        const month_date = document.createElement("li")
        const date_text = document.createTextNode(String(i+1))
        month_date.appendChild(date_text)
        month_date.classList.add("calendar_date", "right_date")
        if(right_marks.includes(month_date.textContent)){
            month_date.style.backgroundColor = "green"
        }
        calendar_dates.appendChild(month_date)
    }


    let prev_arr = date_info.get("prev_arr")
    const prev_month_index = prev_arr[0]
    const prev_year = prev_arr[1]
    prev_arr = String(prev_arr)
    let next_arr = date_info.get("next_arr")
    const next_month_index = next_arr[0]
    const next_year = next_arr[1]
    next_arr = String(next_arr)

    console.log(current_month_index, prev_month_index, next_month_index)

    document.querySelectorAll(".current").forEach(
            date => date.addEventListener("click", () => {
                markDate(date, current_month_index, current_year)
                current_marks.push(date.textContent)
                date_value = parseInt(date.textContent)
                if(date_value<15){
                    if(!mark_dict[prev_arr]){
                        const inner_dict_prev = {"left":[], "current":[], "right":[date.textContent]}
                        mark_dict[prev_arr] = inner_dict_prev
                    }
                    else{
                        const inner_dict_prev = mark_dict[prev_arr]
                        const right_marks_prev = inner_dict_prev["right"]
                        right_marks_prev.push(date.textContent)
                    }
                }
                else if(date_value >=23){
                    if(!mark_dict[next_arr]){
                        const inner_dict_next = {"left":[date.textContent], "current":[], "right":[]}
                        mark_dict[next_arr] = inner_dict_next
                    }
                    else{
                        const inner_dict_next = mark_dict[next_arr]
                        const left_marks_next = inner_dict_next["left"]
                        left_marks_next.push(date.textContent)
                    }
                }
            }
          )
     )
     document.querySelectorAll(".left_date").forEach(
            date => date.addEventListener("click", () => {
                markDate(date, prev_month_index, prev_year)
                left_marks.push(date.textContent)
                if (!mark_dict[prev_arr]){
                    const inner_dict_prev = {"left": [], "current": [date.textContent], "right": []}
                    mark_dict[prev_arr] = inner_dict_prev
                }
                else{
                    const inner_dict_prev = mark_dict[prev_arr]
                    const current_marks_prev = inner_dict_prev["current"]
                    current_marks_prev.push(date.textContent)
                }
            }
          )
     )
      document.querySelectorAll(".right_date").forEach(
            date => date.addEventListener("click", () => {
                markDate(date, next_month_index, next_year)
                right_marks.push(date.textContent)
                if (!mark_dict[next_arr]){
                    const inner_dict_next = {"left":[], "current":[date.textContent], "right":[]}
                    mark_dict[next_arr] = inner_dict_next
                }
                else{
                    const inner_dict_next = mark_dict[next_arr]
                    const current_marks_next = inner_dict_next["current"]
                    current_marks_next.push(date.textContent)
                }
            }
          )
     )
}
function getDateInfo(date_object){
    const month_date = date_object.getDate()
    const month_index =date_object.getMonth()
    const month = months[month_index]
    const year = date_object.getFullYear()
    const month_and_year_text = month + " " + year
    const final_date = new Date(year, month_index+1, 0).getDate()
    const first_day_index = new Date(year, month_index, 1).getDay()
    const previous_final_date = new Date(year, month_index, 0).getDate()
    const arr = [month_index, year]


    const prev_date = new Date(year, month_index-1)
    const prev_arr = [prev_date.getMonth(), prev_date.getFullYear()]
    const next_date = new Date(year, month_index+1)
    const next_arr = [next_date.getMonth(), next_date.getFullYear()]

    const date_info_map = new Map()
    date_info_map.set("month_index", month_index)
    date_info_map.set("month", month)
    date_info_map.set("year", year)
    date_info_map.set("month_and_year_text", month_and_year_text)
    date_info_map.set("final_date", final_date)
    date_info_map.set("previous_final_date", previous_final_date)
    date_info_map.set("first_day_index", first_day_index)
    date_info_map.set("arr", arr)
    date_info_map.set("prev_date", prev_date)
    date_info_map.set("prev_arr", prev_arr)
    date_info_map.set("next_date", next_date)
    date_info_map.set("next_arr", next_arr)

    return date_info_map
}

function formatCalendar(date_or_month){
    if(date_or_month<10){
            let formatted_date = "0" + date_or_month
            return formatted_date
    }
    else{
        return String(date_or_month)
    }
}
function markDate(date_element, month_index, year){

    backdrop.classList.remove("hidden")
    backdrop.addEventListener("click", hideAddHoursDiv)
    const add_hours_div = document.getElementById("add_hours_div")
    add_hours_div.classList.remove("hidden")
    const chosen_date_label = document.getElementById("hours_label")
    const formatted_date = formatCalendar(date_element.textContent)
    const formatted_month = formatCalendar(month_index+1)
    chosen_date_label.textContent = formatted_date + " / " + formatted_month + " / " + year
    document.getElementById("hours_input").focus()

    hours_form = document.getElementById("hours_form")
    hours_form.addEventListener("submit", () =>{
           mark_dict_json = JSON.stringify(mark_dict)
           document.getElementById("mark_dict_input").value = mark_dict_json
       }
    )
}
function hideAddHoursDiv(){
    const add_hours_div = document.getElementById("add_hours_div")
    add_hours_div.classList.add("hidden")
    backdrop.classList.add("hidden")
    backdrop.removeEventListener("click", hideAddHoursDiv)
}
