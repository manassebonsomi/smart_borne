const axios = require("axios");

axios.post("http://localhost:5000/api/auth/login", {
    email: "admin@ccc.cd",
    mot_de_passe: "123456"
})
.then(response => {
    console.log(response.data);
})
.catch(error => {
    console.log(error.response.data);
});