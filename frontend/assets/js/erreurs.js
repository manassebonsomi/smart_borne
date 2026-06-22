async function loadErreurs() {

    const result =
        await apiGet(
            "/dashboard/errors"
        );

    if (!result.success) {

        alert(
            "Erreur chargement erreurs"
        );

        return;
    }

    let html = "";

    result.data.forEach(e => {

        html += `

        <tr>

            <td>${e.id_erreur}</td>

            <td>${e.type_erreur}</td>

            <td>${e.message}</td>

            <td>${e.corrigee}</td>

            <td>${e.date_erreur ?? ""}</td>

        </tr>

        `;
    });

    document
        .getElementById(
            "erreursTable"
        )
        .innerHTML = html;
}

loadErreurs();