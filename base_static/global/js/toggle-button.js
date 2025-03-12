const body = document.querySelector("body");
const toggle = document.querySelector("#toggle");
const moonIcon = document.querySelector(".toggle .fa-moon");
const sunIcon = document.querySelector(".toggle .fa-sun");

toggle.addEventListener("change", () => {
    body.classList.toggle("light-theme");
});
