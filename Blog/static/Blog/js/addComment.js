let base_url = window.location.protocol + "//" + window.location.host;
let form = document.querySelector("form");
let comment_inp = document.querySelector("#comment-inp");


// adding comments 
form.onsubmit = function (e) {
    e.preventDefault();
    formdata = new FormData(form);
    data = {
      article_id: formdata.get("post_id"),
      comment_text: formdata.get("comment_text"),
    };

    fetch(base_url + "/add-comment/", {
        method : "POST",
        headers: {
            Accept:"application/json",
            "X-Requested-With":"XMLHttpRequest",
            "X-CSRFToken":formdata.get('csrfmiddlewaretoken')
        },
        body : JSON.stringify(data)
    })
    .then(
         res => res.json()
    )
    .then(
        data => {
            let commentList = document.querySelector("ul.media-list");
            
            if(data['status'] == "success")
            {
                let cmt_count = document.querySelector("#commets-count");
                cmt_count.innerText = (Number(cmt_count.innerText) + 1);
                comment = `
                        <li class="media">
                        <div class="comment">
                            <div class="author-img">
                                <img src="https://randomuser.me/api/portraits/women/87.jpg"
                                    class="rounded-circle s-sm-2 " alt="" />
                            </div>
                            <h5 class="media-heading">${data['comment']['user']}</h5>
                            <div class="media-body">
                                <p>
                                    ${data['comment']['comment_text']}
                                </p>
                            </div>
                        </div>
                    </li>
                `;
                if(commentList.firstElementChild.nodeName == "SPAN") // if comment box is empty  so it contains span 
                {
                    commentList.innerHTML = comment;
                    comment_inp.value = "";
                }
                else if(commentList.lastElementChild.nodeName == "LI")
                {
                    commentList.innerHTML += comment;
                    comment_inp.value = "";
                }
                else if(commentList.lastElementChild.nodeName == "A")
                {
                        let more_cmt_btn =commentList.lastElementChild;
                        commentList.lastElementChild.remove();
                        commentList.innerHTML += comment;
                        commentList.appendChild(more_cmt_btn);
                        comment_inp.value = "";
                }
            }
        }
    )
}

// get next comments

function getComments(linkElement)
{
    let commentList = document.querySelector("ul.media-list");
    let next_page = linkElement.getAttribute("data-next-page");
    let post_id = linkElement.getAttribute("data-post-no");

    let url = base_url + "/get-comments/" + post_id + "/" + "?page=" + next_page; 
    fetch(url)
    .then(res => res.json())
    .then( data => {
        if(data['status'] == 'success'){
            commentList.lastElementChild.remove();
            commentList.innerHTML += data['res'];
        }
    })
}


function add_like(post_id){
    alert(post_id);
    url = base_url + "/add-like?post_id=" + post_id; 
    fetch(url).then(res => res.json()).then(data => {
        document.querySelector("#likes-count").innerText = Number(document.querySelector("#likes-count").innerText) + 1;
    });
}
