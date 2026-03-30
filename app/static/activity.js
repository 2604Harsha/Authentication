const token = localStorage.getItem("access_token");

if (!token) {
    window.location.replace("/");
}

const activityList = document.getElementById("activityList");

fetch("http://127.0.0.1:8000/auth/login-history", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
})
.then(res => {
    if (!res.ok) {
        throw new Error(res.status);
    }
    return res.json();
})
.then(data => {
    activityList.innerHTML = "";

    if (data.length === 0) {
        activityList.innerHTML = "<p>No login activity found.</p>";
        return;
    }

    data.forEach(item => {
        const date = new Date(item.logged_in_at).toLocaleString();

        const div = document.createElement("div");
        div.className = "activity-item";

        div.innerHTML = `
            <span class="dot"></span>
            <div>
                <p class="activity-text">Logged in successfully</p>
                <small>${date}</small>
                ${item.ip_address ? `<small>IP: ${item.ip_address}</small>` : ""}
                ${item.user_agent ? `<small>Device: ${item.user_agent}</small>` : ""}
            </div>
        `;

        activityList.appendChild(div);
    });
})
.catch(err => {
    console.error("Activity error:", err);
    activityList.innerHTML = "<p>Failed to load activity.</p>";
});
