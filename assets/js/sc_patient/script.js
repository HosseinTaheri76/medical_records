function login(patient) {
    let time = new Date();
    let cookie_value = patient.getAttribute('data-code');
    time.setTime(time.getTime() + (1000 * 24 * 60 * 60 * 7));
    time.toUTCString();
    document.cookie = "p_code=" + cookie_value + ";expires=" + time + ";path=/";
    window.location.assign("/");
}

