tinymce.init({
  selector: "#tinymce-textarea", // change this value according to your HTML
  images_upload_url: "upload-image/", // Image upload address in Django route
  height: 300,
  plugins: [
    "advlist autolink link image lists charmap print preview hr anchor pagebreak",
    "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
    "emoticons template help",
  ],
  toolbar:
    "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | " +
    "bullist numlist outdent indent | print preview media fullscreen | " +
    "forecolor backcolor emoticons | help",
  menu: {
    favs: {
      title: "My Favorites",
      items: "code visualaid | searchreplace | emoticons",
    },
  },
  menubar: "favs file edit view insert format tools table help",
  image_advtab: true,
  image_title: true,
  automatic_uploads: true,
});
