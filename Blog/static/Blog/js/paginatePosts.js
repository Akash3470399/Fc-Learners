let page_btns = document.querySelectorAll("a.page-link");
let posts_div = document.querySelector("div#posts");
let base_url = (window.location.protocol + "//" + window.location.host);

Array.from(page_btns).forEach(btn => 
    btn.addEventListener('click', getPage)
);

function getPage(e){
    e.preventDefault();

    let url = base_url + "/paginated_posts" + this.getAttribute("href");
    
    fetch(url)
    .then(res => res.json())
    .then(data => {
        posts_div.innerHTML = data['res'];

        page_btns = posts_div.querySelectorAll("a.page-link");
        Array.from(page_btns).forEach((btn) =>
        btn.addEventListener("click", getPage)
        );
    });
    
}