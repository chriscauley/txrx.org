<modal>
  <div class="mask" onclick={ cancel }></div>
  <div class="inner">
    <div class="title">{ opts.title }</div>
    <yield/>
  </div>

  <style scoped>
  :scope {
    display: block;
    position: fixed;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
    justify-content: center;
    z-index: 1000;
  }
  :scope, .mask {
    bottom: 0;
    left: 0;
    right: 0;
    top: 0;
  }
  .mask {
    background: rgba(0,0,0,0.3);
    position: absolute;
    z-index: 1;
  }
  .inner {
    align-self: center;
    display: inline-block;
    background: white;
    min-width: 300px;
    padding: 15px;
    position: relative;
    z-index: 2;
  }
  .title {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 10px;
  }
  </style>

  cancel() {
    this.unmount();
  }
  success(e) {
    (this.opts.success || function(){})();
    this.unmount();
  }
</modal>
