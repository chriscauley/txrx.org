// Set the first date according to the value of the first class time
// runs on save 

django.jQuery(function() {
  var $ = django.jQuery;
  $("[name=first_date_0]").closest(".field-first_date").hide();
  $("[name=last_date_0]").closest(".field-last_date").hide();
  $("[type=submit]").click(function() {
    try {
      var startDate = new Date(2599,1,1);
      var endDate = new Date(1999,1,1);
      $(".field-start .vDateField").each(function(){
	var day = this.value;
	var time = $(this).siblings("[type=text]")[0].value
	var _d = new Date(day+" "+time);
        var end_time = $(this).closest(".form-row").find(".field-end_time .vTimeField").val();
        var _e = new Date(day+" "+end_time);
	if (_d < startDate) {
	  startDate = _d;
	  $("[name=first_date_0]").val(day);
	  $("[name=first_date_1]").val(time);
	}
	if (_e > endDate) {
	  endDate = _e;
	  $("[name=last_date_0]").val(day);
	  $("[name=last_date_1]").val(end_time);
	}
      });
    }
    catch (e) {console.log(e)}
  })
})
