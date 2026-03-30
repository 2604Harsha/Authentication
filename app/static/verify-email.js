function getTokenFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("token");
}

async function verifyEmail() {
    const token = getTokenFromURL();

    const icon = document.getElementById("icon");
    const title = document.getElementById("title");
    const message = document.getElementById("message");

    if (!token) {
        icon.innerHTML = "❌";
        title.innerText = "Invalid Link";
        message.innerText = "Verification token missing";
        message.className = "status yellow";
        return;
    }

    try {
        const res = await fetch(`/auth/verify-email?token=${encodeURIComponent(token)}`);

        if (!res.ok) throw new Error("Verification failed");

        const data = await res.json();

        icon.innerHTML = "✅";
        title.innerText = "Email Verified!";
        message.innerText = data.message;
        message.className = "status green";

    } catch (err) {
        icon.innerHTML = "❌";
        title.innerText = "Verification Failed";
        message.innerText = "Token expired or invalid";
        message.className = "status yellow";
    }
}

verifyEmail();
