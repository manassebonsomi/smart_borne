async function loadAudit() {

    const result =
        await apiGet(
            "/audit"
        );

    if (!result.success) {

        alert(
            "Erreur chargement audit"
        );

        return;
    }

    let html = "";

    result.data.forEach(a => {

        html += `

        <tr>

            <td>${a.id_audit}</td>

            <td>${a.date_action}</td>

            <td>${a.action}</td>

            <td>${a.objet}</td>

            <td>${a.resultat}</td>

            <td>${a.details}</td>

        </tr>

        `;
    });

    document
        .getElementById(
            "auditTable"
        )
        .innerHTML = html;
}

loadAudit();