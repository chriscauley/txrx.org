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
  f();
}

function timeit(f) {
  return function() {
    var start = new Date().valueOf();
    var out = f.apply(this,arguments);
    var t = new Date().valueOf()-start;
    return out
  }
}

// how to disable/enable timeit
//function timeit(f) { return f }

// this is just so that I can easily timeit
var resetProductList = timeit(function() {
  window.PRODUCT_LIST.update()
});

TXRX.schema = {
  new_rfid: [
    { name: 'username', label: 'Username or Email'},
    { name: 'password', type: 'password' },
    { name: 'new_rfid', type: 'hidden' },
  ]
}
uR.addRoutes({
  "^/gift/$": function(path,data) { uR.alertElement("giftcard-redeem",data) },
  "^/work/$": function(path,data) {
    uR.ajax({
      url: "/durf/redtape/document/"+5+"/",
      success: function(data) {
        uR.mountElement("ur-document",data);
      },
    });
  },
});

// #! TODO btn classes should be moved into theme
uR.config.btn_primary = "btn blue text-white btn-primary";
uR.config.btn_success = "btn green text-white btn-success";
uR.config.btn_cancel = "btn red text-white btn-danger";
//uR.drop.cart_tag = "cart";
uR.drop.store_tags = "category-list,product-list,cart-button,add-to-cart";
uR.drop.login_required = false;
uR.config.mount_to = "#main";
uR.config.support_email = "info@txrxlabs.org";
uR.config.do404 = function() {}
uR.config.form.field_class = "form-group"; // bootstrap
uR.drop.paypal_email = "txrxlabs@gmail.com";
uR.drop.prefix = "/shop";
uR.drop.stripe = true;
uR.drop.paypal = true;
uR.config.tmp_file_url = "/redtape/file/";

uR.theme = {
  input: "form-control",
  cart_items: "well cart-items",
  message_list: "card",
  success_class: "alert alert-success card-content green white-text",
  error_class: "alert alert-danger card-content red white-text",
  modal: {
    outer: "modal-content",
    header: "modal-header",
    content: "modal-body",
    footer: "modal-footer",
  },
}
uR.config.text_validators['signature'] = function(value,tag) {
  if (!value.startsWith("/s/")) { tag.data_error = "Signature must start with /s/"; }
}
