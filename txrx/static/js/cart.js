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
  if ($("#cart .itemContainer").length == 0) { $("#cartEmpty").show(); $("#mobileCart").hide() }
  else { $("#mobileCart").show(); }
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
  row.find(".message").hide();
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
      if (data[1]) { row.find(".RsvpLink .message").html(data[1]).show(); };
    },
    "json"
  )
}

function startCheckout() {
  var data = [];
  var cart_items = simpleCart.items;
  for (id in cart_items) {
    data.push({pk: id, quantity: cart_items[id].quantity})
  }
  $.get(
    "/classes/start_checkout/",
    {"cart": JSON.stringify(data)},
    function (data) { verifyCheckout(data); },
    "json"
  )
}

function verifyCheckout(data) {
  if (data.length == 0) { createCookie("checkout_initiated","yes!",10);simpleCart.checkout(); return; }
  var msg = "Sorry, some of the classes you're trying to take have filled since you first loaded this page."
  msg += "\nThe following have been removed from your cart:"
  for (var i=0; i < data.length; i++) {
    var cart_item = simpleCart.items[data[i].pk]
    var item_name = cart_item.name.replace(/<(?:.|\n)*?>/gm, '');
    msg += "\n\n"+item_name+" "
    if (data[i].remaining > 1) {
      msg += "("+ data[i].remaining+ " slots remaining)"
    } else if (data[i].remaining == 1) {
      msg += "(1 slot remaining)"
    } else {
      msg += "(class full)"
    }
    cart_item.remove();
  }
  alert(msg);
}

$(document).ajaxError(function() {
  alert("An unknown error has occurred. Please try again or email us at classes@txrxlabs.org")
});
