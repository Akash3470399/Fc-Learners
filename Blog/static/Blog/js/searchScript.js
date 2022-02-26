base_url = window.location.protocol + "//" + window.location.host;

// getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;



// if user press any key and release
inputBox.onkeyup = (e)=>{
    suggBox.innerHTML = "";
    let inputData = e.target.value; //user enetered data
    let emptyArray = [];
    if(inputData){
        icon.onclick = ()=>{
        }

    fetch(base_url+'/search/'+inputData)
    .then( res => res.json())
    .then(data => {
        
        let page_btns = document.querySelectorAll("a.page-link");
        let posts_div = document.querySelector("div#posts");
        posts_div.innerHTML = data['res'];

        page_btns = posts_div.querySelectorAll("a.page-link");
        Array.from(page_btns).forEach((btn) =>
        btn.addEventListener("click", getPage));

        if(data['status'] == 'success'){
            data["data"].forEach((result) => {
            suggBox.innerHTML += `<li onclick="select(this)" data-post_no="${result[1]}">${result[0]}</li>`;
            });
        }
        else
            suggBox.innerHTML = `<li>results not found.</li>`;
    });
    searchWrapper.classList.add("active"); //show autocomplete box
    
    }else{
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}

function select(element){
    
    let selectData = element.textContent;
    post_no = element.dataset.post_no;
    document.location.href = base_url + `/detail-page/${post_no}`;
    inputBox.value = "";

    icon.onclick = ()=>{
        document.location.href = base_url + `/detail-page/${post_no}`;
    }
    // searchWrapper.classList.remove("active");
}

