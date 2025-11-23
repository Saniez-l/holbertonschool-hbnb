function handleLogout(event) {
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
}

function updateAuthUI() {
    const loginLink = document.getElementById('login-link');
    const token = localStorage.getItem('token');
    const logoutButton = document.getElementById('logout-button');
    
    const isAuthenticated = !!token && token !== "undefined" && token !== "null";

    if (loginLink) loginLink.style.display = isAuthenticated ? 'none' : 'block';
    if (logoutButton) {
        logoutButton.style.display = isAuthenticated ? 'block' : 'none';

        if (isAuthenticated && !logoutButton.hasAttribute('data-listener-added')) {
             logoutButton.addEventListener('click', handleLogout);
             logoutButton.setAttribute('data-listener-added', 'true');
        }
    }
}


async function fetchPlacePreview(placeId, token) {
    const placeTitleEl = document.getElementById('place-title');
    const placeNameSpan = document.getElementById('place-name');

    if (!placeId) return;

    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
        if (!response.ok) throw new Error('Impossible de récupérer la place');

        const place = await response.json();
        placeTitleEl.textContent = place.title;
        placeNameSpan.textContent = place.title;

    } catch (err) {
        console.error('Erreur fetch place:', err);
    }
}


document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();

    const reviewForm = document.getElementById('add-review-form');
    const backLink = document.getElementById('back-to-place');
    const placeId = getPlaceIdFromURL();
    const token = localStorage.getItem('token');

    
    if (!token) {
        alert("Vous devez être connecté pour ajouter une review.");
        window.location.href = "index.html";
        return;
    }

    if (!placeId) {
        alert("Place ID manquant !");
        return;
    }

    fetchPlacePreview(placeId, token);

    // Mettre le lien "Back to Place" avec le bon place_id
    backLink.href = `place.html?place_id=${encodeURIComponent(placeId)}`;

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const text = document.getElementById('review-text').value.trim();
            const rating = parseInt(document.getElementById('review-rating').value, 10);

            if (!text || !rating) {
                alert("Veuillez remplir tous les champs !");
                return;
            }

            try {
                const response = await fetch(
                    `http://127.0.0.1:5000/api/v1/reviews/${placeId}/reviews`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({ text, rating})
                    }
                );

                if (!response.ok) {
                    const err = await response.json().catch(() => ({}));
                    alert("Erreur lors de l'ajout de la review : " + (err.error || response.status));
                    return;
                }

                alert("Review ajoutée avec succès !");
                // Redirection vers la page place avec le place_id intact
                window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;

            } catch (error) {
                console.error("Erreur réseau add review:", error);
                alert("Erreur réseau : impossible d'ajouter la review.");
            }
        });
    }
});

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}
