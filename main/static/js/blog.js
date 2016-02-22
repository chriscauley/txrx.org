function insertImage(chunk,callback) {
  window.wmd_chunk = chunk;
  window.current_modal = "#image-modal";
  window.iframe_callback = callback;
  $("#image-modal iframe").attr("src","/media_files/photo/insert/");
  $("#image-modal").modal('show');
}
function addImage() {
  $("#image-modal iframe").attr("src","/media_files/photo/add/");
}
function insertShortCode(obj) {
  var out = wmd_chunk.before.trimRight()+"\n\n";
  out += obj.shortcode;
  out += "\n\n"+wmd_chunk.after.trimLeft();
  $("#wmd-input").val(out.trim());
  $(current_modal).modal('hide');
}
function insertID(obj) {
  $("#id_photo").val(obj.id);
  $(current_modal).modal('hide');
}
function extractor(query) {
  var result = /([^,]+)$/.exec(query);
  if(result && result[1])
    return result[1].trim();
  return '';
}

function initBlag() {
  /* a function to initialize blog javascript */
  $("#id_tags").attr("autocomplete","off");

  $("#lookup_id_photo").attr("href","javascript:;").attr("onclick","");
  $("#lookup_id_photo").click(function(){insertImage('',insertID)})
  $('#id_tags').typeahead({
    source: window.tagsAutocomplete,
    updater: function(item) {
      return this.$element.val().replace(/[^,]*$/,'')+item+',';
    },
    matcher: function (item) {
      var tquery = extractor(this.query);
      if(!tquery) return false;
      return ~item.toLowerCase().indexOf(tquery)
    },
    highlighter: function (item) {
      var query = extractor(this.query).replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
      return item.replace(new RegExp('(' + query + ')', 'ig'), function ($1, match) {
        return '<strong>' + match + '</strong>'
      })
    }
  });
}
