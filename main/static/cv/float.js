$(function() {
  $("form.cvfloat [placeholder]").each(function() {
    var cvfloat = $("<label cvfloat='"+this.placeholder+"'></label>");
    //this.placeholder = '';
    cvfloat.attr("for",this.id);
    $(this).before(cvfloat);
    function f() {
      if (this.value.length == 0) {cvfloat.addClass("down");} 
      else { cvfloat.removeClass('down'); }
    }
    f = f.bind(this);
    $(this).bind("keyup change blur",f);

    f();
    // run to catch autocomplete
    setTimeout(f,500);
    setTimeout(f,1000);
    setTimeout(f,5000);
  });
});
