$(function() {
  var numDisplay = 3;
  if ($(window).width() < 480) {
    $("[data-lightbox]").removeAttr("data-lightbox");
    //uncomment when the site becomes responsive
    //numDisplay = 2;
  }
  if ($(window).width() < 350) {
    //uncomment when the site becomes responsive
    //numDisplay = 1;
  }
  $(".photoset").each(function() {
    if ($(this).find("li").length > 2) {
      $(this).find("ul").addClass("ts-list");
      $(this).thumbScroller({
	responsive:true,
	numDisplay:numDisplay,
	slideWidth:200,
	slideHeight:200,
	slideMargin:5,
	slideBorder:2,
	padding:10,
	navButtons:'hover',
	playButton:false,
	continuous:true,
      });
    }
  });
  //$('a').bind('touchend', function(e) {
  //  $(this).click();
  //});
});
