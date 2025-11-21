document.addEventListener('DOMContentLoaded', () => {
    // 1. Déclarations initiales
    const token = localStorage.getItem("token");

    // 2. Gestion de l'affichage Login/Logout
    checkAuthentication(token);

    // 3. Récupération et affichage des détails du lieu
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }

    // 4. Gestion du Clic FORCÉ pour la navigation (écouteur général sur le corps)
    document.body.addEventListener('click', (e) => {
        // Cibler uniquement le lien dynamique que nous créons
        if (e.target && e.target.id === 'add-review-link') {
            e.preventDefault(); 
            const reviewLink = e.target;
            const placeIdToRedirect = reviewLink.getAttribute('data-place-id');
            const reviewPath = "/part4/hbnb/front/add_review.html"; // CHEMIN ABSOLU CORRIGÉ

            if (placeIdToRedirect) {
                 // Navigation forcée pour garantir que l'ID n'est pas perdu dans l'URL
                 window.location.href = `${reviewPath}?place_id=${encodeURIComponent(placeIdToRedirect)}`;
            } else {
                 alert("Erreur critique: Place ID n'a pas pu être lu par l'écouteur.");
            }
        }
    });

    // --- Logique du formulaire de soumission de review (si sur place.html) ---
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submissionPlaceId = getPlaceIdFromURL(); // Relire l'ID juste avant la soumission
            if (submissionPlaceId) {
                submitReview(submissionPlaceId, token); 
            }
        });
    }
});

// ----------------------------------------------------------------------
// Fonctions d'Utilité
// ----------------------------------------------------------------------

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

function checkAuthentication(token) {
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    // Le conteneur add-review est maintenant géré par le bouton généré dans displayPlaceDetails

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) {
            logoutButton.style.display = 'inline-block';

            if (!logoutButton.dataset.listenerAdded) {
                logoutButton.addEventListener('click', () => {
                    localStorage.removeItem('token');
                    window.location.reload();
                });
                logoutButton.dataset.listenerAdded = true;
            }
        }
    }
}

// ----------------------------------------------------------------------
// Fetching (Récupération des données)
// ----------------------------------------------------------------------

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });

        if (!response.ok) throw new Error('Impossible de récupérer la place');

        const place = await response.json();
        
        displayPlaceDetails(place);
        displayReviews(place.reviews || []);

    } catch (error) {
        console.error("Erreur fetchPlaceDetails :", error);
        const section = document.getElementById('place-details');
        if (section) section.innerHTML = `<p>Impossible de charger les détails de cette place. Vérifiez l'ID et l'API.</p>`;
    }
}

// ----------------------------------------------------------------------
// Affichage (GÉNÈRE LE BOUTON DYNAMIQUE)
// ----------------------------------------------------------------------

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    if (!section) return;

    const imageUrl = place.image_url || 'images/default_place.png'; 

    // Injection de l'ensemble de la structure HTML
    section.innerHTML = `
        <img src="${imageUrl}" alt="${place.title}" class="place-image">
        <div class="place-info">
            <h1>${place.title}</h1>
            <p><strong>Price:</strong> $${place.price} / night</p>
            <p><strong>Latitude:</strong> ${place.latitude}</p>
            <p><strong>Longitude:</strong> ${place.longitude}</p>
            <h3>Description:</h3>
            <p>${place.description}</p>

            <a id="add-review-link" data-place-id="${place.id}"
                class="btn-add-review">
                ➕ Add a Review
            </a>
        </div>
    `;
}

// ----------------------------------------------------------------------
// Affichage des Reviews (Utilisée par fetchPlaceDetails)
// ----------------------------------------------------------------------

function displayReviews(reviews) {
    const container = document.getElementById('reviews-container');
    if (!container) return;

    container.innerHTML = '';

    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(r => {
        const div = document.createElement('div');
        div.className = 'review-card';
        div.innerHTML = `
            <p><strong>User:</strong> ${r.user_id || 'Anonymous'}</p>
            <p>${r.text}</p>
            <p><strong>Rating:</strong> ${r.rating}/5</p>
        `;
        container.appendChild(div);
    });
}

// ----------------------------------------------------------------------
// Soumission de Review (Méthode utilisée par le formulaire)
// ----------------------------------------------------------------------

async function submitReview(placeId, token) {
    const text = document.getElementById("review-text").value;
    const rating = document.getElementById("review-rating").value;

    if (!text || !rating) {
        alert("Please fill out all fields.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                text: text,
                rating: parseInt(rating)
            })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(`Erreur lors de l'ajout de la review : ${err.error || response.status}`);
        }

        // Si le POST réussit, mettez à jour l'affichage
        const updated = await response.json();
        // Ici, vous devrez probablement re-fetch la liste complète des reviews si l'API ne renvoie pas la liste mise à jour.
        
        // Simplement vider les champs après succès
        document.getElementById("review-text").value = "";
        document.getElementById("review-rating").value = "";
        alert("Review ajoutée avec succès !");

    } catch (error) {
        console.error("Erreur submitReview :", error);
        alert(`Impossible d'ajouter une review. ${error.message}`);
    }
}