const API_URL = "https://acb-production.up.railway.app/";

document.addEventListener("DOMContentLoaded", async function() {
    let token = localStorage.getItem("token");
    if (token == null){
        window.location.href = "../login/login.html";
        return;
    }
    let user_id = localStorage.getItem("user_id");
    try {
        let response = await fetch(API_URL + "users/" + user_id + "/",{
            method: "GET",
            headers: {
                "Authorization": "Token " + token
            }
        })
        let data = await response.json();
        if (response.status == 200){
            if (!data.is_super_admin){
                window.location.href = "../dashboard/dashboard.html";
                return;
            }
            await load_pending_organizations();
        }
    }
    catch (error){
        window.location.href = "../login/login.html";
        return;
    }
})

async function load_pending_organizations(){
    document.getElementById("pending-organizations").innerHTML = `<div class="loading">Loading pending organizations ...</div>`;
    try {
        let response = await fetch(API_URL + "pending_organizations/",{
            method: "GET",
            headers: {
                "Authorization": "Token " + localStorage.getItem("token")
            }
        })
        let data = await response.json();
        if (data.length == 0){
            document.getElementById("pending-organizations").innerHTML = '<div class="no-organizations">There are no pending organizations at the moment.</div>';
        }
        else {
            document.getElementById("pending-organizations").innerHTML = "";
            for (let org of data){
                console.log(org)
                let org_div = document.createElement("div");
                org_div.className = "pending-organization";
                org_div.innerHTML = `
                    <h3>${org.name}</h3>
                    <p>${org.description}</p>
                    <button class="approve-btn" data-id="${org.name}">Approve</button>
                    <button class="reject-btn" data-id="${org.name}">Reject</button>
                `
                document.getElementById("pending-organizations").appendChild(org_div);
            }
            document.querySelectorAll(".approve-btn").forEach(button => {
                button.addEventListener("click", approve_organization);
            })
            document.querySelectorAll(".reject-btn").forEach(button => {
                button.addEventListener("click", reject_organization);
            })
        }
    }
    catch (error){
        console.log(error)
        document.getElementById("pending-organizations").innerHTML = '<div class="error">An error occurred while loading pending organizations. Please try again later.</div>';
    }
}

async function approve_organization(event){
    let organization_name = event.target.getAttribute("data-id");
    let response = await fetch(API_URL + "approve_organization/" + organization_name + "/",{
        method: "POST",
        headers: {
            "Authorization": "Token " + localStorage.getItem("token"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem("token")
        }) 
    })
    let data = await response.json();
    console.log(data);
}

async function reject_organization(event){}

