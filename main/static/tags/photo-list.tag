<photo-list>
  <div class="rows">
    <div id="dropzone" class="fourth dropzone"></div>
    <photo class="fourth" each={ photos }>
      <img src="{ thumbnail }" if={ thumbnail }/>
      <div data-error={ error } if={ error }></div>
      <div class="name">{ name }</div>
    </photo>
  </div>

  this.photos = window._PHOTOS.photos;
  var that = this;
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
        object_pk:window._PHOTOS.object_id,
        photo_pk: e.item.pk
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
