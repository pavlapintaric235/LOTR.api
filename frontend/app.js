console.log("app.js loaded");

const API_URL = "https://lotr-api-gs1y.onrender.com/characters/";
const container = document.getElementById("characters");

const modal = document.getElementById("character-modal");
const closeModalButton = document.getElementById("close-modal");
const modalImage = document.getElementById("modal-image");
const modalName = document.getElementById("modal-name");
const modalAge = document.getElementById("modal-age");
const modalRace = document.getElementById("modal-race");
const modalDescription = document.getElementById("modal-description");

async function loadCharacters() {
  try {
    const response = await fetch(API_URL);
    const characters = await response.json();

    container.innerHTML = "";

    characters.forEach((character) => {
      const card = document.createElement("article");
      card.className = "character-card";


      card.innerHTML = `
        <img src="${character.image}" alt="${character.name}" class="character-image" />
        <div class="character-card-content">
          <h2 class="character-name">${character.name}</h2>
          <p class="character-meta"><strong>Age:</strong> ${character.age}</p>
          <p class="character-meta"><strong>Race:</strong> ${character.race}</p>
          <p class="description-preview">${character.description}</p>
          <p class="click-more">Click to read more...</p>
        </div>
      `;
        card.addEventListener("click", () => openModal(character));
        container.appendChild(card);
    });
  } catch (error) {
    console.error("Error loading characters:", error);
    container.innerHTML = "<p>Could not load characters.</p>";
  }
}

function openModal(character) {
  modalImage.src = character.image;
  modalImage.alt = character.name;
  modalName.textContent = character.name;
  modalAge.textContent = character.age;
  modalRace.textContent = character.race;
  modalDescription.innerHTML = character.description;

  modal.classList.remove("hidden");
}

function closeModal() {
  modal.classList.add("hidden");
}

closeModalButton.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

loadCharacters();