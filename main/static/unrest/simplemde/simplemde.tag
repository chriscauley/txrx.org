(function() {
  uR.config.input_overrides['simplemde-input'] = 'simplemde-input';
  uR.form.fields['simplemde-input'] = class SimpleMDEInput extends uR.form.URInput {
    reset() {
      this.field_tag.simplemde.codemirror.setValue("arstarst");
    }
  }
})();

<simplemde-input>
  <textarea></textarea>

  var self = this
  this.on("mount",function() {
    var options = {
      element: this.root.querySelector("textarea"),
      spellChecker: false,
      initialValue: this.field.initial_value,
    };
    this.simplemde = new SimpleMDE(options);
    window.S = this.simplemde;
    window.T = this;
    this.simplemde.codemirror.on("change", function(){
      self.field.value = self.simplemde.codemirror.getValue();
    });
  });
</simplemde-input>
