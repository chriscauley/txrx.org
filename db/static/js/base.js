function poptastic(url) {
  var newwindow = window.open(url,'name','height=390,width=650');
  if (window.focus) {newwindow.focus()}
}

function miniSlideShow(wrapper,start_at) {
  if (!start_at) { start_at = 0; }
  var ul = $(wrapper).children("ul,ol");
  var width = ul.children()[0].scrollWidth;
  ul.css({width: (width*ul.children().length)+"px"});
  var out = {
    ul: ul,
    i: start_at,
    max: Math.ceil(ul.children().length)-2,
    next: function() { this.i++; this.scroll() },
    prev: function() { this.i--; this.scroll() },
    scroll: function(speed,push) {
      if (push == undefined) { push = true; }
      if (!!speed) { speed = "slow"; }
      $(".prev,.next").show();
      if (this.i == this.max) { $(".next").hide(); }
      if (this.i == 0) { $(".prev").hide(); }
      $(wrapper).animate({scrollLeft: width*this.i},speed);
      if (push != 0) { pushPage(this.i); }
    }
  }
  out.scroll(0,false);
  window.onpopstate = function(event) {
    var page = window.location.href.match(/page=(\d+)#?$/);
    if (!!page) { out.i = page[1]*1 }
    else if (!window.location.href.match(/entry=(\d+)$#?/)) { out.i = 0 }
    out.scroll("slow",false)
  };
  return out;
}

function pushPage(i) {
  if (!!(window.history && history.pushState)) {
    history.pushState({},'',window.location.pathname+"?page="+i)
  }
}

function showSearch() {
  $("#search_box").show().animate({width: 155},"slow");
  window.showSearch = function() { $("#header .top form").submit() };
}

function showOther(that,update) {
  if (!!$(that).val()) { return }
  var text = $("<input type='text'>");
  text.attr("name",that.name);
  $(that).parent().append(text);
  $(that).detach();
  text.focus();
  if (!!update) {
    $(text).hide()[0].value = "Option 6";
    var text2 = $("<input type='text'>");
    text.parent().append(text2);
    text2.focus();
    $(text2).keyup(function() {
      var a6 = $("[name=option_amount6]");
      a6.val($(this).val());
    });
  }
}

$(document).ready(function(){
  /*$("#tweet").tweet({
    // Use username searches instead of query searches to avoid
    // lag on api.twitter.com.
    username: "bluecurenews",
    join_text: "auto",
    avatar_size: 20,
    count: 5,
    auto_join_text_default: "we said,",
    auto_join_text_ed: "we",
    auto_join_text_ing: "we were",
    auto_join_text_reply: "we replied to",
    auto_join_text_url: "we were checking out",
    loading_text: "",
    template: function(item) {
      return '<div class="tweet-info">' + item["time"] + '&ndash; '
        + item["text"] + '</div>';
    }
  });

  (function() {
    // IE8 and presumably IE9 are incapable of passing extra
    // parameters via setTimeout, so a closure is used.
    var index = 1;
    var rotate_tweets = function() {
      index += 1;
      var li_elems = $("#tweet ul li");
      if (li_elems.length > 0) {
        index = index % li_elems.length;
        li_elems.hide();
        li_elems.slice(index, index+1).show();
        setTimeout(rotate_tweets, 5000);
      }
    };
    setTimeout(rotate_tweets, 5000);
  })();
*/
});
