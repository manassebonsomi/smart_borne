async function loadStats() {

    const stats = await apiGet("/dashboard/statistics");

    const data = stats.data;

    const container = document.getElementById("stats");

    container.innerHTML = "";

    const items = [
        { label: "Utilisateurs", value: data.utilisateurs },
        { label: "Sessions", value: data.sessions },
        { label: "Questions", value: data.questions },
        { label: "Recommandations", value: data.recommandations },
        { label: "Commandes", value: data.commandes },
        { label: "Campagnes", value: data.campagnes },
        { label: "Audits", value: data.audits }
    ];

    items.forEach(item => {

        const card = document.createElement("div");
        card.className = "stat-card";

        card.innerHTML = `
            <h2>${item.value}</h2>
            <p>${item.label}</p>
        `;

        container.appendChild(card);
    });
}


async function loadStatsChart() {

    const stats = await apiGet("/dashboard/statistics");
    const data = stats.data;

    const ctx1 = document.getElementById("statsChart");

    new Chart(ctx1, {

        type: "bar",

        data: {
            labels: [
                "Utilisateurs",
                "Sessions",
                "Questions",
                "Recommandations",
                "Commandes",
                "Campagnes",
                "Audits"
            ],

            datasets: [{
                label: "Statistiques CCC",
                data: [
                    data.utilisateurs,
                    data.sessions,
                    data.questions,
                    data.recommandations,
                    data.commandes,
                    data.campagnes,
                    data.audits
                ],
                backgroundColor: [
                    "#2563eb",
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444",
                    "#8b5cf6",
                    "#14b8a6",
                   "#f59e0b"
                ]
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    // =========================
    // DONUT CHART (vision globale)
    // =========================

    const ctx2 = document.getElementById("statsPieChart");

    new Chart(ctx2, {

        type: "doughnut",

        data: {
            labels: [
                "Utilisateurs",
                "Sessions",
                "Questions"
            ],

            datasets: [{
                data: [
                    data.utilisateurs,
                    data.sessions,
                    data.questions
                ],
                backgroundColor: [
                    "#2563eb",
                    "#22c55e",
                    "#f59e0b"
                ]
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}

async function loadParcoursChart() {

    const response = await fetch(API_URL + "/dashboard/parcours");
    const result = await response.json();

    const labels = result.data.map(p => p.parcours);
    const values = result.data.map(p => p.nombre);

    const ctx = document.getElementById("parcoursChart");

    new Chart(ctx, {

        type: "doughnut",

        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    "#2563eb",
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444",
                    "#8b5cf6"
                ],
                borderWidth: 1
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}

loadStats()
loadStatsChart()
loadParcoursChart()