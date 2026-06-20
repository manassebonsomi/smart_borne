const API_URL =
    "http://127.0.0.1:5000/api";

let questions = [];

let current = 0;

let inactivity = 0;

let surveyFinished = false;

let sessionId =
    localStorage.getItem(
        "session_id"
    );

if (!sessionId) {

    alert(
        "Aucune session active"
    );

    window.location =
        "profil.html";
}

let userId =
    localStorage.getItem(
        "user_id"
    );

let currentQuestion =
    null;

let selectedValue = "";


/*
=====================================
CHARGEMENT QUESTIONS
=====================================
*/

async function loadQuestions() {

    try {

        const response =
            await fetch(
                API_URL +
                "/questions"
            );

        questions =
            await response.json();

        if (
            !questions ||
            questions.length === 0
        ) {

            alert(
                "Aucune question disponible"
            );

            return;
        }

        await restoreProgress();

    }

    catch(error) {

        console.error(error);

        alert(
            "Erreur chargement questions"
        );
    }
}


/*
=====================================
REPRISE SESSION
=====================================
*/

async function restoreProgress() {

    try {

        const response =
            await fetch(

                API_URL +
                "/session/" +
                sessionId
            );

        if(response.ok) {

            const result =
                await response.json();

            if (
                result.success
            ) {

                current =
                    result.data
                    .question_actuelle || 0;
            }
        }

        showQuestion();

    }

    catch(error) {

        console.error(error);

        showQuestion();
    }
}


/*
=====================================
AFFICHAGE QUESTION
=====================================
*/

function showQuestion() {

    if (
        current >=
        questions.length
    ) {

        finishSurvey();

        return;
    }

    currentQuestion =
        questions[current];

    const savedAnswer =

        localStorage.getItem(

            "answer_" +
            currentQuestion.id_question

        ) || "";

    document
        .getElementById(
            "questionNumber"
        )
        .innerHTML =

        `Question ${
            current + 1
        } / ${
            questions.length
        }`;

    document
        .getElementById(
            "questionContainer"
        )
        .innerHTML =

        `
        <h2>
            ${
                currentQuestion
                .texte_question
            }
        </h2>

        <textarea
            id="answer"
            class="answer-box"
            placeholder="Votre réponse..."
        >${savedAnswer}</textarea>
        `;

    updateProgressBar();
}


/*
=====================================
BARRE PROGRESSION
=====================================
*/

function updateProgressBar() {

    const percent =

        (
            (current + 1)
            /
            questions.length
        ) * 100;

    document
        .getElementById(
            "progressBar"
        )
        .style.width =

        percent + "%";
}


/*
=====================================
SAUVEGARDE REPONSE
=====================================
*/

async function saveAnswer() {

    selectedValue =

        document
        .getElementById(
            "answer"
        )
        .value
        .trim();

    if (
        selectedValue === ""
    ) {

        alert(
            "Veuillez répondre"
        );

        return false;
    }

    localStorage.setItem(

        "answer_" +
        currentQuestion.id_question,

        selectedValue
    );

    try {

        const response =
            await fetch(

                API_URL +
                "/survey/save-answer",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            id_session:
                                sessionId,

                            id_question:
                                currentQuestion
                                .id_question,

                            valeur_reponse:
                                selectedValue
                        })
                }
            );

        if(!response.ok) {

            throw new Error(
                "Erreur sauvegarde réponse"
            );
        }

        await saveSessionProgress();

        return true;
    }

    catch(error) {

        console.error(error);

        return false;
    }
}


/*
=====================================
SAUVEGARDE SESSION
=====================================
*/

async function saveSessionProgress() {

    try {

        await fetch(

            API_URL +
            "/session/save",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify({

                        id_session:
                            sessionId,

                        question:
                            current,

                        etat:
                            "QUESTIONNAIRE"
                    })
            }
        );

    }

    catch(error) {

        console.error(error);
    }
}


/*
=====================================
QUESTION SUIVANTE
=====================================
*/

async function nextQuestion() {

    const success =
        await saveAnswer();

    if (!success)
        return;

    current++;

    showQuestion();
}


/*
=====================================
QUESTION PRECEDENTE
=====================================
*/

function previousQuestion() {

    if (
        current > 0
    ) {

        current--;

        showQuestion();
    }
}


/*
=====================================
FIN QUESTIONNAIRE
=====================================
*/

async function finishSurvey() {

    if (surveyFinished)
        return;

    surveyFinished = true;

    try {

        /*
        QUESTIONNAIRE -> ANALYSE
        */

        await fetch(

            API_URL +
            "/survey/complete/" +
            sessionId,

            {
                method: "POST"
            }
        );

        /*
        GENERATION RECOMMANDATION
        */

        const recommandationResponse =

            await fetch(

                API_URL +
                "/recommandation/generate/" +
                sessionId,

                {
                    method: "POST"
                }
            );

        const recommandationResult =

            await recommandationResponse.json();

        if (
            !recommandationResult.success
        ) {

            throw new Error(

                recommandationResult.message
            );
        }

        /*
        ANALYSE -> RESULTAT
        */

        await fetch(

            API_URL +
            "/survey/result/" +
            sessionId,

            {
                method: "POST"
            }
        );

        /*
        STOCKAGE LOCAL
        */

        localStorage.setItem(

            "recommandation",

            JSON.stringify(

                recommandationResult.data
            )
        );

        /*
        RESULTAT -> FIN_SESSION
        */

        await fetch(

            API_URL +
            "/survey/finish/" +
            sessionId,

            {
                method: "POST"
            }
        );

        /*
        REDIRECTION
        */

        window.location =
            "resultat.html";

    }

    catch(error) {

        console.error(error);

        alert(

            "Erreur : " +
            error.message
        );

        surveyFinished = false;
    }
}


/*
=====================================
INACTIVITE
=====================================
*/

setInterval(() => {

    inactivity++;

}, 1000);

document.onclick = () => {

    inactivity = 0;
};

document.onmousemove = () => {

    inactivity = 0;
};

document.onkeypress = () => {

    inactivity = 0;
};

setInterval(

    async () => {

        try {

            await fetch(

                API_URL +
                "/session/inactivity",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            id_session:
                                sessionId,

                            secondes:
                                inactivity
                        })
                }
            );

            if (
                inactivity >= 300
            ) {

                alert(
                    "Session interrompue pour inactivité"
                );

                window.location =
                    "index.html";
            }

        }

        catch(error) {

            console.error(error);
        }

    },

    30000
);


/*
=====================================
BOUTONS
=====================================
*/

document
    .getElementById(
        "nextBtn"
    )
    .addEventListener(

        "click",

        nextQuestion
    );

document
    .getElementById(
        "prevBtn"
    )
    .addEventListener(

        "click",

        previousQuestion
    );


/*
=====================================
INITIALISATION
=====================================
*/

loadQuestions();

