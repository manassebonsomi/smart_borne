async function generateResult(){

    const userId =
        localStorage.getItem(
            "user_id"
        );

    const result =
        await apiGet(

            `/recommandation/${userId}`
        );

    document
        .getElementById(
            "result"
        )
        .innerHTML =

        `
        <h2>

            ${
                result.data.profil_detecte
            }

        </h2>

        <p>

            Score :

            ${
                result.data.score
            }

        </p>
        `;
}

generateResult();