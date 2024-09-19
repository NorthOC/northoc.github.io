DARK_THEME_VAL = "theme-dark"
LIGHT_THEME_VAL = "theme-light"

DARK_THEME_LABEL = "Theme: Dark"
LIGHT_THEME_LABEL = "Theme: Light"

function check_theme(){
    if (localStorage.getItem("theme") == null || localStorage.getItem("theme") == DARK_THEME_VAL){
        localStorage.setItem("theme", DARK_THEME_VAL);
        set_theme(DARK_THEME_LABEL);
    } else{
        set_theme(LIGHT_THEME_LABEL);
    }
}
function toggle_theme(){
    if(localStorage.getItem("theme") == LIGHT_THEME_VAL){
        localStorage.setItem("theme", DARK_THEME_VAL);
        set_theme(DARK_THEME_LABEL);
    }
    else{
        localStorage.setItem("theme", LIGHT_THEME_VAL);
        set_theme(LIGHT_THEME_LABEL);
    }
}

function set_theme(html_text){
    document.documentElement.className = localStorage.getItem("theme");
    let elem = document.getElementById("theme-toggler")
    elem.innerHTML = html_text;
}