'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

(function () {
  uR.config.input_overrides['simplemde-input'] = 'simplemde-input';
  uR.form.fields['simplemde-input'] = function (_uR$form$URInput) {
    _inherits(SimpleMDEInput, _uR$form$URInput);

    function SimpleMDEInput() {
      _classCallCheck(this, SimpleMDEInput);

      return _possibleConstructorReturn(this, (SimpleMDEInput.__proto__ || Object.getPrototypeOf(SimpleMDEInput)).apply(this, arguments));
    }

    _createClass(SimpleMDEInput, [{
      key: 'reset',
      value: function reset() {
        this.field_tag.simplemde.codemirror.setValue("arstarst");
      }
    }]);

    return SimpleMDEInput;
  }(uR.form.URInput);
})();

riot.tag2('simplemde-input', '<textarea></textarea>', '', '', function (opts) {

  var self = this;
  this.on("mount", function () {
    var options = {
      element: this.root.querySelector("textarea"),
      spellChecker: false,
      initialValue: this.field.initial_value
    };
    this.simplemde = new SimpleMDE(options);
    window.S = this.simplemde;
    window.T = this;
    this.simplemde.codemirror.on("change", function () {
      self.field.value = self.simplemde.codemirror.getValue();
    });
  });
});