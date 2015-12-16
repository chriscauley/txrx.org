<modal>
  <div class="mask" onclick={ cancel }></div>
  <div class="inner">
    <a onclick={ cancel } class="cancel">X</a>
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
    overflow: auto;
    z-index: 1000;
  }
  :scope.absolute { position: absolute; }
  @media (max-width: 480px) { /* we'll need all the space we can get in mobile */
    :scope.absolute { position: fixed; }
  }
  :scope, .mask {
    bottom: 0;
    left: 0;
    right: 0;
    top: 0;
  }
  .cancel {
    background: black;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    display: block;
    height: 26px;
    line-height: 26px;
    position: absolute;
    right: -13px;
    text-align: center;
    text-decoration: none;
    top: -13px;
    width: 26px;
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
    max-width: 100%;
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

  var that = this;
  cancel(e) {
    (this.opts.cancel || function(){})(e);
    this.unmount();
  }
  success(e) {
    (this.opts.success || function(){})();
    this.unmount();
  }
  this.parent.on("update",function() { that.update() });
</modal>
