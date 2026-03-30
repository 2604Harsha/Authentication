function getTokenFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("token");
}

async function resetPassword() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const message = document.getElementById("message");
    const token = getTokenFromURL();

    if (!token) {
        message.innerText = "Invalid or missing reset token";
        return;
    }

    if (!password || !confirmPassword) {
        message.innerText = "All fields are required";
        return;
    }

    if (password !== confirmPassword) {
        message.innerText = "Passwords do not match";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/auth/password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: token,
                new_password: password,
                confirm_password: confirmPassword
            })
        });

        const data = await res.json();

        if (!res.ok) {
            message.innerText = data.detail || "Password reset failed";
        } else {
            message.style.color = "green";
            message.innerText = "Password updated successfully! Redirecting...";
            setTimeout(() => {
                window.location.href = "/login.html";
            }, 2000);
        }
    } catch (err) {
        message.innerText = "Server error. Try again.";
    }
}
