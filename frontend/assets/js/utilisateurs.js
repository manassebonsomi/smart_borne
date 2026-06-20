async function loadUsers() {

    const users =
        await apiGet(
            "/utilisateurs"
        );

    // const users = result.data;

    let html = "";

    users.forEach(u => {

        html += `
        <tr>

            <td>${u.id}</td>

            <td>${u.nom}</td>

            <td>${u.prenom}</td>

            <td>${u.age}</td>

            <td>${u.profil}</td>

        </tr>
        `;
    });

    document
        .getElementById(
            "usersTable"
        )
        .innerHTML = html;
}

loadUsers();