<photo-list>
  <photo class="col-sm-6 col-md-4 col-lg-3" each={ photos }>
    <img src="{ thumbnail }" />
    <div class="name">{ name }</div>
  </photo>
  this.photos = this.opts.photos;
</photo-list>
