// script.js
function toggleSidebar() {
    const sidebarMenu = document.getElementById("sidebarMenu");
    sidebarMenu.classList.toggle("show"); // Toggle the "show" class
}
document.addEventListener('DOMContentLoaded', () => {
    // Sélection des éléments
    const menuBtn = document.getElementById('menuBtn');
    const closeBtn = document.getElementById('closeBtn');
    const sidebarMenu = document.getElementById('sidebarMenu');

    if (menuBtn && closeBtn && sidebarMenu) {
        // Afficher le menu
        menuBtn.addEventListener('click', () => {
            sidebarMenu.classList.add('show');
        });

        // Masquer le menu
        closeBtn.addEventListener('click', () => {
            sidebarMenu.classList.remove('show');
        });

        // Masquer le menu lorsque l'on clique sur un lien
        const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                sidebarMenu.classList.remove('show');
            });
        });
    } else {
        console.error('Erreur : Les éléments du menu latéral ne sont pas disponibles.');
    }
});
//MENU
document.addEventListener("DOMContentLoaded", function () {
    const menuItems = document.querySelectorAll(".menu-item");
    const submenus = document.querySelectorAll(".submenu");

    // Ouvrir le menu
    (document.querySelector(".menu-icon")).addEventListener("click", () => {
        (document.querySelector(".menu-container")).classList.add("active");
    });

    // Fermer le menu
    (document.querySelector(".close-btn")).addEventListener("click", () => {
        (document.querySelector(".menu-container")).classList.remove("active");
    });

    // Gestion des sous-menus
    menuItems.forEach((item) => {
        item.addEventListener("click", () => {
            const target = item.getAttribute("data-target");

            // Masquer tous les sous-menus
            submenus.forEach((submenu) => {
                submenu.classList.remove("active");
            });

            // Afficher le sous-menu sélectionné
            const activeSubmenu = document.getElementById(target);
            if (activeSubmenu) {
                activeSubmenu.classList.add("active");
            }
        });
    });
// Sélection des éléments
const menuIcon = document.querySelector('.menu-icon');
const menuContainer = document.querySelector('.menu-container');
const closeBtn = document.querySelector('.close-btn');

// Afficher le menu
    (document.querySelector(".menu-icon")).addEventListener('click', () => {
    (document.querySelector(".menu-container")).classList.add('active');
});

// Masquer le menu
    (document.querySelector(".close-btn")).addEventListener('click', () => {
    (document.querySelector(".menu-container")).classList.remove('active');
});


});
//POUR masquer la barre sup lors de l'affichage du menu
document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelector(".menu-icon");
    const closeBtn = document.querySelector(".close-btn");
    const menuContainer = document.querySelector(".menu-container");
    const topBar = document.querySelector(".top-bar");

    // Afficher le menu et cacher la barre supérieure
    menuIcon.addEventListener("click", function () {
        menuContainer.classList.add("active");
        topBar.classList.add("hidden"); // Ajoute la classe .hidden pour cacher la barre supérieure
    });

    // Fermer le menu et réafficher la barre supérieure
    closeBtn.addEventListener("click", function () {
        menuContainer.classList.remove("active");
        topBar.classList.remove("hidden"); // Retire la classe .hidden pour réafficher la barre supérieure
    });
});

//FIN MENU

