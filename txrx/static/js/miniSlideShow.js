function miniSlideShow(wrapper,opts) {
  if (!opts) { opts = {} }
  var defaults = {
    oncall: function(){},
    callback: function(){},
    start_at: 0,
    interval: false, // stopped with out.stop()
    timeout: false, // persists
    wrap: false
  }
  for (key in defaults) {
    if (!opts[key]) { opts[key]=defaults[key]; }
  }
  var ul = $(wrapper).children("ul,ol");
  if (ul.children().length < 2) {
    $(wrapper).parent().find(".prev,.next").detach();
    return
  }
  if (opts.wrap) { ul.append(ul.children().first().clone()); }
  var width = ul.children()[0].scrollWidth;
  ul.css({width: (width*ul.children().length)+"px"});
  var out = {
    ul: ul,
    i: opts.start_at,
    max: ul.children().length-1,
    next: function() { this.i++; this.scroll(); },
    prev: function() { this.i--; this.scroll(); },
    scrollTo: function(i) { this.i = i; this.scroll(); },
    stop: function(){ clearInterval(this.interval); },
    scroll: function(speed,stop) {
      opts.oncall();
      if (stop) { this.stop() }
      if (!!speed) { speed = 300; }
      if (this.i >= 0) {
	$(wrapper).animate({scrollLeft: width*this.i},speed,opts.callback);
      }
      if (opts.wrap) {
	if (this.i == this.max) {
	  this.i = 0;
	  $(wrapper).animate({scrollLeft: 0},0);
	}
	if (this.i == -1) {
	  this.i = this.max-1;
	  $(wrapper).animate({scrollLeft: width*this.max},0);
	  this.scroll();
	}
      } else {
	$(".prev,.next").show();
	if (this.i == this.max) { $(".next").hide(); }
	if (this.i == 0) { $(".prev").hide(); }
      }
      $(".slide-nav a").removeClass("active").eq(this.i).addClass("active");
      if (!!opts.timeout) {
	clearTimeout(this.timeout);
	this.timeout = setTimeout(function(){out.next()},opts.timeout);
      }
    }
  }
  if (!!opts.interval) { out.interval = setInterval(function(){out.next()},opts.interval) }
  out.scroll(0);
  return out;
}