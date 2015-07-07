jQuery(document).ready(function() {
  var $ = jQuery;

  function dropHandler(e) {
    e.preventDefault();
    $("photo-list .rows").addClass("loading");

    var files = e.originalEvent.dataTransfer.files;

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    formData.append('content_type',window._PHOTOS.content_type);
    formData.append('object_id',window._PHOTOS.object_id);
    var csrf_token = $('[name=csrfmiddlewaretoken]').val()
    formData.append('csrfmiddlewaretoken', csrf_token)

    var xhr = new XMLHttpRequest();
    var post_url = "/media_files/photo/bulk_upload/";
    xhr.open('POST', post_url);
    xhr.onload = function () {
      var i;
      var text = this.responseText;
      if (xhr.status === 200) {
        var new_photos = JSON.parse(xhr.responseText);
        var i = new_photos.length;
        while (i--) {
          window._PHOTOS.photos.unshift(new_photos[i]);
        }
        riot.update("photo-list");
        $("photo-list .rows").removeClass("loading");
      } else {
        alert("An unknown error has occurred, go bug Chris");
      }
    };
    // Here's where the form, with photos attached, is actually posted:
    xhr.send(formData);
  }

  riot.mount("photo-list",{dropHandler:dropHandler});
  riot.mount('photo-search',{});
});
