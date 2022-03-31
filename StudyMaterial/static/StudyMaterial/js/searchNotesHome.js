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
            let newli = `<a href="${base_url + note[1]}" target="_blank"><li>${
              note[0]
            }</li></a>`;
            notes_list.innerHTML += newli;
          });
        }
        else{
            notes_list.innerHTML = "<li>No result found</li>";
        }
        });
        searchWrapper.classList.add("active");
  }
  else{
      window.location.reload();
      searchWrapper.classList.remove("active");
  }
};
