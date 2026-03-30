const resetForm = document.getElementById("resetForm");
const message = document.getElementById("message");

resetForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    message.textContent = "Resetting password...";
    message.style.color = "#94a3b8";

    try {
        const response = await fetch("/auth/reset-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                new_password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Password reset failed";
            message.style.color = "#f87171";
            return;
        }

        message.textContent = "Password reset successful! Redirecting to login...";
        message.style.color = "#22c55e";

        setTimeout(() => {
            window.location.href = "/login";
        }, 1500);

    } catch (error) {
        console.error(error);
        message.textContent = "Server error. Please try again.";
        message.style.color = "#f87171";
    }
});
