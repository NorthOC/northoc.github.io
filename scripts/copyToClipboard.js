function copyToClipboard(element_id) {
    navigator.clipboard.writeText("rev.denisas@gmail.com");
    let btn = document.getElementById(element_id);
    btn.innerHTML = "Copied!";
    btn.style.backgroundColor = "var(--green1)"
};