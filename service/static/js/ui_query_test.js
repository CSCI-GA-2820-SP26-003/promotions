const API_BASE_URL = "/promotions";
//create buttons
const createBtn = document.getElementById("create-btn");
const createName = document.getElementById("pet_name");
const createType = document.getElementById("pet_promotion_type");
const createValue = document.getElementById("pet_value");
const createStartDate = document.getElementById("pet_start_date");
const createEndDate = document.getElementById("pet_end_date");

const nameFilter = document.getElementById("nameFilter");
const activeFilter = document.getElementById("activeFilter");
const searchBtn = document.getElementById("search-btn");
const clearBtn = document.getElementById("clear-btn");
const search_results = document.getElementById("search_results");
const flash_message = document.getElementById("flash_message");
const promotionIdInput = document.getElementById("promotionId");
const retrieveBtn = document.getElementById("retrieve-btn");
const retrieveResult = document.getElementById("retrieveResult");

let promotionsCache = [];

function showMessage(text, type = "info") {
    flash_message.textContent = text;
    flash_message.className = `message ${type}`;
    flash_message.style.display = "block";
}

function hideMessage() {
    flash_message.style.display = "none";
    flash_message.textContent = "";
}

// function formatPromotionType(type) {
//     const typeMap = {
//         1: "Percentage",
//         2: "Amount",
//         3: "Free Shipping"
//     };

//     return typeMap[type] || type || "N/A";
// }

function formatPromotionType(type) {
    const typeMap = {
        PERCENT_OFF: "Percentage",
        BUY_N_GET_ONE: "Buy N Get One",
        FIXED_DISCOUNT: "Fixed Discount",
        FREE_SHIPPING: "Free Shipping",
        PAYBACK_PERCENT: "Payback Percent"
    };

    return typeMap[type] || type || "N/A";
}

function renderPromotions(promotions) {
    search_results.innerHTML = "";

    promotions.forEach((promotion) => {
        const card = document.createElement("div");
        card.className = "promotion-card";

        const isActive = promotion.active === true || promotion.active === "true";
        const activeClass = isActive ? "active" : "inactive";
        const activeText = isActive ? "Active" : "Inactive";

        card.innerHTML = `
            <h3>${promotion.name || "No Name"}</h3>
            <p><strong>ID:</strong> ${promotion.id}</p>
            <p><strong>Description:</strong> ${promotion.description || "N/A"}</p>
            <p><strong>Type:</strong> ${formatPromotionType(promotion.promotion_type)}</p>
            <p><strong>Value:</strong> ${promotion.value ?? "N/A"}</p>
            <p><strong>Start Date:</strong> ${promotion.start_date || "N/A"}</p>
            <p><strong>End Date:</strong> ${promotion.end_date || "N/A"}</p>
            <p>
                <strong>Status:</strong>
                <span class="badge ${activeClass}">${activeText}</span>
            </p>
        `;

        const actions = document.createElement("div");
        actions.className = "actions";

        const editBtn = document.createElement("button");
        editBtn.textContent = "Edit";
        editBtn.className = "btn-secondary";

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.className = "btn-danger";

        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);

        const form = document.createElement("form");
        form.className = "edit-form";
        form.style.display = "none";

        form.innerHTML = `
            <div class="form-row">
                <div>
                    <label for="name-${promotion.id}">Name</label>
                    <input id="name-${promotion.id}" name="name" type="text" value="${promotion.name || ""}" required />
                </div>
                <div>
                    <label for="description-${promotion.id}">Description</label>
                    <input id="description-${promotion.id}" name="description" type="text" value="${promotion.description || ""}" />
                </div>
            </div>
            <div class="form-row">
                <div>
                    <label for="type-${promotion.id}">Type</label>
                    <select id="type-${promotion.id}" name="promotion_type">
                        <option value="1" ${Number(promotion.promotion_type) === 1 ? "selected" : ""}>Percentage</option>
                        <option value="2" ${Number(promotion.promotion_type) === 2 ? "selected" : ""}>Amount</option>
                        <option value="3" ${Number(promotion.promotion_type) === 3 ? "selected" : ""}>Free Shipping</option>
                    </select>
                </div>
                <div>
                    <label for="value-${promotion.id}">Value</label>
                    <input id="value-${promotion.id}" name="value" type="number" value="${promotion.value ?? ""}" />
                </div>
            </div>
            <div class="form-row">
                <div>
                    <label for="start-${promotion.id}">Start Date</label>
                    <input id="start-${promotion.id}" name="start_date" type="date" value="${promotion.start_date ? promotion.start_date.split("T")[0] : ""}" />
                </div>
                <div>
                    <label for="end-${promotion.id}">End Date</label>
                    <input id="end-${promotion.id}" name="end_date" type="date" value="${promotion.end_date ? promotion.end_date.split("T")[0] : ""}" />
                </div>
                <div>
                    <label for="active-${promotion.id}">Active</label>
                    <select id="active-${promotion.id}" name="active">
                        <option value="true" ${isActive ? "selected" : ""}>True</option>
                        <option value="false" ${!isActive ? "selected" : ""}>False</option>
                    </select>
                </div>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn-primary">Save</button>
                <button type="button" class="btn-secondary" data-action="cancel">Cancel</button>
            </div>
        `;

        editBtn.addEventListener("click", () => {
            form.style.display = form.style.display === "none" ? "block" : "none";
        });

        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            await handleUpdate(promotion.id, form);
        });

        form.querySelector('[data-action="cancel"]').addEventListener("click", () => {
            form.style.display = "none";
        });

        deleteBtn.addEventListener("click", async () => {
            await handleDelete(promotion.id);
        });

        card.appendChild(actions);
        card.appendChild(form);

        search_results.appendChild(card);
    });
}

