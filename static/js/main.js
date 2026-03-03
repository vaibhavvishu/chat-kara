document.addEventListener('DOMContentLoaded', function () {
    // Navbar Toggler logic
    const navbarToggler = document.getElementById('navbar-toggler');
    const navbarLinks = document.getElementById('navbar-links');

    if (navbarToggler) {
        navbarToggler.addEventListener('click', function () {
            navbarLinks.classList.toggle('active');
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
