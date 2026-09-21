
// Global variables
let backdrop
let mark_dict
let remove_dict
const months = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]
let user_curr_date
let markable

//DOM_LOAD
document.addEventListener("DOMContentLoaded", function(){

    if(document.getElementById("nav_menu")){
        backdrop = document.getElementById("backdrop")
        showMenuNav()
        showSearchNav()
        addUserNavListener()
        pfpPicker()
    }
    if(document.getElementById("landing_page_body")){
        textTyping()
    }
    if(document.getElementById("calendar")){
        mark_dict_json = document.getElementById("mark_dict_input").value
        mark_dict = JSON.parse(mark_dict_json)
        remove_dict = {}
        user_curr_date = new Date()
        markable = document.getElementById("markable_input").value
        calendarNavigation()
        centerWorkName()
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
function addUserNavListener(){
    const pfp = document.getElementById("pfp_div")
    pfp.onclick = showUserNav
}
function showUserNav(event){
      event.stopPropagation()
      const pfp = document.getElementById("pfp_div")
      const user_nav_div = document.getElementById("user_navigation");
      const pfp_nav_info = document.getElementById("pfp_nav_info");
      user_nav_div.classList.remove("hidden")
      pfp_nav_info.style.display = "none";
      pfp_nav_info.textContent = "Close user navigation menu"
      pfp.onmouseleave = showPfpNavInfo
      user_nav_div.onclick=function(event){
          event.stopPropagation()
      }
      pfp.onclick = hideUserNav
      document.body.onclick = function(){
          hideUserNav()
          showPfpNavInfo()
          console.log("whyyy")
      }
}

function hideUserNav(){
    const user_nav_div = document.getElementById("user_navigation");
    user_nav_div.classList.add("hidden")
    const pfp_nav_info = document.getElementById("pfp_nav_info")
    pfp_nav_info.style.display = "none";
    pfp_nav_info.textContent = "Open user navigation menu"
    pfp = document.getElementById("pfp_div")
    pfp.onclick = showUserNav
    document.body.onclick = null
}

function showPfpNavInfo(){
    // when calling showUserNav we make the pfp_nav_info to display:none, so when mouse leaves pfp - we remove that style
    document.getElementById("pfp_nav_info").style.removeProperty('display');
}
function showMenuNav(){
    const menu = document.getElementById("menu_div")
    menu.onclick= function() {
        const menu_nav_div = document.getElementById("menu_navigation")
        const close_icon_div = document.getElementById("close_icon_div")
        menu_nav_div.classList.remove("hidden")
        close_icon_div.onclick = hideMenuNav
        backdrop.classList.remove("hidden")
        backdrop.onclick = function(){
            hideMenuNav()
            const friends = document.getElementsByClassName("nav_button_name")
            for(let i =0; i<friends.length; i++){
                let fr = friends[i]
                if(fr.scrollWidth > fr.clientWidth){
                    console.log(fr.textContent, " ", overflow)
                }
                else{
                    console.log("no overflows")
                }

            }
        }
    }

}

function hideMenuNav(){
    const menu_nav_div = document.getElementById("menu_navigation");
    menu_nav_div.classList.add("hidden")
    backdrop.classList.add("hidden")
    backdrop.onclick = null
}
function showSearchNav(){
    const search_div = document.getElementById("search_div")
    search_div.onclick= function(){
        const search_nav_div = document.getElementById("search_navigation")
        search_nav_div.classList.remove("hidden")
        backdrop.classList.remove("hidden")
        backdrop.onclick = hideSearchNav
        document.getElementById("search_user").focus()
    }

}
function hideSearchNav(){
    search_div = document.getElementById("search_navigation")
    search_div.classList.add("hidden")
    backdrop.classList.add("hidden")
    backdrop.onclick = null

}

function pfpPicker(){
    const pfp_picker_input = document.getElementById("pfp_picker")
    const pfp_picker_form = document.getElementById("pfp_picker_form")
    pfp_picker_input.onchange = ()=>{pfp_picker_form.submit()}

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
        if (j>=0 && j%4!==0){
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
    let current_date
    const month_year_input = document.getElementById("month_year_input")
    if(month_year_input === null || month_year_input.value ===""){
        current_date = user_curr_date
        console.log(user_curr_date.getMonth())
        generateCalendarContent(user_curr_date)
    }
    else{
        const month_year = month_year_input.value.split(",")
        const month_index = month_year[0]
        const year = month_year[1]
        current_date = new Date(year, month_index)
        generateCalendarContent(current_date)
        console.log("wtf")
    }


    const left_arrow = document.getElementById("calendar_prev")
    const right_arrow = document.getElementById("calendar_next")

    left_arrow.onclick = function(){
        current_date = new Date(current_date.getFullYear(), current_date.getMonth()-1)
        generateCalendarContent(current_date)
    }

    right_arrow.onclick= function () {
        current_date = new Date(current_date.getFullYear(), current_date.getMonth() + 1)
        generateCalendarContent(current_date)
    }
}
function generateCalendarContent(date_obj){
    const date_info = getDateInfo(date_obj)
    document.getElementById("month_and_year").textContent = date_info.get("month_and_year_text")

    const calendar_total_dates = 42
    const calendar_dates = document.getElementById("calendar_dates_list")
    let month_year = date_info.get("month_year")
    const current_month_index = month_year[0]
    const current_year = month_year[1]
    month_year = String(month_year)

    let inner_dict
    if(!mark_dict[month_year]){
        inner_dict = {"left":[[], []], "current":[[], []], "right":[[], []]}
        mark_dict[month_year] =  inner_dict
    }
    else{
        inner_dict = mark_dict[month_year]
    }
    const left_marks = inner_dict["left"]
    const current_marks = inner_dict["current"]
    const right_marks = inner_dict["right"]

    calendar_dates.innerHTML = ""

    const first_day_index = date_info.get("first_day_index")
    const previous_month_final_date = date_info.get("previous_final_date")
    for (let i=0; i<first_day_index; i++){
        const calendar_date = document.createElement("li")
        const previous_month_date = previous_month_final_date-first_day_index+1+i
        const date_text = document.createTextNode(String(previous_month_date))
        calendar_date.appendChild(date_text)
        calendar_date.classList.add("calendar_date", "left")
        if(left_marks[0].includes(calendar_date.textContent)){
            renderMarkedDate(calendar_date, date_obj)
        }
        calendar_dates.appendChild(calendar_date)
    }
    const final_date = date_info.get("final_date")
    for(let i=1; i<=final_date; i++){
        const calendar_date = document.createElement("li")
        const date_text = document.createTextNode(String(i))
        calendar_date.appendChild(date_text)
        calendar_date.classList.add("calendar_date", "current")
        if(current_marks[0].includes(calendar_date.textContent)){
            renderMarkedDate(calendar_date,  date_obj)
        }
        calendar_dates.appendChild(calendar_date)
    }
    const already_added_dates = first_day_index + final_date
    const remaining_dates = calendar_total_dates - already_added_dates
    for(let i =0; i<remaining_dates; i++){
        const calendar_date = document.createElement("li")
        const date_text = document.createTextNode(String(i+1))
        calendar_date.appendChild(date_text)
        calendar_date.classList.add("calendar_date", "right")
        if(right_marks[0].includes(calendar_date.textContent)){
            renderMarkedDate(calendar_date, date_obj)
        }
        calendar_dates.appendChild(calendar_date)
    }
    month_year_input = document.getElementById("month_year_input")
    if(month_year_input !== null){
        month_year_input.value = month_year
    }


    if(markable==="true"){
        document.querySelectorAll(".calendar_date").forEach(
        calendar_date => {
            if(isFutureDate(calendar_date, date_obj)){
                calendar_date.classList.add("future")
                calendar_date.onclick = invalidDate
            }
            else if(!calendar_date.classList.contains("marked")){
                calendar_date.date_obj = date_obj
                calendar_date.onclick = showHoursForm
                calendar_date.onmouseover = function(){calendar_date.style.cursor = "pointer"}
            }
          }
        )
    }

}
function isFutureDate(calendar_date, date_obj){
    const calendar_date_info_Div = calendar_date.firstElementChild
    let removed="false"
    if(calendar_date_info_Div){
        //doing this because info_Div's text content goes into calendar_date's text content. remove to prevent
        calendar_date.removeChild(calendar_date_info_Div)
        removed = "true"
    }

    const date_info = getDateInfo(date_obj)
    const month_year = date_info.get("month_year")
    const prev_month_year = date_info.get("prev_month_year")
    const next_month_year = date_info.get("next_month_year")
    let validation
    const user_year = user_curr_date.getFullYear()
    const user_month = user_curr_date.getMonth()
    const user_date = user_curr_date.getDate()
    switch(calendar_date.classList[1]){
        case "current":
            validation = (
                 month_year[1] > user_year ||
                 (month_year[1] === user_year && month_year[0] >user_month) ||
                 (month_year[1] === user_year && month_year[0] === user_month && parseInt(calendar_date.textContent) > user_date)
            )
            break;
        case "left":
            validation = (
                prev_month_year[1] > user_year ||
                (prev_month_year[1] === user_year && prev_month_year[0] > user_month) ||
                (prev_month_year[1] === user_year && prev_month_year[0] === user_month && parseInt(calendar_date.textContent) > user_date)
            )
            break;
        case "right":
            validation = (
                next_month_year[1] > user_year ||
                (next_month_year[1] === user_year && next_month_year[0] > user_month) ||
                (next_month_year[1] === user_year && next_month_year[0] === user_month && parseInt(calendar_date.textContent) > user_date)
            )
            break;
    }
    //Bandaid solution for bigger problem. InfoDiv and X affect textContent.
    // this makes the check for calendar_date.textContent vs user_date fucked up. i dont know what to do about textContent checks..
    if(removed==="true"){
        calendar_date.appendChild(calendar_date_info_Div)
    }
    return validation
}

function showHoursForm(event){

    const calendar_date = event.currentTarget
    const date_obj = calendar_date.date_obj
    const date_info = getDateInfo(date_obj)
    const date_text = calendar_date.textContent
    let month_year = date_info.get("month_year")
    let prev_month_year = date_info.get("prev_month_year")
    let next_month_year = date_info.get("next_month_year")

    backdrop.classList.remove("hidden")
    backdrop.onclick = hideHoursForm
    const add_hours_div = document.getElementById("add_hours_div")
    add_hours_div.classList.remove("hidden")
    const chosen_date_label = document.getElementById("hours_label")
    const formatted_date = formatCalendar(date_text)

    let formatted_month
    let year
    switch(calendar_date.classList[1]){
        case "left":
            formatted_month = formatCalendar(prev_month_year[0]+1)
            year = prev_month_year[1]
            break;
        case "current":
            formatted_month = formatCalendar(month_year[0]+1)
            year = month_year[1]
            break;
        case "right":
            formatted_month = formatCalendar(next_month_year[0]+1)
            year = next_month_year[1]
            break
        }
    chosen_date_label.textContent = formatted_date + " / " + formatted_month + " / " + year

    month_year = String(month_year)
    prev_month_year = String(prev_month_year)
    next_month_year = String(next_month_year)
    const hours_input= document.getElementById("hours_input")
    hours_input.focus()
    const hours_form = document.getElementById("hours_form")
    hours_form.onsubmit = function() {
        const hours = parseInt(hours_input.value)
        if(!Number.isInteger(hours)){
            hours_input.value = "invalid"
        }
        else{
            switch (calendar_date.classList[1]) {
            case "left":
                mark_dict[month_year]["left"][0].push(date_text)
                mark_dict[month_year]["left"][1].push(hours)
                if (!mark_dict[prev_month_year]) {
                    const inner_dict_prev = {"left": [[], []], "current": [[date_text], [hours]], "right": [[], []]}
                    mark_dict[prev_month_year] = inner_dict_prev
                } else {
                    const inner_dict_prev = mark_dict[prev_month_year]
                    const current_marks_prev = inner_dict_prev["current"]
                    current_marks_prev[0].push(calendar_date.textContent)
                    current_marks_prev[1].push(hours)
                }
                break;
            case "current":
                mark_dict[month_year]["current"][0].push(date_text)
                mark_dict[month_year]["current"][1].push(hours)
                date_value = parseInt(date_text)
                if (date_value < 15) {
                    if (!mark_dict[prev_month_year]) {
                        const inner_dict_prev = {"left": [[], []], "current": [[], []], "right": [[date_text], [hours]]}
                        mark_dict[prev_month_year] = inner_dict_prev
                    } else {
                        const inner_dict_prev = mark_dict[prev_month_year]
                        const right_marks_prev = inner_dict_prev["right"]
                        right_marks_prev[0].push(date_text)
                        right_marks_prev[1].push(hours)
                    }
                } else if (date_value >= 23) {
                    if (!mark_dict[next_month_year]) {
                        const inner_dict_next = {"left": [[date_text], [hours]], "current": [[], []], "right": [[], []]}
                        mark_dict[next_month_year] = inner_dict_next
                    } else {
                        const inner_dict_next = mark_dict[next_month_year]
                        const left_marks_next = inner_dict_next["left"]
                        left_marks_next[0].push(date_text)
                        left_marks_next[1].push(hours)
                    }
                }
                break;
            case "right":
                mark_dict[month_year]["right"][0].push(date_text)
                mark_dict[month_year]["right"][1].push(hours)
                if (!mark_dict[next_month_year]) {
                    const inner_dict_next = {"left": [[], []], "current": [[date_text], [hours]], "right": [[], []]}
                    mark_dict[next_month_year] = inner_dict_next
                } else {
                    const inner_dict_next = mark_dict[next_month_year]
                    const current_marks_next = inner_dict_next["current"]
                    current_marks_next[0].push(date_text)
                    current_marks_next[1].push(hours)
                }
                break;
            }
            mark_dict_json = JSON.stringify(mark_dict)
            document.getElementById("mark_dict_input").value = mark_dict_json
        }
      }
    console.log(mark_dict)
}
function hideHoursForm(){
    const hours_input = document.getElementById("hours_input")
    hours_input.value = ""
    const add_hours_div = document.getElementById("add_hours_div")
    add_hours_div.classList.add("hidden")
    backdrop.classList.add("hidden")
    backdrop.onclick = null
}
function formatCalendar(date_or_month){
    if(date_or_month<10){
        return "0" + date_or_month
    }
    else{
        return String(date_or_month)
    }
}
function invalidDate(){
    alert("Can not mark future dates!")
}

function renderMarkedDate(calendar_date, date_obj){
     const date_text = calendar_date.textContent
     const date_info = getDateInfo(date_obj)
     const month_year = String(date_info.get("month_year"))
     let position = calendar_date.classList[1]
     calendar_date.classList.add("marked")
     const infoDiv = document.createElement("div")
     const index = mark_dict[month_year][position][0].indexOf(calendar_date.textContent)
     const hours = mark_dict[month_year][position][1][index]
     infoDiv.textContent = String(hours)
     if(hours===undefined){
         infoDiv.textContent=""
     }
     infoDiv.classList.add("infoDiv")
     infoDiv.classList.add("hidden")
     calendar_date.appendChild(infoDiv)

     const removeDiv = document.createElement("img")
     removeDiv.src = "../static/website_images/close_req_icon.png"
     removeDiv.classList.add("remove_div")
     removeDiv.classList.add("hidden")

     const prev_month_year = String(date_info.get("prev_month_year"))
     const next_month_year = String(date_info.get("next_month_year"))
     removeDiv.onclick = function(){
            switch(position){
                case "left":
                    remove_dict[month_year] = ["left", date_text]
                    remove_dict[prev_month_year] = ["current", date_text]
                    break
                case "right":
                    remove_dict[month_year] = ["right", date_text]
                    remove_dict[next_month_year] = ["current", date_text]
                    break
                case "current":
                    remove_dict[month_year] = ["current", date_text]
                    date_value = parseInt(date_text)
                    if(date_value<15){
                        remove_dict[prev_month_year] = ["right", date_text]
                    }
                    else if(date_value>23){
                        remove_dict[next_month_year] = ["left", date_text]
                    }
            }
            const remove_dict_json = JSON.stringify(remove_dict)
            document.getElementById("remove_dict_input").value = remove_dict_json
            document.getElementById("hours_input").value = String(-hours)
            console.log(document.getElementById("remove_dict_input").value)
            document.getElementById("hours_form").submit()
     }

     calendar_date.appendChild(removeDiv)
     calendar_date.onmouseover = function() {
         infoDiv.classList.remove("hidden")
         removeDiv.classList.remove("hidden")
     }
     calendar_date.onmouseleave = function(){
               infoDiv.classList.add("hidden")
               removeDiv.classList.add("hidden")
     }

}

function getDateInfo(date_obj){
    const month_date = date_obj.getDate()
    const month_index =date_obj.getMonth()
    const month = months[month_index]
    const year = date_obj.getFullYear()
    const month_and_year_text = month + " " + year
    const final_date = new Date(year, month_index+1, 0).getDate()
    const first_day_index = new Date(year, month_index, 1).getDay()
    const previous_final_date = new Date(year, month_index, 0).getDate()
    const month_year = [month_index, year]

    const prev_date = new Date(year, month_index-1)
    const prev_month_year = [prev_date.getMonth(), prev_date.getFullYear()]
    const next_date = new Date(year, month_index+1)
    const next_month_year = [next_date.getMonth(), next_date.getFullYear()]

    const date_info_map = new Map()
    date_info_map.set("month_index", month_index)
    date_info_map.set("month", month)
    date_info_map.set("year", year)
    date_info_map.set("month_and_year_text", month_and_year_text)
    date_info_map.set("final_date", final_date)
    date_info_map.set("previous_final_date", previous_final_date)
    date_info_map.set("first_day_index", first_day_index)
    date_info_map.set("month_year", month_year)
    date_info_map.set("prev_date", prev_date)
    date_info_map.set("prev_month_year", prev_month_year)
    date_info_map.set("next_date", next_date)
    date_info_map.set("next_month_year", next_month_year)

    return date_info_map
}

function centerWorkName(){
    const workname = document.getElementById("work_name")
    const workname_len = workname.textContent.length
    let fixed = false
    let len = 2
    let base_margin = 1.3
    let increment = 0.1


    while(fixed === false && len <=workname_len){
        base_margin = base_margin-increment
        if(len===workname_len){
            workname.style.marginLeft = `-${base_margin}rem`
            fixed = true
            console.log("-", base_margin)
            break
        }

        len = len +1
        console.log(len, " length")
    }
}