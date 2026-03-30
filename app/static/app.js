/* ===========================
   LOGIN
=========================== */
function login() {
    const email = document.getElementById("email")?.value.trim();
    const password = document.getElementById("password")?.value.trim();
    const error = document.getElementById("error");

    if (error) error.innerText = "";

    if (!email || !password) {
        if (error) error.innerText = "Email and password are required";
        return;
    }

    fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: email,
            password: password
        })
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        localStorage.setItem("access_token", data.access_token);

        // reset alert flag on fresh login
        sessionStorage.removeItem("back_alert_shown");

        window.location.replace("/dashboard");
    })
    .catch(() => {
        if (error) error.innerText = "Invalid email or password";
    });
}

/* ===========================
   STRONG DASHBOARD PROTECTION
=========================== */
(function protectDashboard() {
    const token = localStorage.getItem("access_token");

    if (window.location.pathname.includes("dashboard") && !token) {
        window.location.replace("/");
    }
})();

/* ===========================
   BACK BUTTON HANDLING
=========================== */
history.pushState(null, "", location.href);

window.addEventListener("popstate", function () {

    // show alert only once
    if (!sessionStorage.getItem("back_alert_shown")) {
        sessionStorage.setItem("back_alert_shown", "true");
        alert("Please login to continue");
    }

    // ALWAYS redirect (no dashboard access)
    window.location.replace("/");
});

/* ===========================
   FETCH USER DETAILS
=========================== */
const token = localStorage.getItem("access_token");

if (token && document.getElementById("username")) {
    fetch("http://127.0.0.1:8000/auth/me", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(user => {
        document.getElementById("username").innerText = user.name;
        document.getElementById("role").innerText = user.role;

        const hour = new Date().getHours();
        let greet = "Hello";
        if (hour < 12) greet = "Good Morning 🌅";
        else if (hour < 17) greet = "Good Afternoon ☀️";
        else greet = "Good Evening 🌙";

        document.getElementById("greeting").innerText = greet;
    })
    .catch(() => {
        localStorage.clear();
        window.location.replace("/");
    });
}

/* ===========================
   LOGOUT
=========================== */
function logout() {
    localStorage.clear();
    sessionStorage.removeItem("back_alert_shown");

    window.location.replace("/?msg=login");
}

/* ===========================
   SHOW LOGIN MESSAGE
=========================== */
(function showLoginMessage() {
    const params = new URLSearchParams(window.location.search);
    const error = document.getElementById("error");

    if (params.get("msg") === "login" && error) {
        error.innerText = "Please login again to continue";
    }
})();


/* ===========================
   CONFETTI (OPTIONAL)
=========================== */
function confettiBlast() {
    const colors = ["#ff4d4d", "#4da6ff", "#ffd633", "#4dff88"];

    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement("div");
        confetti.style.position = "absolute";
        confetti.style.width = "6px";
        confetti.style.height = "6px";
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.top = "0px";
        confetti.style.left = Math.random() * window.innerWidth + "px";
        confetti.style.opacity = 0.8;

        document.body.appendChild(confetti);

        confetti.animate(
            [
                { transform: "translateY(0)" },
                { transform: `translateY(${window.innerHeight}px)` }
            ],
            {
                duration: 3000,
                easing: "ease-out"
            }
        );

        setTimeout(() => confetti.remove(), 3000);
    }
}
