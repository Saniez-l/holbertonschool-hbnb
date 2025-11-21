document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errData = await response.json();
                alert('Login failed: ' + (errData.error || 'Identifiants incorrects'));
                return;
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';

        } catch (error) {
            alert('Erreur réseau : ' + error.message);
        }
    });
});
