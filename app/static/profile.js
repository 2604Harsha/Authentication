const token = localStorage.getItem("access_token");

// protect page
if (!token) {
    window.location.replace("/");
}

// load user data
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
    document.getElementById("name").value = user.name;
    document.getElementById("email").value = user.email;
    document.getElementById("role").value = user.role;
})
.catch(() => {
    localStorage.clear();
    window.location.replace("/");
});

// edit/save logic (UI only)
const editBtn = document.getElementById("editBtn");
const saveBtn = document.getElementById("saveBtn");

const editableFields = [
    document.getElementById("name"),
    document.getElementById("email")
];

editBtn.addEventListener("click", () => {
    editableFields.forEach(f => f.disabled = false);
    editBtn.classList.add("hidden");
    saveBtn.classList.remove("hidden");
});

saveBtn.addEventListener("click", () => {
    editableFields.forEach(f => f.disabled = true);
    saveBtn.classList.add("hidden");
    editBtn.classList.remove("hidden");

    alert("Profile updated (UI only)");
});
