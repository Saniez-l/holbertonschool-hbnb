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
            const reviewPath = "/part4/hbnb/front/add_review.html";

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

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) {
            logoutButton.style.display = 'inline-block';

            if (!logoutButton.dataset.listenerAdded) {
                logoutButton.addEventListener('click', (event) => {
                    event.preventDefault();
                    const confirmed = confirm("Do you dare log out? Afraid of the adventure?");
                    if (!confirmed) return;

                    localStorage.removeItem('token');

                    const video = document.createElement('video');
                    video.src = 'images/logout.mp4';
                    video.style.position = 'fixed';
                    video.style.top = 0;
                    video.style.left = 0;
                    video.style.width = '100%';
                    video.style.height = '100%';
                    video.style.zIndex = 9999;
                    video.autoplay = true;
                    video.onended = () => {
                        window.location.href = 'index.html';
                    };

                    document.body.appendChild(video);
                    video.play();
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

    const amenitiesList = (place.amenities && place.amenities.length > 0)
        ? place.amenities.map(a => a.name).join(', ')
        : 'None';

    // Injection de l'ensemble de la structure HTML
    section.innerHTML = `
        <img src="${imageUrl}" alt="${place.title}" class="place-image">
                <div class="place-info">
            <h1 class="place-title">${place.title}</h1>

            <div class="place-detail-item">
                <span class="label">Price:</span> $${place.price} / night
            </div>

            <div class="place-detail-item">
                <span class="label">Latitude:</span> ${place.latitude}
            </div>

            <div class="place-detail-item">
                <span class="label">Longitude:</span> ${place.longitude}
            </div>

            <div class="place-detail-item">
                <span class="label">Description:</span> ${place.description}
            </div>

            <div class="place-detail-item">
                <span class="label">Amenities:</span> ${amenitiesList}
            </div>

            <a id="add-review-link" data-place-id="${place.id}"
                class="details-button add-review-btn-pos">
                Add a Review
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
        const reviewerName = r.user_full_name || 'Anonymous';
        div.innerHTML = `
            <p><strong>User:</strong> ${reviewerName}</p>
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