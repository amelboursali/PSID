fetch("http://127.0.0.1:8000/api/tasks/") // L'URL de ton API Django
    .then(response => response.json()) // Convertir la réponse en JSON
    .then(data => {
        console.log("Bien connecté au backend :", data); // Vérifier dans la console
        document.getElementById("content").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => console.error("Erreur lors de la récupération des données :", error));

// Fonction pour récupérer un message depuis l'API Django
function fetchMessage(section) {
    fetch(`http://127.0.0.1:8000/api/message/${section}/`)
        .then(response => response.json())
        .then(data => {
            console.log("Message reçu du back:", data.message); // Vérifier dans la console
            document.getElementById("content").innerHTML = `<h1>${data.message}</h1>`;
        })
        .catch(error => console.error("Erreur lors de la récupération du message :", error));
}

// Fonction appelée lorsqu'on clique sur un menu
function showSection(section) {
    fetchMessage(section);
}
