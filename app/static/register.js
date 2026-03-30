document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        role: document.getElementById("role").value
    };

    console.log(payload); // 🔥 MUST SEE THIS IN BROWSER CONSOLE

    const res = await fetch("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log(data);

    document.getElementById("message").innerText =
        res.ok ? "Success" : JSON.stringify(data.detail);
});
