uR.drop.ready(function initPromocode() {
  var code_to_check = uR.getQueryParameter("p");
  if (code_to_check) {
    var has_promocode = uR.drop.cart.extra.promocode
    uR.drop.ajax({
      url: "/promocode/redeem_ajax/",
      data: { code: code_to_check},
      success: function(data) {
        uR.drop.cart = data.cart;
        !has_promocode && uR.drop.notifyPromocode();
      },
    });
  }
  uR.drop.notifyPromocode = function() {
    var p = uR.drop.cart.extra.promocode;
    var opts = {
      close_text: "<< Continue Shopping",
    }
    if (uR.drop.cart.all_items && uR.drop.cart.all_items.length) {
      opts.buttons = [{
        onclick: function() { uR.drop.openCart() },
        text: "Checkout",
        className: uR.config.btn_success,
      }];
    }
    p && uR.alert("The following promocode will be applied at checkout:<br/><b>"+p.name+"</b>",opts);
  }
  uR.drop.payment_backends.push({
    tagname: 'promocode-redeem',
    get_copy: function() { return uR.drop.promocode?"Change Promocode":'Enter a Promocode'; },
    className: uR.config.btn_primary,
    icon: 'fa fa-tags',
    name: 'promocode',
    order: 4,
    skip_checkout: true,
  });
  var prefix = uR.drop.prefix+"/promocode";
  var _routes = {};
  _routes[prefix+"/redeem/"] = function(path,data) { uR.alertElement("promocode-redeem",data) }
  uR.addRoutes(_routes);
});

<promocode-redeem>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Enter a Promocode</h3></div>
    <div class={ theme.content }>
      <ur-form action={ url } method="GET" cancel_function={ close } initial={ initial }
               ajax_success={ ajax_success } if={ !success_message }></ur-form>
      <div if={ success_message }>
        <p class={ uR.config.alert_success }>{ success_message }</p>
        <button class={ uR.config.btn_primary } onclick={ close }>{ close_text }</button>
      </div>
    </div>
  </div>
  var self = this;
  this.schema = [{name: "code", label: "Promoode"}];
  this.initial = { code: uR.storage.get("promocode") };
  this.url = uR.drop.prefix+"/promocode/redeem_ajax/";
  var has_cart = uR.drop.cart && uR.drop.cart.all_items && uR.drop.cart.all_items.length;
  this.ajax_success = function(data) {
    uR.drop.cart = data.cart;
    uR.drop.notifyPromocode();
    self.update();
  } 
  close(e) {
    has_cart && uR.drop.openCart();
    this.unmount();
  } 
</promocode-redeem>
