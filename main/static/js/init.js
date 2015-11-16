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
});

function createCookie(name,value,days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
  }
  else var expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

function eraseCookie(name) { createCookie(name,"",-1); }

function openCart() {
  $("body").append("<cart></cart>");
  riot.mount("cart");
}

function updateCartButton() {
  var total = 0,quantity=0;
  PRODUCTS.list.forEach(function(l) {
    total += l.price*l.quantity;
    quantity += l.quantity;
  });
  var button = $(".store-button").hide();
  button.find(".quantity").html(quantity);
  button.find(".total").html("$"+total.toFixed(2));
  if (total) { button.show(); }
}

function cheatCode(f,qs) {
  var HACKERKEYS = [];
  var code = [38,38,40,40,37,39,37,39,66,65];
  $(document).keyup(function(e) {
    HACKERKEYS.push(e.keyCode);
    var entries = HACKERKEYS.slice(-code.length);
    for (var i = 0; i < code.length; ++i) { if (code[i] !== entries[i]) return false; }
    f();
  });
  if (window.location.search.indexOf(qs) == -1) { return }
  console.log(window.location.search)
  console.log(window.location.search.indexOf(qs))
  f();
}

function timeit(f) {
  return function() {
    var start = new Date().valueOf();
    var out = f.apply(this,arguments);
    var t = new Date().valueOf()-start;
    console.log(t)
    return out
  }
}

// how to disable/enable timeit
function timeit(f) { return f }

// this is just so that I can easily timeit
var resetProductList = timeit(function() {
  riot.update('product-list');
});
