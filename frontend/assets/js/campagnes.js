async function loadCampagnes() {

    const result =
        await apiGet(
            "/campagnes"
        );

    if (!result.success) {

        alert(
            "Erreur chargement campagnes"
        );

        return;
    }

    let html = "";

    result.data.forEach(c => {

        html += `

        <tr>

            <td>${c.id}</td>

            <td>${c.nom}</td>

            <td>${c.description ?? ""}</td>

            <td>${c.date_debut ?? ""}</td>

            <td>${c.date_fin ?? ""}</td>

            <td>${c.active}</td>

        </tr>

        `;
    });

    document
        .getElementById(
            "campagnesTable"
        )
        .innerHTML = html;
}

loadCampagnes();