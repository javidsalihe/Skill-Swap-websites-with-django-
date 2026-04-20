document.addEventListener("DOMContentLoaded", function () {

  setupMobileMenu();

  // Set up logout button
  document.getElementById("logoutBtn").addEventListener("click", function () {
    if (confirm("Möchten Sie sich wirklich abmelden?")) {
      alert(
        "Erfolgreich abgemeldet! In einer echten Anwendung würden Sie zur Login-Seite weitergeleitet."
      );
    }
  });

  // Handle window resize
  window.addEventListener("resize", handleResize);
  handleResize(); // Initial check
});


// Set up mobile hamburger menu
function setupMobileMenu() {
  const hamburgerBtn = document.getElementById("hamburgerBtn");
  const sidebar = document.getElementById("sidebar");

 hamburgerBtn.addEventListener("click", function () {
    sidebar.classList.toggle("active");
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener("click", function (e) {
    if (
      window.innerWidth <= 992 &&
      !sidebar.contains(e.target) &&
      !hamburgerBtn.contains(e.target)
/*
        &&
      sidebar.classList.contains("active")*/
    ) {
      //sidebar.classList.remove("active");
    }
  });
}

// Handle window resize
function handleResize() {
  // Hide sidebar on mobile when resizing to larger screen
  if (window.innerWidth > 992) {
    //document.getElementById("sidebar").classList.remove("active");

    // Show desktop tables, hide mobile tables
    document.querySelectorAll(".desktop-table").forEach((el) => {
      el.style.display = "block";
    });
    document.querySelectorAll(".mobile-table").forEach((el) => {
      el.style.display = "none";
    });
  } else {
    // Show mobile tables, hide desktop tables
    document.querySelectorAll(".desktop-table").forEach((el) => {
      el.style.display = "none";
    });
    document.querySelectorAll(".mobile-table").forEach((el) => {
      el.style.display = "block";
    });
  }
}

// Initialize page-specific functionality
function initializePage(pageId) {
  if (pageId === "benutzer") {
    // Add user button functionality
    document
      .getElementById("addUserBtn")
      ?.addEventListener("click", function () {
        alert(
          "In einer vollständigen Implementierung würde hier ein Formular zum Hinzufügen eines neuen Benutzers geöffnet."
        );
      });
  }

  if (pageId === "einstellungen") {
    // Settings form submission
    document
      .getElementById("settingsForm")
      ?.addEventListener("submit", function (e) {
        e.preventDefault();
        alert("Einstellungen wurden gespeichert!");
      });
  }

  // Handle responsive table display
  handleResize();
}
