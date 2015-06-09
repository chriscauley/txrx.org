jQuery(document).ready(function() {
  var $ = jQuery;

  function dropHandler(e) {
    e.preventDefault();

    var files = e.originalEvent.dataTransfer.files;

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    formData.append('name',$("#photos_name").val());
    var csrf_token = $('[name=csrfmiddlewaretoken]').val()
    formData.append('csrfmiddlewaretoken', csrf_token)

    var xhr = new XMLHttpRequest();
    var post_url = "";
    xhr.open('POST', post_url);
    xhr.onload = function () {
      var i;
      var text = this.responseText;
      if (xhr.status === 200) {
        var photos = JSON.parse(xhr.responseText);
        for (i = 0; i<photos.length; i++) {
          loadPhoto(photos[i]);
        }
      } else {
        alert("An unknown error has occurred, go bug Chris");
      }
    };
    // Here's where the form, with photos attached, is actually posted:
    xhr.send(formData);
  }

  for (var i=0;i<window.ADMIN_PHOTOS.length;i++) {
    var photo = window.ADMIN_PHOTOS[i];
    loadPhoto(photo);
  }
  $('.dropzone').bind("dragenter", function(e) {
    e.preventDefault();
    $(e.target).addClass("hover");
  }).bind("dragleave", function(e) {
    e.preventDefault();
    $(e.target).removeClass("hover");
  }).bind("dragover", function(e) {
    e.preventDefault();
  }).bind("drop", dropHandler);
  function loadPhoto(photo) {
    if (window.PHOTO_TEMPLATE) {
      var fragment = Mustache.render(window.PHOTO_TEMPLATE,photo)
      $("#images_list").append($(fragment));
    } else {
      $.get(
        "/static/mustache/admin/photo.html",
        function(template) {
          window.PHOTO_TEMPLATE = template;
          loadPhoto(photo);
        }
      );
    }
  }
});
