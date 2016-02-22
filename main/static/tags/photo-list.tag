<photo-list>
  <div class="rows foreground_loading">
    <div id="dropzone" class="fourth dropzone"></div>
    <photo class="fourth background_loading" each={ photos }>
      <div class="buttons">
        <button class="btn btn-danger" onclick={ parent.untag } title="Will not delete photo from database">
          <i class="fa fa-times"></i> Unlink</button>
        <button class="btn btn-danger" onclick={ parent.delete } title="Will delete from database">
          <i class="fa fa-warning"></i> Delete</button>
        <a class="btn btn-primary" href="/admin/media/photo/{ id }">
          <i class="fa fa-pencil-square"></i> Edit</a>
      </div>
      <img src="{ thumbnail }" if={ thumbnail }/>
      <div data-error={ error } if={ error }></div>
      <div class="name" contenteditable="true" onkeyup={ parent.editName }>{ name }</div>
    </photo>
  </div>

  this.photos = window._PHOTOS.photos;
  var that = this;
  var edit_timeout;
  this.on("mount",function() {
    $("#dropzone").bind("dragenter", function(e) {
      e.preventDefault();
      $(e.target).addClass("hover");
    }).bind("dragleave", function(e) {
      e.preventDefault();
      $(e.target).removeClass("hover");
    }).bind("dragover", function(e) {
      e.preventDefault();
    }).bind("drop", opts.dropHandler);
  });
  editName(e) {
    clearTimeout(edit_timeout);
    $(e.target).closest('photo').addClass("loading").removeClass("success");
    edit_timeout = setTimeout(function() {
      $.post(
        '/media_files/photo/edit/'+e.item.id+'/',
        {name:e.target.innerText},
        function(data) {
          $(e.target).closest('photo').removeClass("loading").addClass("success");
        }
      )
    },500);
  }
  function removePhoto(id) {
    for (var i=0;i<window._PHOTOS.photos.length;i++) {
      if (window._PHOTOS.photos[i].id == id) { window._PHOTOS.photos.splice(i,1); }
    }
    riot.update("photo-list");
  }
  untag(e) {
    $.post(
      '/media_files/photo/untag/',
      {
        content_type:window._PHOTOS.content_type,
        object_id:window._PHOTOS.object_id,
        photo_id: e.item.id
      },
      function(data) {
        removePhoto(e.item.id);
      }
    )
  }
  delete(e) {
    var warn = "This will delete this photo entirely from the site. Don't do this unless you are certain";
    if (confirm(warn)) {
      $.post(
        '/media_files/photo/delete/'+e.item.id+'/',
        function(data) {
          removePhoto(e.item.id);
        }
      )
    }
  }
</photo-list>

<photo-search>
  <form onsubmit={ search }>
    <input name="q" onkeyup={ search }>
    <div class="search_results rows">
      <div onclick={ parent.select } each={ search_results } class="fourth btn btn-primary">
        <img src="{ thumbnail }" />
        <div class="name">{ name }</div>
      </div>
    </div>
  </div>

  var that = this;
  var search_timeout;
  search(e) {
    clearTimeout(search_timeout);
    var q = that.q.value;
    if (!q || q.length < 3) { return }
    search_timeout = setTimeout(function() {
      $.get(
        "/media_files/photo/search/",
        {q:that.q.value},
        function(data) {
          that.search_results = data;
          that.update();
        },
        "json"
      )
    },200);
    return true;
  }
  select(e) {
    $.get(
      "/media_files/photo/tag/",
      {
        content_type:window._PHOTOS.content_type,
        object_id:window._PHOTOS.object_id,
        photo_id: e.item.id
      },
      function(data) {
        that.search_results = [];
        that.update();
        if (data) { //data is true/false depending on whether or not a tag was created
          window._PHOTOS.photos.unshift(e.item);
          riot.update("photo-list");
        }
      }
    )
  }
</photo-search>
