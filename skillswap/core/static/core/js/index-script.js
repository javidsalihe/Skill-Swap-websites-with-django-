const popUpMenuDiv = document.getElementById("PopupMenu");
const barsBtn = document.querySelector(".bars-div");
const closeBtn = document.querySelector(".close-div");

function navbar_open() {
  popUpMenuDiv.classList.remove("hidden");
  barsBtn.classList.add("hidden");
  closeBtn.classList.remove("hidden");
}

function navbar_close() {
  popUpMenuDiv.classList.add("hidden");
  barsBtn.classList.remove("hidden");
  closeBtn.classList.add("hidden");
}



function startAutoSlider(trackId) {
    const track = document.getElementById(trackId);
    let index = 0;
    const cards = track.children;
    const cardWidth = cards[0].offsetWidth + 20; // Breite der Karte + Gap (20px)

    setInterval(() => {
        index++;

        // Wenn wir am Ende sind, zurück zum Anfang
        if (index >= cards.length - 1) {
            index = 0;
        }

        track.style.transform = `translateX(-${index * cardWidth}px)`;
    }, 3000); // Alle 3 Sekunden
}

// Starte beide Slider, wenn die Seite geladen ist
window.onload = function() {
    startAutoSlider('track1');
    startAutoSlider('track2');
};