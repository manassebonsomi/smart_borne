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
        // AFFICHAGE REPONSE

        document.getElementById(
            "commandResponse"
        ).innerText =
            JSON.stringify(
                data,
                null,
                2
            );

        // FORMULAIRES DYNAMIQUES

        if (
            data.execution &&
            data.execution.show_form
        ) {

            if (
                data.execution.form_type ===
                "add_question"
            ) {

                showAddQuestionForm();
            }

            else if (
                data.execution.form_type ===
                "edit_question"
            ) {

                showEditQuestionForm(

                    data.execution.question_id
                );
            }
        }

        // RECHARGER HISTORIQUE
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

function showAddQuestionForm() {

    document.getElementById(
        "dynamicForm"
    ).innerHTML = `

        <h3>Ajouter une question</h3>

        <input
            type="text"
            id="texte_question"
            placeholder="Texte question">

        <input
            type="number"
            id="ordre_question"
            placeholder="Ordre">

        <input
            type="number"
            id="id_categorie"
            placeholder="Catégorie">



        <button
            onclick="submitAddQuestion()">

            Enregistrer
        </button>
    `;
}

async function submitAddQuestion() {

    const payload = {

        texte_question:
            document.getElementById(
                "texte_question"
            ).value,

        ordre_question:
            parseInt(
                document.getElementById(
                    "ordre_question"
                ).value
            ),

        id_categorie:
            parseInt(
                document.getElementById(
                    "id_categorie"
                ).value
            )
    };

    const result =
        await apiPost(
            "/questions",
            payload
        );

    if(result.id_question){

        alert(
            "Question ajoutée avec succès"
        );

        document.getElementById(
            "dynamicForm"
        ).innerHTML = "";

        loadCommandes();

    } else {

        alert(
            "Erreur lors de l'ajout"
        );
    }
}

function showEditQuestionForm(
    questionId
){

    document.getElementById(
        "dynamicForm"
    ).innerHTML = `

        <h3>
            Modifier Question
            ${questionId}
        </h3>

        <input
            type="text"
            id="texte_question" placeholder="Veuiller saisir la nouvelle question">

        <input
            type="number"
            id="ordre_question" placeholder="Entrer le numero d'ordre">

        <button
            onclick="submitEditQuestion(${questionId})">

            Modifier
        </button>
    `;
}

async function submitEditQuestion(questionId) {

    const payload = {

        texte_question:
            document.getElementById(
                "texte_question"
            ).value,

        ordre_question:
            parseInt(
                document.getElementById(
                    "ordre_question"
                ).value
            ),

    };

    const result = await apiPut(
        "/questions/" + questionId,
        payload
    );

    if(result.success){

        alert(
            "Question modifiée avec succès"
        );

        document.getElementById(
            "dynamicForm"
        ).innerHTML = "";

        loadCommandes();

    } else {

        alert(
            result.message ||
            "Erreur lors de la modification"
        );
    }
}

loadCommandes();