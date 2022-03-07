const searchWrapper = document.querySelector(".search-input");
let queryInput = document.querySelector("div.search-input > input");
suggBoxWrapper = document.querySelector(".wrapper");
let base_url = window.location.protocol + "//" + window.location.host;
let notes_list = document.querySelector(".autocom-box");

queryInput.onkeyup = function () {
  let query = queryInput.value;
  if(query){    
    fetch(base_url + "/study-material/search-notes/" + "?q=" + query)
        .then((res) => res.json())
        .then((data) => {
        if (data["status"] == "success") {
          notes_list.innerHTML ="";
          data["notes_list"].forEach(note => {
            let newli = `<li><a href="${base_url + note[1]}">${note[0]}</a></li>`;
            notes_list.innerHTML += newli;
          });
          searchWrapper.classList.add("active");
        }
        else{
            notes_list.innerHTML = "<li>No result found</li>";
        }
        });
  }
  else{
      window.location.reload();
      searchWrapper.classList.remove("active");
  }
};
