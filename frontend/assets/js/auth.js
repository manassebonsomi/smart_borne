async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const result =
        await apiPost("/auth/login",
            {
                email: email,
                mot_de_passe: password
            }
        );

    if (result.success) {
        localStorage.setItem("token", result.token
        );
        window.location = "dashboard.html";
    }

    else {
        alert("Connexion refusée");
    }
}