function show(){
    let menu = document.getElementById('small-menu');
    if(menu.className === "sm-header-nav"){
        menu.className += " show";
    }
    else {
        menu.className = "sm-header-nav";
    }
}
function logout() {
    let time = new Date();
    time.setTime(time.getTime() - (1000 * 24 * 60 * 60));
    time.toUTCString();
    document.cookie = "p_code=null;expires=" + time + ";path=/";
    window.location.replace('/select-patient/');
}