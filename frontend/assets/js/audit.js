async function loadAudit() {
    const result = await apiGet("/dashboard/audit");

    if (!result.success) {
        alert("Erreur chargement audit" );
        return;
    }

    let html = "";
    result.data.forEach(a => {
        html += `
        <tr>
            <td>${a.id}</td>
            <td>${a.date}</td>
            <td>${a.action}</td>
            <td>${a.objet}</td>
            <td>${a.resultat}</td>
            <td>${a.details}</td>
        </tr>
        `;
    });

    document.getElementById("auditTable").innerHTML = html;
}

loadAudit();