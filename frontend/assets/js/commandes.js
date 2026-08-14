// ENVOYER UNE COMMANDE
function sendCommand() {
    const input = document.getElementById("commandInput");
    const command = input.value.trim();

    if (!command) {
        showCommandMessage("Veuillez saisir une commande.", "warning");
        return;
    }

    // Nettoyer une éventuelle interaction précédente
    clearCommandInteraction();
    fetch("http://127.0.0.1:5000/api/commands/execute",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command: command })
        }
    ).then(res => res.json()).then(data => {

        // AFFICHAGE DE LA REPONSE JSON
        document.getElementById("commandResponse").innerText = JSON.stringify(data,null,2);

        // INTERACTION UTILISATEUR
        handleCommandInteraction(data);

        // FORMULAIRES DYNAMIQUES
        handleDynamicForm(data);

        // HISTORIQUE
        loadCommandes();
    })
    .catch(error => {
        console.error("Erreur lors de l'exécution de la commande :", error);
        showCommandMessage("Une erreur est survenue lors de l'exécution de la commande.", "error");
    });
}


// GESTION DES INTERACTIONS
function handleCommandInteraction(data) {

    if (!data || !data.interaction) {
        return;
    }
    const interaction = data.interaction;

    // CONFIRMATION
    if (interaction.type === "CONFIRMATION") {
        showConfirmationInteraction(interaction);
        return;
    }

    // MESSAGE
    if (interaction.type === "MESSAGE") {
        showCommandMessage(interaction.message || "", "info");
        return;
    }

    // FORMULAIRE
    if (interaction.type === "FORM") {
        handleInteractionForm(interaction);
        return;
    }

    // DOWNLOAD
    if (interaction.type === "DOWNLOAD") {
        showCommandMessage(interaction.message ||"Le fichier est prêt.", "success");
        return;
    }
}


// CONFIRMATION OUI / NON
function showConfirmationInteraction(interaction) {
    const container = document.getElementById("commandInteraction");
    if (!container) {
        console.warn("Element #commandInteraction introuvable.");
        return;
    }

    const message = interaction.message ||  "Voulez-vous confirmer ?";
    const value = interaction.value || "";
    container.innerHTML = `
        <div class="command-confirmation">
            <div class="confirmation-message">
                ${escapeHtml(message)}
            </div>
            <div class="confirmation-command">
                ${escapeHtml(value)}
            </div>
            <div class="confirmation-actions">
                <button type="button" class="btn-confirm" onclick="confirmCommand(true)">
                    OUI
                </button>
                <button type="button" class="btn-cancel" onclick="confirmCommand(false)">
                    NON
                </button>
            </div>
        </div>
    `;
    container.style.display = "block";
}

// REPONSE A LA CONFIRMATION
function confirmCommand(confirmed) {
    const container = document.getElementById("commandInteraction");
    if (!confirmed) {
        if (container) {
            container.innerHTML = `
                <div class="command-interaction-message">
                    Commande annulée. Veuillez reformuler votre commande.
                </div>
            `;
        }
        return;
    }

    // Récupérer la commande proposée
    const commandElement = document.querySelector(".confirmation-command");
    if (!commandElement) {
        showCommandMessage("Impossible de récupérer la commande proposée.", "error");
        return;
    }

    const command = commandElement.textContent.trim();
    if (!command) {
        showCommandMessage("La commande proposée est vide.", "error");
        return;
    }

    // Nettoyer l'interaction
    clearCommandInteraction();

    // Mettre la commande corrigée dans le champ
    const input = document.getElementById("commandInput");

    if (input) {
        input.value = command;
    }
    sendCommand();
}


// FORMULAIRES DYNAMIQUES
function handleDynamicForm(data) {
    if (!data || !data.execution) {
        return;
    }

    const execution = data.execution;
    if (execution.show_form) {
        if (execution.form_type === "add_question") {
            showAddQuestionForm();
        }

        else if (execution.form_type === "edit_question") {
            showEditQuestionForm(execution.question_id);
        }
    }
}

