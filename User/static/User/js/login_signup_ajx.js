base_url = window.location.protocol + "//" + window.location.host;

sign_up_form = document.querySelector("form.sign-up-form");
login_in_form = document.querySelector("form.sign-in-form");

let signin_validatonBox = document.querySelector("form.sign-in-form > div.validation-box");
let signup_validatonBox = document.querySelector("form.sign-up-form > div.validation-box");


// to remove messages & red border from validation box & input fields respectively.
Array.from(document.querySelectorAll("input")).forEach(inp => {
  inp.addEventListener('click', () => {
    Array.from(document.querySelectorAll("div.input-field")).forEach(element => {
      element.style.border = "none";
    });
    signin_validatonBox.innerHTML = "";
    signup_validatonBox.innerHTML = "";
  })
});


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
            document.querySelector("#sign-in-btn").click();
          else
            invalidSignUPMsg(data['errors']);          
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
      else
        invalidLoginMsg(data['errors']); // show appropiate messages
  })

}


// to add appropiate messages on invalid credentials
function invalidLoginMsg(errors)
{
  let signin_emailField = document.querySelector(
    "form.sign-in-form > div.input-field"
  );
  let signin_passField = document.querySelectorAll(
    "form.sign-in-form > div.input-field"
  )[1];
  if ("email" in errors) {
    signin_emailField.style.border = "2px solid #ff4d4d";
    signin_validatonBox.innerHTML = `${errors["email"]}`;
    signin_validatonBox.removeAttribute("hidden");
  } else if ("password" in errors) {
    signin_passField.style.border = "2px solid #ff4d4d";
    signin_validatonBox.innerHTML = `${errors["password"]}`;
    signin_validatonBox.removeAttribute("hidden");
  }
}


// to show messages on invalid informaton during 
function invalidSignUPMsg(errors)
{
  signup_validatonBox.innerHTML += "";
  let inps = document.querySelectorAll("form.sign-up-form > div.input-field");
  let name_ = inps[0];
  let email = inps[1];
  let pass1 = inps[2];
  let pass2 = inps[3];
  
  inps = {'name':name_, 'email':email, 'password1':pass1, 'password2':pass2}


  for(var key in errors){
    signup_validatonBox.innerHTML += `<i class="fa-duotone fa-circle"></i> ${errors[key][0]}<br>`;
    inps[key].style.border = "2px solid #ff4d4d";
  }
}