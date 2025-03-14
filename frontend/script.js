fetch("http://127.0.0.1:8000/api/tasks/") // L'URL de ton API Django
    .then(response => response.json()) // Convertir la réponse en JSON
    .then(data => {
        console.log("Données reçues :", data); // Vérifier dans la console
        document.getElementById("content").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => console.error("Erreur lors de la récupération des données :", error));

// Fonction pour afficher le contenu dynamique
function showSection(section) {
    const content = document.getElementById("content");

    let message = "";
    if (section === "accueil") {
        message = "<h1>🏠 Bienvenue !</h1><p>Ceci est la page d'accueil.</p>";
    } else if (section === "machinelearning") {
        message = "<h1>🤖 Machine Learning</h1><p>Découvrez les modèles d'IA.</p>";
    } else if (section === "graphe") {
        message = "<h1>📊 Graphes et Analyses</h1><p>Visualisation des données.</p>";
    }

    // Mettre à jour le contenu
    content.innerHTML = message;
}
