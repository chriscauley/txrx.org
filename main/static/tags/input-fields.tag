<input-field>
  <div if={ !tagname }>
    <label if={ label } for={ id } class={ required: required, labelclass }>
      { name && label }</label>
    <input name={ name } id={ id } type={ type } value={ value } placeholder={ placeholder }>
    <div if={ error } class="alert alert-danger error">{ error }</div>
  </div>

  this.on("update", function() {
    this.id = this.id || this.name?"id_"+this.name:undefined;
    this.value = this.value || "";
  });
/*
  this.on("mount",function() {
    var tagname = this.opts.tagname;
    if (tagname == "input") { return }
    var tag = document.createElement(tagname);
    this.root.appendChild(tag);
    riot.mount(tagname,tag);
  });
*/
</input-field>
