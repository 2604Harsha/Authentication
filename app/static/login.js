const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    message.textContent = "Logging in...";
    message.style.color = "#94a3b8";

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // ✅ OAuth2 requires FORM DATA
    const formData = new URLSearchParams();
    formData.append("username", email);   // IMPORTANT
    formData.append("password", password);

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Login failed";
            message.style.color = "#f87171";
            return;
        }

        // ✅ Save tokens
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        message.textContent = "Login successful! Redirecting...";
        message.style.color = "#22c55e";

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 1000);

    } catch (err) {
        console.error(err);
        message.textContent = "Server error. Try again.";
        message.style.color = "#f87171";
    }
});
