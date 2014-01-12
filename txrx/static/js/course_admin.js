// Set the first date according to the value of the first class time
// runs on save 

django.jQuery(function() {
  var $ = django.jQuery;
  $("[type=submit]").click(function() {
    try {
      var startDate = new Date(2099,1,1);
      $(".start .vDateField").each(function(){
	var day = this.value;
	var time = $(this).siblings("[type=text]")[0].value
	var _d = new Date(day+" "+time);
	if (_d < startDate) {
	  startDate = _d;
	  $("[name=first_date_0]").val(day);
	  $("[name=first_date_1]").val(time);
	}
      });
    }
    catch (e) {}
  })
})