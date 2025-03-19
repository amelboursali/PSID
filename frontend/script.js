// Définition de l'URL de base de l'API Django
const baseURL = "http://127.0.0.1:8000/api";

// Récupérer un message spécifique depuis l'API Django
async function fetchMessage(section) {
    const contentElement = document.getElementById("content");
    contentElement.innerHTML = `<p class="loading">Chargement...</p>`; // Affichage d'un message de chargement

    try {
        const response = await fetch(`${baseURL}/message/${section}/`);
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        const data = await response.json();
        console.log("Message reçu du back:", data.message);
        contentElement.innerHTML = `<h1>${data.message}</h1>`;
    } catch (error) {
        console.error("Erreur lors de la récupération du message :", error);
        contentElement.innerHTML = `<p class="error">Erreur : impossible de charger cette section.</p>`;
    }
}

// Fonction pour afficher une section via un appel à l'API
function showSection(section) {
    fetchMessage(section);
}
