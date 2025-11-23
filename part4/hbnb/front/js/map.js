document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. INITIALISATION DU GLOBE ---
    const globeContainer = document.getElementById('globeViz');
    
    const world = Globe()
        (globeContainer)
        .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
        .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
        .pointOfView({ lat: 30, lng: 0, altitude: 2.0 }); // Vue de départ

    // --- 2. RÉCUPÉRATION DU TOKEN ---
    const token = localStorage.getItem('token');

    // --- 3. APPEL API HBNB ---
    const API_URL = 'http://127.0.0.1:5000/api/v1/places/';

    fetch(API_URL, {
        method: 'GET',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        return response.json();
    })
    .then(places => {
        console.log(`Carte chargée : ${places.length} places trouvées.`);
        
        // --- 4. AFFICHAGE DES POINTS ---
        world
            .htmlElementsData(places)
            // Conversion sécurisée des coordonnées en nombres
            .htmlLat(d => parseFloat(d.latitude))
            .htmlLng(d => parseFloat(d.longitude))
            
            // IMPORTANT : Colle les points à la surface (Altitude 0)
            .htmlAltitude(0)
            
            .htmlElement(place => {
                // A. LE CONTENEUR (Invisible, sert au positionnement)
                const container = document.createElement('div');
                container.style.width = '0';
                container.style.height = '0';
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.style.justifyContent = 'center';
                
                // MAGIE 1 : Le conteneur laisse passer les clics (pour pouvoir tourner la terre)
                container.style.pointerEvents = 'none';

                // B. LE POINT ROUGE (Visible)
                const dot = document.createElement('div');
                dot.style.width = '14px';
                dot.style.height = '14px';
                dot.style.background = 'rgba(255, 0, 0, 0.9)';
                dot.style.borderRadius = '50%';
                dot.style.border = '2px solid white';
                dot.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.8)';
                
                // Animation
                dot.style.animation = 'blink 1.5s infinite ease-in-out';
                
                // MAGIE 2 : Le point rouge capture le clic
                dot.style.pointerEvents = 'auto';
                dot.style.cursor = 'pointer';

                // Info-bulle
                dot.title = `${place.title || place.name} - $${place.price}`;

                // C. L'ACTION AU CLIC
                dot.onclick = (event) => {
                    // MAGIE 3 : Empêche le clic de traverser vers la carte
                    event.stopPropagation();
                    
                    console.log("Redirection vers :", place.id);
                    window.location.href = `place.html?place_id=${place.id}`;
                };

                // On met le point dans le conteneur
                container.appendChild(dot);
                return container;
            });
    })
    .catch(error => {
        console.error("Erreur lors du chargement des places :", error);
        if (!token) {
            alert("Veuillez vous connecter pour voir les places.");
        }
    });

    // --- 5. CONTRÔLES ET ROTATION ---
    const controls = world.controls();
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.6;
    
    // Arrêter la rotation si on manipule le globe
    globeContainer.addEventListener('mousedown', () => {
        controls.autoRotate = false;
    });

    // --- 6. GESTION DU REDIMENSIONNEMENT ---
    window.addEventListener('resize', () => {
        world.width(window.innerWidth);
        world.height(window.innerHeight);
    });

    // --- 7. BOUTON RETOUR ---
    const backBtn = document.getElementById('back-button');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            window.location.href = "index.html";
        });
    }
});