document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // Filtre prix
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlaces);
    }

    // Logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.reload();
        });
    }
});

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    const token = localStorage.getItem('token');

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
        console.log(places);
    } catch (error) {
        console.error("Erreur fetchPlaces :", error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const div = document.createElement('article');
        div.classList.add('place-card');

        // Définir l'image correctement
        const imageSrc = place.image_url || 'images/default_place.png';

        div.innerHTML = `
            <img src="${imageSrc}" alt="${place.title}" class="place-image">
            <h2>${place.title}</h2>
            <p class="price">Price: $${place.price}</p>
            <button class="details-button" data-id="${place.id}">View Details</button>
        `;
        placesList.appendChild(div);
    });

    // Ajouter événement pour tous les boutons "View Details"
    const detailButtons = document.querySelectorAll('.details-button');
    detailButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const placeId = e.target.getAttribute('data-id');
            if (!placeId) return;
            window.location.href = `place.html?place_id=${placeId}`;
        });
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
