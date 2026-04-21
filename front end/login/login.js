const API_URL = "http://127.0.0.1:8000/";

async function login(){
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let response = await fetch(API_URL + "login/",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    msg_area = document.getElementById("message-area");
    let data = await response.json();
    if(response.status == 200){
        if (data.logged_in){ 
            msg_area.innerHTML = "You have logged in, You will be redirected in 5 seconds";
            msg_area.className = "message-area success";
            setTimeout(function(){
                localStorage.setItem("token", data.token);
                window.location.href = "../dashboard/dashboard.html";
            }, 5000);

        }
        else{
            msg_area.innerHTML = data.error;
            msg_area.className = "message-area error";
        }
    }
    else{
        msg_area.innerHTML = data.detail;
        msg_area.className = "message-area error";
    }
}

document.getElementById("submit-btn").addEventListener("click", function(event) {
    event.preventDefault();
    event.stopPropagation();
    login(event);
});

document.getElementById("login-form").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        login(event);
    }
});
