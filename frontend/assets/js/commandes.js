function sendCommand() {

    let command =
        document.getElementById("commandInput").value;

    fetch("http://127.0.0.1:5000/api/commands/execute", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ command })
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("commandResponse").innerText =
            JSON.stringify(data, null, 2);

        loadCommandes();
    });
}

async function loadCommandes() {

    const result =
        await apiGet("/commands");

    if (!result.success) {
        alert("Erreur chargement commandes");
        return;
    }

    let html = "";

    result.data.forEach(c => {

        html += `
        <tr>
            <td>${c.id_commande}</td>
            <td>${c.texte_commande}</td>
            <td>${c.tokens}</td>
            <td>${c.resultat}</td>
            <td>${c.valide}</td>
            <td>${c.date_execution}</td>
        </tr>`;
    });

    document.getElementById("commandesTable").innerHTML = html;
}

loadCommandes();