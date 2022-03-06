let notes_list = document.querySelector("#notes-list");
let pages = document.querySelectorAll("a.page-link");
let base_url = window.location.protocol + "//" + window.location.host;

if (pages) {
  Array.from(pages).forEach((link) => {
    link.addEventListener("click", get_page);
  });
}

function get_page(e) {
  e.preventDefault();
  let page_no = e.target.getAttribute("href");
  fetch(base_url + "/study-material/study-material-listing/" + page_no)
    .then((res) => res.json())
    .then((data) => {
      if (data["status"] == "success") {
        notes_list.innerHTML = data["data"];
        let pages = notes_list.querySelectorAll("a.page-link");
        if (pages) {
          console.log(pages);
          Array.from(pages).forEach((link) => {
            link.addEventListener("click", get_page);
          });
        }
      }
    });
}
