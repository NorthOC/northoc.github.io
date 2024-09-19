FILTER_VAL = "none"
NO_FILTER_VAL = "block"
FILTER_LABEL = "Mode: SAFE"
NO_FILTER_LABEL = "Mode: WILD"
DISPLAY_STYLE_NONE = "hidden"
DISPLAY_STYLE_BLOCK = "block"

function check_filter(){
    if (localStorage.getItem("filter-mode") == null || localStorage.getItem("filter-mode") == FILTER_VAL){
        localStorage.setItem("filter-mode", FILTER_VAL);
        set_filter(FILTER_LABEL);
    } else{
        set_filter(NO_FILTER_LABEL);
    }
}
function toggle_filter(){
    if(localStorage.getItem("filter-mode") == NO_FILTER_VAL){
        localStorage.setItem("filter-mode", FILTER_VAL);
        set_filter(FILTER_LABEL);
    }
    else{
        localStorage.setItem("filter-mode", NO_FILTER_VAL);
        set_filter(NO_FILTER_LABEL);
    }
}

function set_filter(html_text){
    let filter_type = localStorage.getItem("filter-mode");
    let elems = document.getElementsByClassName("filtered");


    for (let element of elems) {
        element.style.display = filter_type;
        let warning = document.createElement("p")
        warning.className = "warning"
        warning.innerHTML = "TRIGGER WARNING"
        element.appendChild(warning);
    };

    let elem = document.getElementById("filter-toggler")
    elem.innerHTML = html_text;
}