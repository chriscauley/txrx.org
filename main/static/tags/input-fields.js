riot.tag('input-field', '<div if="{ !tagname }"> <label if="{ label }" for="{ id }" class="{ required: required, labelclass }"> { label }</label> <input name="{ name }" id="{ id }" type="{ type }" value="{ value }"> <div if="{ error }" class="alert alert-danger error">{ error }</div> </div>', function(opts) {

  this.on("update", function() {
    this.id = this.id || this.name?"id_"+this.name:undefined;
    this.value = this.value || "";
  });


});
