async function loadStats() {

    const stats =
        await apiGet(
            "/dashboard/statistics"
        );

      // console.log(stats.data.questions);

      const data =
        stats.data;

    document
        .getElementById(
            "stats"
        ).innerHTML =

        `
        <h3>
            Utilisateurs :
            ${data.utilisateurs}
        </h3>

        <h3>
            Sessions :
            ${data.sessions}
        </h3>

        <h3>
            Questions :
            ${data.questions}
        </h3>

        <h3>
            Recommandations :
            ${data.recommandations}
        </h3>
        `;
}


async function loadParcoursChart() {

    const response =
        await fetch(

            API_URL +
            "/dashboard/parcours"
        );

    const result =
        await response.json();

    const labels =

        result.data.map(

            p => p.parcours
        );

    const values =

        result.data.map(

            p => p.nombre
        );

    const ctx =

        document
        .getElementById(
            "parcoursChart"
        );

    new Chart(

        ctx,

        {

            type: "doughnut",

            data: {

                labels: labels,

                datasets: [

                    {

                        data: values
                    }
                ]
            }
        }
    );
}

loadStats();
loadParcoursChart();