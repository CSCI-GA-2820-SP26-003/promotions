const API_BASE_URL = "/promotions";

const nameFilter = document.getElementById("nameFilter");
const activeFilter = document.getElementById("activeFilter");
const searchBtn = document.getElementById("searchBtn");
const clearBtn = document.getElementById("clearBtn");
const promotionList = document.getElementById("promotionList");
const messageBox = document.getElementById("messageBox");

function showMessage(text, type = "info") {
    messageBox.textContent = text;
    messageBox.className = `message ${type}`;
    messageBox.style.display = "block";
}

function hideMessage() {
    messageBox.style.display = "none";
    messageBox.textContent = "";
}

function formatPromotionType(type) {
    const typeMap = {
        1: "Percentage",
        2: "Amount",
        3: "Free Shipping"
    };

    return typeMap[type] || type || "N/A";
}

function renderPromotions(promotions) {
    promotionList.innerHTML = "";

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
            <p>
                <strong>Status:</strong>
                <span class="badge ${activeClass}">${activeText}</span>
            </p>
        `;

        promotionList.appendChild(card);
    });
}

async function handleSearch() {
    hideMessage();
    promotionList.innerHTML = "";

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
    promotionList.innerHTML = "";
    hideMessage();
}

searchBtn.addEventListener("click", handleSearch);
clearBtn.addEventListener("click", handleClear);