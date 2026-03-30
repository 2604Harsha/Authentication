const token = new URLSearchParams(window.location.search).get("token");

fetch(`http://127.0.0.1:8000/auth/verify-email?token=${token}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;
    });
