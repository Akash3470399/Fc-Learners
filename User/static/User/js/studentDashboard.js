base_url = window.location.protocol +"//"+window.location.host;
let blog_list = document.querySelector("#blog-list");
let notes_list = document.querySelector("#note-list");
const detail_page_url = "/detail-page/";

let moreBlogBtn = document.querySelector("#more-blog-btn");
let moreNotesBtn = document.querySelector("#more-notes-btn");


// for more blog (pagination)
moreBlogBtn.onclick = function (e) {
  
  let page_num = e.target.getAttribute("data-next-blog");

  fetch(base_url + "/user/dash-blogs-paginated/" + "?page="+page_num)
    .then((res) => res.json())
    .then((data) => {

      if(data['status'] ==  'success'){
        data["blogs_list"].forEach(blog => {
          blog_list.innerHTML += `<tr>
                                                    <td><a href="${detail_page_url + blog[0]}/">${blog[1]}</a></td>
                                                    <td> ${blog[2]} </td> 
                                                    <td>
                                                        <p id="likes">${blog[3]}</p>&nbsp;&nbsp;
                                                        <span  class="las la-thumbs-up"></span >
                                                        </td> 
                                                    <td>
                                                        <p id="likes">${blog[4]}</p>&nbsp;&nbsp;
                                                        <span   class="las la-comments"></span >
                                                        </td>                                 
                                                </tr>`;
          if(data['next_page_num'])
            moreBlogBtn.setAttribute("data-next-blog", data['next_page_num']);
          else
            moreBlogBtn.remove();          
        });
      }

    });
}

// for more notes
moreNotesBtn.onclick = function (e){
  let page_num = e.target.getAttribute("data-next-note");
  fetch(base_url + "/user/dash-notes-paginated/?page=" + page_num
  ).then( res => res.json()
  ).then(data => {
    if(data['status'] == 'success'){
      data['notes_list'].forEach(note => {
                 let noteElement = ` <tr>
                        <td>${note['title']}</td>
                        <td>${note['subject']} </td>
                        `;
                        let status = "";
                        if (note['status'] == "Accepted")
                            status = `<td> <span class="status green"></span>${ note['status']}</td>`; 
                        else if (note['status'] == "Pending")
                            status = `<td> <span class="status yellow"></span>${note['status']}</td>`; 
                        else if (note['status'] == "Review")
                            status = `<td> <span class="status red"></span>${note['status']}</td>`; 

                        status += ` <td><a href=""><span  class="las la-trash"></a></span> </td> 
                        <td><a href=""><span  class="las la-edit"></a></span> </td>                          
                    </tr>`;
                    noteElement += status;

                    notes_list.innerHTML += noteElement;

                    if(data['next_page_num'])
                      moreNotesBtn.setAttribute("data-next-note", data['next_page_num'])
                    else
                      moreNotesBtn.remove();
        });
    }
  });
}

