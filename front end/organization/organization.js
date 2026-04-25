const API_URL = "http://127.0.0.1:8000/";

async function load_organization(){
    let token = localStorage.getItem("token");
    let urlParams = new URLSearchParams(window.location.search);
    let org_id = urlParams.get("org_id");
    let response = await fetch(API_URL + "organizations/" + org_id + "/",{
        method: "GET",
        headers: {
            "Authorization": "Token " + token
        }
    })
    let data = await response.json();
    if (response.status == 200){
        document.getElementById("organization-name").innerHTML = data.name;
        document.getElementById("balance").innerHTML = "Balance: " + data.balance + " $";
        load_members(org_id);
        load_transactions(org_id);
    }
    else{
        document.getElementById("org-name").innerHTML = "Failed to load organization details.";
    }
}

async function load_transactions(org_id){
    let response = await fetch(API_URL + "organization/" + org_id + "/transactions/",{
        method: "GET",
        headers: {
            "Authorization": "Token " + localStorage.getItem("token")
        }
    })
    let data = await response.json();
    if (response.status == 200){
        let transactions_div = document.getElementById("recent-transactions");
        transactions_div.innerHTML = "";
        if (data.length == 0){
            transactions_div.innerHTML = `<div class="no-transactions">No transactions found for this organization</div>`;
            return;
        }
        for (let transaction of data){
            let transaction_div = document.createElement("div");
            if (transaction.receiver_bank_account_id == org_id){
                transaction_div.className = "transaction incoming";
            }
            transaction_div.className = "transaction";
            transaction_div.innerHTML = `
                <h3>${transaction.amount} $</h3>
                <p>${transaction.description}</p>
                <p>From: ${transaction.sender_bank_account_id} To: ${transaction.receiver_bank_account_id}</p>
                <p>${new Date(transaction.timestamp).toLocaleString()}</p>
                `
            transactions_div.appendChild(transaction_div);
        }

        
    }
}

async function load_members(org_id){
    let response = await fetch(API_URL + "organization/" + org_id + "/members/",{
        method: "GET",
        headers: {
            Authorization: "Token " + localStorage.getItem("token")
        }
    })
    let data = await response.json();
    console.log(data)
    if (response.status == 200){
        let members_div = document.getElementById("members");
        members_div.innerHTML = "";
        let members_list = document.createElement("ul");
        members_list.className = "members-list";
        for (let member of data.members){
            let member_li = document.createElement("li");
            member_li.className = "member";
            member_li.innerHTML = member;
            members_list.appendChild(member_li);
        }
        members_div.appendChild(members_list);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    load_organization();
})