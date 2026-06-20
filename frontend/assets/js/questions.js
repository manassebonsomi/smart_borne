async function loadQuestions() {

    const questions =
        await apiGet(
            "/questions"
        );

    // const questions = result.data;

    let html = "";

    questions.forEach(q => {

        html += `
        <tr>

            <td>
                ${q.id_question}
            </td>

            <td>
                ${q.texte_question}
            </td>

            <td>
                ${q.ordre_question}
            </td>

            <td>
                ${q.active}
            </td>

        </tr>
        `;
    });

    document
        .getElementById(
            "questionsTable"
        )
        .innerHTML = html;
}

loadQuestions();