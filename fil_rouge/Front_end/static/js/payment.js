console.log("payment.js chargé");

async function refreshAccessToken() {
    const refreshToken = sessionStorage.getItem("refreshToken");
    if (!refreshToken) throw new Error("Pas de refresh token, veuillez vous reconnecter.");

    const response = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken })
    });

    if (!response.ok) throw new Error("Impossible de rafraîchir le token.");

    const data = await response.json();
    sessionStorage.setItem("accessToken", data.access);
    return data.access;
}

async function fetchWithRefresh(url, options) {
    let accessToken = sessionStorage.getItem("accessToken");
    if (!accessToken) throw new Error("Pas de token d'accès, veuillez vous connecter.");

    options.headers = options.headers || {};
    options.headers["Authorization"] = `Bearer ${accessToken}`;

    let response = await fetch(url, options);

    if (response.status === 401) {
        const text = await response.text();
        if (text.includes("token_not_valid")) {
            try {
                accessToken = await refreshAccessToken();
                options.headers["Authorization"] = `Bearer ${accessToken}`;
                response = await fetch(url, options);
            } catch {
                throw new Error("Session expirée, veuillez vous reconnecter.");
            }
        }
    }

    return response;
}

document.addEventListener("DOMContentLoaded", () => {
    const cartSummary = document.getElementById("cart-summary");
    const payButton = document.getElementById("pay-button");

    const jwtToken = sessionStorage.getItem("accessToken");
    if (!jwtToken) {
        alert("Vous devez être connecté pour payer.");
        window.location.href = "/login";
        return;
    }

    const panier = JSON.parse(localStorage.getItem("panier")) || {};
    const items = Object.entries(panier).map(([id, item]) => ({
        id,
        name: item.name,
        quantity: item.quantity,
        price: item.price
    }));

    if (items.length === 0) {
        cartSummary.innerHTML = "<p>Votre panier est vide.</p>";
        payButton.disabled = true;
        return;
    }

    let ul = document.createElement("ul");
    items.forEach(item => {
        const price = typeof item.price === 'number' ? item.price : 0;
        let li = document.createElement("li");
        li.textContent = `${item.name} - ${item.quantity} x ${price.toFixed(2)}€`;
        ul.appendChild(li);
    });
    cartSummary.appendChild(ul);

    let total = items.reduce((acc, item) => acc + item.quantity * (item.price || 0), 0);
    const totalP = document.createElement("p");
    totalP.id = "total-price";
    totalP.innerHTML = `<strong>Total : ${total.toFixed(2)}€</strong>`;
    cartSummary.appendChild(totalP);

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const cardElement = elements.create("card");

    const cardDiv = document.createElement("div");
    cardDiv.id = "card-element";
    cardDiv.style = "margin: 1em 0;";
    cartSummary.appendChild(cardDiv);

    cardElement.mount("#card-element");

    const cardErrors = document.createElement("div");
    cardErrors.id = "card-errors";
    cardErrors.style.color = "red";
    cartSummary.appendChild(cardErrors);

    payButton.addEventListener("click", async () => {
        payButton.disabled = true;
        payButton.textContent = "Paiement en cours...";

        const cartForBackend = items.map(item => ({
            id: item.id,
            quantity: item.quantity,
        }));

        try {
            let response = await fetchWithRefresh("/api/payment/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ cart: cartForBackend })
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Erreur ${response.status} : ${text}`);
            }

            const data = await response.json();

            if (!data.clientSecret || !data.amount) throw new Error("Données inattendues du serveur.");

            document.getElementById("total-price").innerHTML = `<strong>Total : ${(data.amount / 100).toFixed(2)}€</strong>`;

            const result = await stripe.confirmCardPayment(data.clientSecret, {
                payment_method: { card: cardElement }
            });

            if (result.error) {
                cardErrors.textContent = result.error.message;
                payButton.disabled = false;
                payButton.textContent = "Payer";
            } else if (result.paymentIntent.status === "succeeded") {
                Swal.fire({
                    icon: 'success',
                    title: 'Paiement réussi !',
                    text: 'Merci pour votre achat.',
                    confirmButtonText: 'OK'
                }).then(() => {
                    localStorage.removeItem("panier");
                    window.location.href = "/";
                });
            }
        } catch (err) {
            console.error("Erreur de paiement :", err);
            Swal.fire({
                icon: 'error',
                title: 'Erreur',
                text: "Erreur lors du paiement : " + err.message
            });
            payButton.disabled = false;
            payButton.textContent = "Payer";
        }
    });
});
