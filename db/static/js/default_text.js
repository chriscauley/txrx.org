/*Created by Chris Cauley February 2012 for Mouth Watering Media
Creates default text in an input element when the element is empty.
Requires any jquery > 1.4.3

Will be automatically applied to any $("input[data-default-text]")
Applies the class "default-text" and replaces the value with [data-default-text] if blank.
*/
$(document).ready(function() {
  function defaultFocus() {
    if (this.value == $(this).data("defaultText")) {
      this.value = "";
      $(this).removeClass("default-text");
    }
  }
  function defaultBlur() {
    if (!this.value || this.value == $(this).data("defaultText")) {
      this.value = $(this).data("defaultText");
      $(this).addClass("default-text");
    }
  }
  $("input[data-default-text]").focus(defaultFocus).blur(defaultBlur).blur();
});