// FORMULAIRE VIA INTERACTION
function handleInteractionForm(interaction) {
    if (interaction.form_type === "add_question") {
        showAddQuestionForm();
        return;
    }

    if (interaction.form_type === "edit_question") {
        showEditQuestionForm(interaction.question_id);
        return;
    }
}

// MESSAGE UTILISATEUR
function showCommandMessage(message, type = "info") {
    const container = document.getElementById("commandInteraction");

    if (!container) {
        return;
    }

    container.innerHTML = `
        <div class="command-interaction-message ${type}">
            ${escapeHtml(message)}
        </div>
    `;
    container.style.display = "block";
}


// NETTOYER INTERACTION
function clearCommandInteraction() {

    const container = document.getElementById("commandInteraction");
    if (!container) {
        return;
    }
    container.innerHTML = "";
    container.style.display = "none";
}

// PROTECTION HTML
function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// CHARGEMENT HISTORIQUE
async function loadCommandes() {
    const result = await apiGet("/commands");
    if (!result.success) {
        alert("Erreur chargement commandes");
        return;
    }

    let html = "";
    result.data.forEach(
        c => {
            html += `
                <tr>
                    <td>
                        ${c.id_commande}
                    </td>
                    <td>
                        ${escapeHtml(c.texte_commande)}
                    </td>
                    <td>
                        ${escapeHtml(c.tokens)}
                    </td>
                    <td>
                        ${escapeHtml(c.resultat)}
                    </td>
                    <td>
                        ${c.valide}
                    </td>
                    <td>
                        ${c.date_execution}
                    </td>
                </tr>
            `;
        }
    );

    document.getElementById("commandesTable").innerHTML = html;
}

// AJOUTER QUESTION
function showAddQuestionForm() {
    const container = document.getElementById("dynamicForm");
    container.innerHTML = `
        <div class="dynamic-form">
            <h3>
                Ajouter une question
            </h3>
            <input type="text" id="texte_question" placeholder="Texte question">
            <input type="number" id="ordre_question" placeholder="Ordre">
            <input type="number" id="id_categorie" placeholder="Catégorie">
            <button type="button" onclick="submitAddQuestion()">
                Enregistrer
            </button>
        </div>
    `;
}


// ENREGISTRER QUESTION
async function submitAddQuestion() {
    const payload = {
        texte_question: document.getElementById("texte_question").value,
        ordre_question: parseInt(document.getElementById("ordre_question").value),
        id_categorie: parseInt(document.getElementById("id_categorie").value)
    };

    const result = await apiPost("/questions", payload);
    if (result.id_question) {
        alert("Question ajoutée avec succès");
        document.getElementById("dynamicForm").innerHTML = "";
        loadCommandes();
    }

    else {
        alert(result.message || "Erreur lors de l'ajout");
    }
}

// MODIFIER QUESTION
function showEditQuestionForm(questionId) {
    document.getElementById("dynamicForm").innerHTML = `
        <div class="dynamic-form">
            <h3>
                Modification de la Question ${questionId}
            </h3>
            <input type="text" id="texte_question" placeholder="Veuillez saisir la nouvelle question">
            <input type="number" id="ordre_question" placeholder="Entrer le numéro d'ordre">
            <button type="button" onclick="submitEditQuestion(${questionId})">
                Modifier
            </button>
        </div>
    `;
}

// ENREGISTRER MODIFICATION
async function submitEditQuestion(questionId) {
    const payload = {
        texte_question: document.getElementById("texte_question").value,
        ordre_question: parseInt(document.getElementById("ordre_question").value)
    };

    const result = await apiPut("/questions/" + questionId, payload);

    if (result.success) {
        alert("Question modifiée avec succès");
        document.getElementById("dynamicForm").innerHTML = "";
        loadCommandes();

    }

    else {
        alert(result.message || "Erreur lors de la modification");
    }
}

// INITIALISATION
loadCommandes();