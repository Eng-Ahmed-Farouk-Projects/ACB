const API_URL = "https://api.taskmaster.com/api/v1/";

document.addEventListener("DOMContentLoaded",async function(){
    let token = localStorage.getItem("token");
    if (token == null){
        window.location.href = "../login/login.html";
        return;
    }
    document.getElementById("create-organization-form").addEventListener("submit", async function (event){
        event.preventDefault();
        let name = document.getElementById("org-name").value;
        let description = document.getElementById("org-description").value;
        try {
            let response = await fetch("" + API_URL + "new_organization/",{
                name: name,
                description: description,
                owner_id: localStorage.getItem("user_id")
            })
            let data = await response.json();
            if (response.status == 200){
                
                window.location.href = "../dashboard/dashboard.html";
            }


        }
        catch (error){

        }
    })
})