document.addEventListener('DOMContentLoaded', () => {
  // Sélection des éléments
  const menuIcon = document.querySelector('.menu-icon');
  const closeBtn = document.querySelector('.close-btn');
  const menuContainer = document.querySelector('.menu-container');
  const topBar = document.querySelector('.top-bar');
  const menuItems = document.querySelectorAll('.menu-item');
  const submenus = document.querySelectorAll('.submenu');

  // Vérification des éléments nécessaires
  if (menuIcon && closeBtn && menuContainer) {
    // Afficher le menu et cacher la barre supérieure
    menuIcon.addEventListener('click', () => {
      menuContainer.classList.add('active');
      if (topBar) topBar.classList.add('hidden'); // Cache la barre supérieure
    });

    // Masquer le menu et réafficher la barre supérieure
    closeBtn.addEventListener('click', () => {
      menuContainer.classList.remove('active');
      if (topBar) topBar.classList.remove('hidden'); // Réaffiche la barre supérieure
    });
  } else {
    console.error('Erreur : Les éléments principaux du menu ne sont pas disponibles.');
  }

  // Gestion des sous-menus
  if (menuItems && submenus) {
    menuItems.forEach((item) => {
      item.addEventListener('click', () => {
        const target = item.getAttribute('data-target');

        // Masquer tous les sous-menus
        submenus.forEach((submenu) => submenu.classList.remove('active'));

        // Afficher le sous-menu sélectionné
        const activeSubmenu = document.getElementById(target);
        if (activeSubmenu) {
          activeSubmenu.classList.add('active');
        }
      });
    });
  }

  // Initialisation de Swiper
  if (typeof Swiper !== 'undefined') {
    new Swiper('.slide-content', {
      slidesPerView: 3,
      spaceBetween: 25,
      loop: true,
      centerSlide: 'true',
      grabCursor: 'true',
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
        dynamicBullets: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        520: {
          slidesPerView: 2,
        },
        950: {
          slidesPerView: 3,
        },
      },
    });
  } else {
    console.error('Swiper non défini. Assurez-vous que la bibliothèque est incluse.');
  }
});
