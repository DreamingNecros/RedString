(function() {
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      sessionStorage.setItem('accessToken', token);  // clé unifiée ici
      // Nettoyer l'URL pour ne plus afficher le token
      const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    } else {
    }
  } catch (e) {
    console.error("Erreur lors du stockage du token :", e);
  }
})();
