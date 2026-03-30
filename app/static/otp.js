let userEmail = "";

async function sendOTP() {
    const email = document.getElementById("email").value;
    const message = document.getElementById("message");

    if (!email) {
        message.innerText = "Please enter email";
        return;
    }

    userEmail = email;

    try {
        const res = await fetch(
            `/auth/login-otp?email=${encodeURIComponent(email)}`,
            {
                method: "POST"
            }
        );

        const data = await res.json();

        if (!res.ok) {
            message.innerText = data.detail || "Failed to send OTP";
            return;
        }

        message.innerText = "OTP sent to your email ✅";
        document.getElementById("step-email").style.display = "none";
        document.getElementById("step-otp").style.display = "block";

    } catch (err) {
        message.innerText = "Server error";
    }
}

async function verifyOTP() {
    const otp = document.getElementById("otp").value;
    const message = document.getElementById("message");

    if (!otp) {
        message.innerText = "Enter OTP";
        return;
    }

    try {
        const res = await fetch(
            `/auth/verify-otp?email=${encodeURIComponent(userEmail)}&otp=${encodeURIComponent(otp)}`,
            {
                method: "POST"
            }
        );

        const data = await res.json();

        if (!res.ok) {
            message.innerText = data.detail || "Invalid OTP";
            return;
        }

        // ✅ Save JWT token
        localStorage.setItem("access_token", data.access_token);

        message.innerText = "Login successful 🎉";

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 1000);

    } catch (err) {
        message.innerText = "Server error";
    }
}
