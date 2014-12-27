function loadJSON(url) { window.location = url; } // IE Fallback
function showLogin() {
  $("#login-dialog").toggleClass("login-visible");
}

simpleCart.successURL = window.location.origin+"/classes/?success"
simpleCart.cartHeaders = ["Name", "Price", "Decrement", "Increment","Quantity", "Remove"]

function showCart() {
  $("#cart-modal").modal({width: 400, modal: true, minHight: 300});
}

function addClass(session_id) {
  var session = window.SESSIONS_ON_PAGE[session_id];
  addItem(session.name,session.fee,session_id);
  toggleCourses(session.name);
  $("#cartModal").modal({show:true})
}

function addItem(name,price,id) {
  simpleCart.add('name='+name,'price='+price,'id='+id,'quantity=1');
}

function toggleCourses(name) {
  $(".in-cart").removeClass("in-cart");
  var has_items = false;
  for (id in simpleCart.items) { $("#s"+id).addClass("in-cart"); has_items = true; }
  simpleCart.update();
  if (has_items) { $("#mobileCart,.btn-cart").show(); }
  else { $("#mobileCart,.btn-cart").hide(); }
  $(".recentAdd").removeClass("recentAdd");
  $(".itemContainer").each(function() {
    if ($(this).find(".itemName").text() == name) {
      $(this).addClass("recentAdd");
    }
  })
}

function applyFilters(that) {
  // Controls filters found in widgets/filters.html and course/_filters.html
  var form = $(that);
  var data = form.serializeArray();
  var items = $(".filterable").show();
  if ($("#show_closed").attr("checked")) { $(".course_list .past").show(); }
  else { $(".course_list .past").hide(); }
  for (var i=0; i<data.length;i++) {
    var name = data[i].name;
    var value = data[i].value;
    if (!value) { continue }
    items.filter(function() {
      return $(this).data(name).search(value)<0;
    }).hide();
  }
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
$(function() {
  if (simpleCart && simpleCart.items && window.SESSIONS_ON_PAGE){
    var undiscounted = 0, discounted = 0;
    for (id in simpleCart.items) {
      if (!window.SESSIONS_ON_PAGE[id]) { continue; }
      var cart_price = simpleCart.items[id].price;
      var session_price = window.SESSIONS_ON_PAGE[id].fee;
      if (cart_price < session_price) { undiscounted++; }
      if (cart_price > session_price) { discounted++; }
      simpleCart.items[id].price = session_price;
    }
    simpleCart.update();
    if (discounted) { $("#main").prepend("<div class='alert alert-success'>The price of " + discounted + " classes in your cart have decreased. This is most likely because your membership level has changed (eg: you logged in). Please notify <a href='mailto:classes@txrxlabs.org'>classes@txrxlabs.org</a> if you believe this is in error.</div>"); }
    if (undiscounted) { $("#main").prepend("<div class='alert alert-success'>The price of " + undiscounted + " classes in your cart have increased. This is most likely becaus your membership level has changed (eg: you logged out). Please notify <a href='mailto:classes@txrxlabs.org'>classes@txrxlabs.org</a> if you believe this is in error.</div>"); }
  }
});
