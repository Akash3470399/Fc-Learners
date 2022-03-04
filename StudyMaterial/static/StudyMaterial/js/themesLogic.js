base_url = document.location.protocol + "//" + document.location.host;
var modeicon = document.getElementById("modeicon");


if(localStorage.getItem("theme") == null) // if theme value is not there in localStorages then save it fist
    localStorage.setItem("theme", "lightMode");
else if (localStorage.getItem('theme') == "darkMode") // if theme value is dark mode then toggle value of dark mode variable.
  {
     // modeicon.src = base_url + "img/sun.png";
      document.body.classList.toggle("dark-theme");
  }  

modeicon.onclick = function () {
  document.body.classList.toggle("dark-theme");
  if (document.body.classList.contains("dark-theme")) {
      localStorage.setItem("theme", "darkMode");;
    //modeicon.src ="sun.png";
  } else {
      localStorage.setItem("theme", "lightMode");
   // modeicon.src ="moon.png";
  }
};
