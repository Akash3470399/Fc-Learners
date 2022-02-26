base_url = window.location.protocol + "//" + window.location.host;

sign_up_form = document.querySelector("form.sign-up-form");
login_in_form = document.querySelector("form.sign-in-form");

sign_up_form.onsubmit = function(e){
    e.preventDefault();
    
    formdata = new FormData(sign_up_form);

    fetch(base_url + "/user/register/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": formdata.get("csrfmiddlewaretoken").toString(),
      },
      body: JSON.stringify({
        email: formdata.get("email"),
        name: formdata.get("name"),
        password1: formdata.get("password1"),
        password2: formdata.get("password2"),
        is_teacher:formdata.get('is_teacher')
      }),
    })
      .then((res) => res.json())
      .then((data) => {
          if(data['status'] == 'success')
          {
            location.reload();
          }
          else{
            console.log(data['errors']);
          }
        });
}

login_in_form.onsubmit = function(e){
  e.preventDefault();

  let formdata = new FormData(login_in_form);

  fetch(base_url + "/user/login/", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": formdata.get("csrfmiddlewaretoken").toString(),
    },
    body: JSON.stringify({
      'email':formdata.get('email'),
      'password':formdata.get('password')
    })
  })
  .then( res => res.json()
  ).then(data => {
      if(data['status'] == 'success')
        {
          if(window.location.search)
            window.location.href = window.location.search.replace("?next=", "");
          else
            window.location.href = "/";
        }
      else{
        console.log(data)
      }
  })

}