function buildPayloadFromForm(promotionId, form) {
    const formData = new FormData(form);
    const payload = {
        id: promotionId,
        name: formData.get("name")?.trim(),
        description: formData.get("description")?.trim() || null,
        promotion_type: Number(formData.get("promotion_type")),
        value: formData.get("value") ? Number(formData.get("value")) : null,
        start_date: formData.get("start_date") || null,
        end_date: formData.get("end_date") || null,
        active: formData.get("active") === "true",
    };

    return payload;
}

async function handleUpdate(promotionId, form) {
    hideMessage();

    const payload = buildPayloadFromForm(promotionId, form);

    if (!payload.name) {
        showMessage("Name is required to update a promotion.", "error");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/${promotionId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Update failed with status ${response.status}`);
        }

        const updated = await response.json();
        promotionsCache = promotionsCache.map((promo) =>
            promo.id === promotionId ? updated : promo
        );

        renderPromotions(promotionsCache);
        showMessage("Promotion updated successfully.", "success");
    } catch (error) {
        console.error("Update failed:", error);
        showMessage("An error occurred while updating the promotion.", "error");
    }
}

async function handleDelete(promotionId) {
    hideMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/${promotionId}`, {
            method: "DELETE",
        });

        if (!response.ok && response.status !== 204) {
            throw new Error(`Delete failed with status ${response.status}`);
        }

        promotionsCache = promotionsCache.filter((promo) => promo.id !== promotionId);
        renderPromotions(promotionsCache);
        showMessage("Promotion deleted successfully.", "success");
    } catch (error) {
        console.error("Delete failed:", error);
        showMessage("An error occurred while deleting the promotion.", "error");
    }
}

async function handleSearch() {
    hideMessage();
    search_results.innerHTML = "";

    const nameValue = nameFilter.value.trim();
    const activeValue = activeFilter.value;

    const params = new URLSearchParams();

    if (nameValue) {
        params.append("name", nameValue);
    }

    if (activeValue) {
        params.append("active", activeValue);
    }

    if ([...params.keys()].length === 0) {
        showMessage("Please enter at least one search criterion.", "info");
        return;
    }

    const url = `${API_BASE_URL}?${params.toString()}`;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const promotions = Array.isArray(data) ? data : (data.promotions || []);

        promotionsCache = promotions;

        if (promotions.length === 0) {
            showMessage("No promotions match the search criteria.", "info");
            return;
        }

        renderPromotions(promotions);
    } catch (error) {
        console.error("Search failed:", error);
        showMessage("An error occurred while retrieving promotions.", "error");
    }
}

function handleClear() {
    nameFilter.value = "";
    activeFilter.value = "";
    search_results.innerHTML = "";
    promotionsCache = [];
    hideMessage();
}

async function handleRetrieve() {
    hideMessage();
    retrieveResult.innerHTML = "";

    const id = promotionIdInput.value.trim();

    if (!id) {
        showMessage("Please enter a promotion ID.", "info");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);

        if (response.status === 404) {
            showMessage(`Promotion with ID ${id} was not found.`, "error");
            return;
        }

        const promotion = await response.json();
        retrieveResult.innerHTML = `
            <div class="promotion-card">
                <h3>${promotion.name || "No Name"}</h3>
                <p><strong>ID:</strong> ${promotion.id}</p>
                <p><strong>Description:</strong> ${promotion.description || "N/A"}</p>
                <p><strong>Type:</strong> ${formatPromotionType(promotion.promotion_type)}</p>
                <p><strong>Status:</strong> ${promotion.active ? "Active" : "Inactive"}</p>
            </div>
        `;

    } catch (error) {
        console.error("Retrieve failed:", error);
        showMessage("Error retrieving promotion.", "error");
    }
}
async function handleCreate() {
    hideMessage();

    const typeMap = {
        PERCENT_OFF: 1,
        BUY_N_GET_ONE: 2,
        FIXED_DISCOUNT: 3,
        FREE_SHIPPING: 4,
        PAYBACK_PERCENT: 5
    };

    const payload = {
        name: createName.value.trim(),
        promotion_type: typeMap[createType.value],
        value: createValue.value ? Number(createValue.value) : null,
        start_date: createStartDate.value || null,
        end_date: createEndDate.value || null,
        active: true
    };

    if (!payload.name) {
        showMessage("Name is required.", "error");
        return;
    }
    if (!payload.value) {
        showMessage("Value is required.", "error");
        return;
    }

    if (!createStartDate.value || !createEndDate.value) {
        showMessage("Start date and end date are required.", "error");
        return;
    }

    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            let msg = "Create failed";
            try {
                const errorData = await response.json();
                msg = errorData.message || msg;
            } catch (e) {
                const text = await response.text();
                msg = text;
            }
            throw new Error(msg);
        }

        const created = await response.json();
        showMessage("Promotion created successfully.", "success");

        // reset form
        createName.value = "";
        createValue.value = "";
        createStartDate.value = "";
        createEndDate.value = "";

        // update UI
        promotionsCache.push(created);
        renderPromotions(promotionsCache);

    } catch (error) {
        console.error("Create failed:", error);
        showMessage(error.message, "error");
    }
}

searchBtn.addEventListener("click", handleSearch);
clearBtn.addEventListener("click", handleClear);
retrieveBtn.addEventListener("click", handleRetrieve);
createBtn.addEventListener("click", handleCreate);