function insertImage(chunk,callback) {
  window.wmd_chunk = chunk;
  window.current_modal = "#image-modal";
  window.iframe_callback = function(result) {
    callback(result);
    $("#image-modal").modal('hide');
  }
  $("#image-modal iframe").attr("src","/media_files/photo/insert/");
  $("#image-modal").modal('show');
}
function addImage() {
  $("#image-modal iframe").attr("src","/media_files/photo/add/");
}

function insertID(obj) {
  $("#id_photo").val(obj.id);
  $(current_modal).modal('hide');
}

function initBlag() {
  /* a function to initialize blog javascript */
  $("#id_tags").attr("autocomplete","off");

  $("#lookup_id_photo").attr("href","javascript:;").attr("onclick","");
  $("#lookup_id_photo").click(function(){insertImage('',insertID)})
}
