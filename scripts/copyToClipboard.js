function copyToClipboard(element_id) {
    navigator.clipboard.writeText("rev.denisas@gmail.com");
    let btn = document.getElementById(element_id);
    btn.innerHTML = "Copied!";
    btn.style.boxShadow = "0px 0px 1px 1px var(--fa-pip2)"
    btn.style.color = "var(--fa-pip2)"
};