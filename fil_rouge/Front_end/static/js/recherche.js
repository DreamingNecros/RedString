document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("recherche-form");
    const resultats = document.getElementById("resultats-produits");
    const pagination = document.getElementById("pagination");

    let currentPage = 1;

    form.addEventListener("submit", e => {
        e.preventDefault(); 
        currentPage = 1;
        rechercherProduits();
    }); //cette partie permet de rediger vers la page des produit

    function rechercherProduits() {
        const formData = new FormData(form);
        let params = new URLSearchParams();

        formData.forEach((value, key) => {
            if (value) params.append(key, value);
        });

        params.append("page", currentPage);

        fetch(`/api/recherche/?${params.toString()}`)
            .then(res => res.json())
            .then(data => {
                afficherProduits(data.results);
                afficherPagination(data.count, data.next, data.previous);
            });
    }

    function afficherProduits(produits) {
        resultats.innerHTML = "";
        produits.forEach(p => {
            resultats.innerHTML += `
                <div class="card m-2" style="width: 18rem;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${p.name}</h5>
                        <p class="card-text">${p.description}</p>
                        <p class="card-text">Prix : ${p.price} €</p>
                        <p class="card-text">Stock : ${p.stock}</p>
                        <p class="card-text">Catégorie : ${p.category.name}</p>
                        <div class="form-group">
                            <label for="quantity_${p.id}">Quantité :</label>
                            <input type="number" id="quantity_${p.id}" value="1" min="1" max="${p.stock}" class="form-control">
                        </div>
                        <button class="btn btn-primary btn-ajout-panier mt-2"
                                data-id="${p.id}"
                                data-name="${p.name}"
                                data-stock="${p.stock}">
                            Ajouter au panier
                        </button>
                    </div>
                </div>
            `;
        });
        activerBoutonsAjout();
    }

    function afficherPagination(count, next, previous) {
        pagination.innerHTML = "";

        if (previous) {
            const prevPage = new URL(previous).searchParams.get("page");
            pagination.innerHTML += `<button onclick="changerPage(${prevPage})" class="btn btn-secondary m-1">Précédent</button>`;
        }

        if (next) {
            const nextPage = new URL(next).searchParams.get("page");
            pagination.innerHTML += `<button onclick="changerPage(${nextPage})" class="btn btn-secondary m-1">Suivant</button>`;
        }
    }

    window.changerPage = function (page) {
        currentPage = page;
        rechercherProduits();
    }

    function activerBoutonsAjout() {
        const boutons = document.querySelectorAll(".btn-ajout-panier");
        boutons.forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.dataset.id;
                const name = btn.dataset.name;
                const stock = parseInt(btn.dataset.stock);
                const quantity = parseInt(document.getElementById(`quantity_${id}`).value);
                ajouterAuPanier(id, stock, name, quantity);
            });
        });
    }

    rechercherProduits(); // Appel initial
});
