const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".parent-container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  document.title = "Sign Up";
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  document.title = "Sign In"
});