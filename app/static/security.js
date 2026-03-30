const token = localStorage.getItem("access_token");

// protect page
if (!token) {
    window.location.replace("/");
}

function changePassword() {
    const current = document.getElementById("currentPassword").value;
    const next = document.getElementById("newPassword").value;
    const confirm = document.getElementById("confirmPassword").value;
    const msg = document.getElementById("passwordMessage");

    msg.innerText = "";
    msg.style.color = "white";

    if (!current || !next || !confirm) {
        msg.innerText = "All fields are required";
        msg.style.color = "#ffd633";
        return;
    }

    if (next !== confirm) {
        msg.innerText = "Passwords do not match";
        msg.style.color = "#ff4d4d";
        return;
    }

    // UI-only (backend can be added later)
    msg.innerText = "Password updated successfully (UI only)";
    msg.style.color = "#4dff88";

    // clear inputs
    document.getElementById("currentPassword").value = "";
    document.getElementById("newPassword").value = "";
    document.getElementById("confirmPassword").value = "";
}
