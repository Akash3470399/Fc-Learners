const searchWrapper = document.querySelector(".search-input");
let queryInput = document.querySelector("div.search-input > input");
suggBoxWrapper = document.querySelector(".wrapper");
try {
  if (!base_url) {
    let base_url = window.location.protocol + "//" + window.location.host;
  }
  if (!notes_list) {
    let notes_list = document.querySelector("#notes-list");
  }
} catch (error) {}

queryInput.onkeyup = function () {
  let query = queryInput.value;
  if(query){    
    fetch(base_url + "/study-material/search-notes/" + "?q=" + query)
        .then((res) => res.json())
        .then((data) => {
        if (data["status"] == "success") {
            notes_list.innerHTML = data["data"];
        }
        else{
            notes_list.innerHTML = `
                    <div class="card text-center">
                        <div class="card-body">
                            <h3 class="card-text bg-warning">
                                Result not found....
                            </h3>
                        </div>
                    </div>
            `;
        }
        });
  }
  else{
      window.location.reload();
  }
};
