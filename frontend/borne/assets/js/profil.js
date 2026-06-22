document.getElementById("profileForm").addEventListener("submit", async function (e) {
            e.preventDefault();
            const age = parseInt(document.getElementById("age").value);
            let profil = "ENFANT";
            if (age >= 13) {
                profil = "ADOLESCENT";
            }
            try {

                /*
                CREATION UTILISATEUR
                */

                const userResponse =
                    await apiPost("/utilisateurs",
                        {
                            nom:document.getElementById("nom").value,
                            prenom:document.getElementById("prenom").value,
                            age:age,
                            niveau_scolaire:document.getElementById("niveau").value,
                            type_profil:profil,
                            id_ville:1
                        }
                    );

                const userId = userResponse.id_utilisateur;
                localStorage.setItem("user_id", userId);

                /*
                CREATION SESSION
                */

                const sessionResponse =
                    await apiPost(
                        "/session/start",
                        {
                            id_utilisateur: userId,
                            id_campagne: null
                        }
                    );

                const sessionId = sessionResponse.data.id_session;
                localStorage.setItem("session_id", sessionId);

                /*
                QUESTIONNAIRE
                */
                window.location = "questionnaire.html";

            }

            catch (error) {
                console.error(error);
                alert("Erreur création profil");
            }
        }
    );