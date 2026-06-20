document
    .getElementById(
        "profileForm"
    )
    .addEventListener(
        "submit",

        async function(e) {

            e.preventDefault();

            const age =
                parseInt(
                    document
                    .getElementById(
                        "age"
                    )
                    .value
                );

            let profil =
                "ENFANT";

            if(age >= 13){

                profil =
                    "ADOLESCENT";
            }

            const response =
                await apiPost(

                    "/utilisateurs",

                    {

                        nom:
                            document
                            .getElementById(
                                "nom"
                            ).value,

                        prenom:
                            document
                            .getElementById(
                                "prenom"
                            ).value,

                        age:
                            age,

                        niveau_scolaire:
                            document
                            .getElementById(
                                "niveau"
                            ).value,

                        type_profil:
                            profil,

                        id_ville:
                            1
                    }
                );

            localStorage.setItem(

                "user_id",

                response.data.id_utilisateur
            );

            window.location =
                "questionnaire.html";
        }
    );