async function loadErreurs() {

    const result =
        await apiGet(
            "/erreurs"
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

            <td>${e.id}</td>

            <td>${e.type}</td>

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