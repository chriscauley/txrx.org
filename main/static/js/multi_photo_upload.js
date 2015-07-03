jQuery(document).ready(function() {
  var $ = jQuery;

  function dropHandler(e) {
    e.preventDefault();

    var files = e.originalEvent.dataTransfer.files;

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    formData.append('content_type',window._PHOTOS.content_type);
    formData.append('object_pk',window._PHOTOS.object_id);
    formData.append('name',$("#photos_name").val());
    var csrf_token = $('[name=csrfmiddlewaretoken]').val()
    formData.append('csrfmiddlewaretoken', csrf_token)

    var xhr = new XMLHttpRequest();
    var post_url = "/admin/media/photo/bulk/";
    xhr.open('POST', post_url);
    xhr.onload = function () {
      var i;
      var text = this.responseText;
      if (xhr.status === 200) {
          loadPhotos(JSON.parse(xhr.responseText));
      } else {
        alert("An unknown error has occurred, go bug Chris");
      }
    };
    // Here's where the form, with photos attached, is actually posted:
    xhr.send(formData);
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
  function loadPhotos(photo) {
    
  }
  riot.mount("photo-list",{'photos': window._PHOTOS.photos});
});
