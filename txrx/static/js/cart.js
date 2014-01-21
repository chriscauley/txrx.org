function loadJSON(url) { window.location = url; } // IE Fallback
function showLogin() {
  $("#login-dialog").toggleClass("login-visible");
}


simpleCart.successURL = window.location.origin+"/classes/?success"
simpleCart.cartHeaders = ["Name", "Price", "Quantity", "Remove"]

function showCart() {
  $("#cart-modal").modal({width: 400, modal: true, minHight: 300});
}
function addClass(session_id) {
  var session = window.SESSIONS_ON_PAGE[session_id];
  addItem(session.name,session.fee,session_id);
  toggleCourses(session.name);
}
function addItem(name,price,id) {
  simpleCart.add('name='+name,'price='+price,'id='+id,'quantity=1');
}
function toggleCourses(name) {
  $(".in-cart").removeClass("in-cart");
  for (id in simpleCart.items) { $("#c"+id).addClass("in-cart") }
  simpleCart.update();
  $("#cartEmpty").hide();
  if ($("#cart .itemContainer").length == 0) { $("#cartEmpty").show(); }
  $(".recentAdd").removeClass("recentAdd");
  $(".itemContainer").each(function() {
    if ($(this).find(".itemName").text() == name) {
      $(this).addClass("recentAdd");
    }
  })
}

function rsvp(session_id,url) {
  var row = $("#c"+session_id);
  row.addClass("loading");
  row.find(".message".hide);
  $.get(
    url,
    function(data) {
      row.removeClass("loading");
      if (data[0]>0) {
	row.find(".RsvpLink").addClass("attending");
	row.find(".number_attending").text("RSVP'd x "+data[0])
      }
      else { row.find(".RsvpLink").removeClass("attending"); }
      row.removeClass("full");
      if (data[2]) { row.addClass("full"); }
      row.find(".message").css("display","block").html(data[1]);
    },
    "json"
  )
}