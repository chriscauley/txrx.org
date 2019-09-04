<markdown><yield/>
  this.on("mount",function() {
    var content = this.content ||this.opts.content || this.root.innerHTML;
    if (this.opts.url && !content) {
      uR.ajax({
        url: this.opts.url,
        success: (function(data,request) {
          this.opts.content = request.responseText;
          this.mount();
        }).bind(this)
      });
      return
    }
    this.root.innerHTML = markdown.toHTML(content.replace("&amp;","&"));
  });
  setContent(content) {
    this.content = content;
    this.mount();
  }
</markdown>
