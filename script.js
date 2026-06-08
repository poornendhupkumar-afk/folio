/* ==========================================
   PORTFOLIO - script.js
   Features:
   1. Dark Mode Toggle
   2. Back To Top Button
   3. Scroll Reveal Animation
========================================== */


/* ==========================================
   1. DARK MODE TOGGLE
========================================== */

const themeToggle = document.querySelector("#theme-toggle");

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    const isDark = document.body.classList.contains("dark");

    themeToggle.textContent = isDark
        ? "☀️ Light Mode"
        : "🌙 Dark Mode";
});


/* ==========================================
   2. BACK TO TOP BUTTON
========================================== */

const toTop = document.querySelector("#to-top");

if (toTop) {

    window.addEventListener("scroll", () => {

        if (window.scrollY > 300) {
            toTop.classList.add("show");
        } else {
            toTop.classList.remove("show");
        }

    });

    toTop.addEventListener("click", () => {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });
}


/* ==========================================
   3. SCROLL REVEAL ANIMATION
========================================== */

const revealItems = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(

    (entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {

                entry.target.classList.add("is-visible");

                observer.unobserve(entry.target);
            }

        });

    },

    {
        threshold: 0.15
    }
);

revealItems.forEach((item) => {
    observer.observe(item);
});
const buttons = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".project-item");
const counter = document.getElementById("project-count");

buttons.forEach(btn => {
    btn.addEventListener("click", () => {

        document.querySelector(".filter-btn.active")
            .classList.remove("active");

        btn.classList.add("active");

        const filter = btn.dataset.filter;
        let visible = 0;

        cards.forEach(card => {

            if(filter === "all" ||
               card.dataset.category === filter){

                card.classList.remove("hide");
                visible++;

            } else {

                card.classList.add("hide");

            }

        });

        counter.textContent =
            visible + (visible === 1 ? " Project" : " Projects");
    });
});