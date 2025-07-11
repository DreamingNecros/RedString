document.addEventListener("DOMContentLoaded", function () {
    const boutonsAjout = document.querySelectorAll(".btn-ajout-panier");

    boutonsAjout.forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const name = button.dataset.name;
            const stock = parseInt(button.dataset.stock);
            const price = parseFloat(button.dataset.price);

            // Récupérer la quantité depuis l'input correspondant
            const quantityInput = document.getElementById(`quantity_${id}`);
            const quantity = parseInt(quantityInput.value);

            ajouterAuPanier(id, stock, name, quantity, price);

            const message = document.getElementById("message-ajout-panier");
            if (message) {
                message.style.display = "block";
                setTimeout(() => {
                    message.style.display = "none";
                }, 3000);
            }

        });
    });

    // Affiche automatiquement le panier si le container existe sur la page
    if (document.getElementById("panier-container")) {
        afficherPanier();
    }
});


function ajouterAuPanier(id, stock, name, quantity, price) {
    let panier = JSON.parse(localStorage.getItem("panier") || "{}");

    if (panier[id]) {
        panier[id].quantity += quantity;
    } else {
        panier[id] = {
            name: name,
            quantity: quantity,
            stock: stock,
            price: price
        };
    }

    if (panier[id].quantity > stock) {
        panier[id].quantity = stock;
    }

    localStorage.setItem("panier", JSON.stringify(panier));

    if (document.getElementById("panier-container")) {
        afficherPanier();
    }
}

function afficherPanier() {
    const panierContainer = document.getElementById("panier-container");
    if (!panierContainer) return;

    const panier = JSON.parse(localStorage.getItem("panier") || "{}");

    if (Object.keys(panier).length === 0) {
        panierContainer.innerHTML = "<p class='text-muted'>Votre panier est vide.</p>";
        return;
    }

    let totalProduits = 0;
    let html = `
        <h3>Votre Panier</h3>
        <table class="table table-bordered table-striped">
            <thead class="thead-dark">
                <tr>
                    <th>Nom</th>
                    <th>Quantité</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const id in panier) {
        const produit = panier[id];
        totalProduits += produit.quantity;

        html += `
            <tr>
                <td>${produit.name}</td>
                <td>
                    <input type="number" min="1" max="${produit.stock}" value="${produit.quantity}"
                        class="form-control"
                        onchange="modifierQuantite('${id}', this.value)">
                </td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="supprimerProduit('${id}')">Supprimer</button>
                </td>
            </tr>
        `;
    }

    html += `
            </tbody>
        </table>
        <p><strong>Total d'articles :</strong> ${totalProduits}</p>
        <button class="btn btn-secondary" onclick="viderPanier()">Vider le panier</button>
        <button id="pay-button" class="btn btn-primary btn-block">Payer</button>
    `;

    panierContainer.innerHTML = html;

    // Gestion clic du bouton Payer
    const payButton = document.getElementById("pay-button");
    payButton.addEventListener("click", () => {
        const jwtToken = localStorage.getItem("access_token");

        if (!jwtToken) {
            alert("Vous devez être connecté pour payer.");
            window.location.href = "/login/";
            return;
        }
        // payeUrl doit être défini dans le template ou dans un script global
        if (typeof payeUrl !== 'undefined') {
            window.location.href = payeUrl;
        } else {
            alert("URL de paiement non définie.");
        }
    });
}

function modifierQuantite(id, newQuantity) {
    let panier = JSON.parse(localStorage.getItem("panier") || "{}");

    if (panier[id]) {
        newQuantity = parseInt(newQuantity);
        if (newQuantity >= 1 && newQuantity <= panier[id].stock) {
            panier[id].quantity = newQuantity;
        }
        localStorage.setItem("panier", JSON.stringify(panier));
        afficherPanier();
    }
}

function supprimerProduit(id) {
    let panier = JSON.parse(localStorage.getItem("panier") || "{}");
    delete panier[id];
    localStorage.setItem("panier", JSON.stringify(panier));
    afficherPanier();
}

function viderPanier() {
    localStorage.removeItem("panier");
    afficherPanier();
}
