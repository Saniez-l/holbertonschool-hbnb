document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // Filtre prix
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlaces);
    }

    // Gestion du bouton logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('token'); // supprime le token
            window.location.reload(); // recharge la page pour réafficher Login
        });
    }
});

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    const token = localStorage.getItem('token');

    console.log("Token trouvé :", token);

    if (token && token !== "undefined" && token !== "null") {
        loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        fetchPlaces(token);
    } else {
        loginLink.style.display = 'block';
        if (logoutButton) logoutButton.style.display = 'none';
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error('Impossible de récupérer les places');

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error("Erreur fetchPlaces :", error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    const existingCard = placesList.querySelector('.place-card'); // Winchester House

    placesList.innerHTML = '';
    if (existingCard) placesList.appendChild(existingCard);

    places.forEach(place => {
        const div = document.createElement('article');
        div.classList.add('place-card');
        div.innerHTML = `
            <h2>${place.title}</h2>
            <p>Description: ${place.description}</p>
            <p class="price">Price: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(div);
    });
}

function filterPlaces() {
    const maxPrice = document.getElementById('price-filter').value;
    const places = document.querySelectorAll('#places-list > .place-card');

    places.forEach(place => {
        const priceElement = place.querySelector('.price');
        if (!priceElement) return;

        const price = parseFloat(priceElement.textContent.replace(/\D/g, ''));
        if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}
