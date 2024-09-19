function addCss(button) {
    var head = document.head;
    var link = document.createElement("link");
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = "https://denislisunov.xyz/static/style.css";
    head.appendChild(link);
    document.getElementById(button).style.visibility = "hidden"
}