uR.ready(function() {
  uR.schema.fields.amount = { type: 'number', extra_attrs: { step: 1 }, label: "Amount (USD)" };
  var code_to_check = uR.getQueryParameter("giftcode") || (uR.storage.get("giftcard") || {}).code;
  if (code_to_check) {
    var has_giftcard = uR.storage.get("giftcard");
    uR.drop.ajax({
      url: "/giftcard/validate/",
      data: { code: code_to_check},
      success: function(data) {
        if (!data.giftcard || !parseFloat(data.giftcard.remaining)) {
          uR.storage.set("giftcard",null);
          uR.storage.set("giftcode",null);
        } else {
          uR.storage.set("giftcard",data.giftcard);
          if (!has_giftcard) {
            uR.alert("You have activated a gift card worth $"+data.giftcard.remaining+". You can apply this towards the purchase of any item on the site at checkout.");
          }
        }
      },
      error: function(data) {
        uR.storage.set("giftcard",null);
        uR.storage.set("giftcode",null);
      }
    });
  }
  uR.drop._addToCart['giftcard.giftcardproduct'] = function(data) { uR.alertElement('purchase-giftcard',data); }
  uR.drop.payment_backends.push({
    tagname: 'giftcard-checkout',
    copy: 'Pay With A Gift Card',
    className: uR.config.btn_primary,
    icon: 'fa fa-gift', order: 3,
    name: 'giftcard',
  });
  var prefix = uR.drop.prefix+"/giftcard";
  var _routes = {};
  _routes[prefix+"/redeem/"] = function(path,data) { uR.alertElement("giftcard-redeem",data) }
  uR.addRoutes(_routes);
});

<purchase-giftcard>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Purchase a gift card</h3></div>
    <div class={ theme.content }>
      <ur-form schema={ product.extra_fields } success_text="Add to Cart" initial={ initial }></ur-form>
    </div>
  </div>

  var self = this;
  this.product = this.opts.product;
  this.initial = { };
  if (uR.drop.product_on_page) { this.initial.amount = parseInt(uR.drop.product_on_page.unit_price); }
  if (this.opts.initial) { this.initial = this.opts.initial; }
  this.submit = function(ur_form) {
    var data = ur_form.getData();
    uR.drop.saveCartItem(self.product.id,data.amount,self,data);
  }
  this.add_successful = function() {
    self.unmount();
    uR.drop.openCart();
  }
</purchase-giftcard>

<giftcard-redeem>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Redeem a Gift Card</h3></div>
    <div class={ theme.content }>
      <ur-form action={ post_url } method="POST" cancel_function={ close } initial={ initial }
               ajax_success={ ajax_success } if={ !success_message }></ur-form>
      <div if={ success_message }>
        <p class={ uR.config.alert_success }>{ success_message }</p>
        <button class={ uR.config.btn_primary } onclick={ close }>{ close_text }</button>
      </div>
    </div>
  </div>

  var self = this;
  this.schema = [{name: "code", label: "Redemption Code"}];
  this.initial = {code: uR.storage.get("giftcode") };
  this.post_url = uR.drop.prefix+"/giftcard/redeem_ajax/";
  var has_cart = uR.drop.cart && uR.drop.cart.all_items && uR.drop.cart.all_items.length;
  this.close_text = has_cart?"Back to Cart":"Close";
  this.ajax_success = function(data) {
    uR.storage.set("giftcard",data.giftcard);
    if (self.opts.in_checkout) {
      uR.alertElement("giftcard-checkout");
    } else {
      self.success_message = "You giftcard is worth $" + data.giftcard.remaining + ". You can apply this value to your purchase at checkout.";
      self.update();
    }
  }
  close(e) {
    has_cart && uR.drop.openCart();
    this.unmount();
  }
</giftcard-redeem>

<giftcard-checkout>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Pay with Gift Card</h3></div>
    <div class={ theme.content }>
      <ul>
        <li><b>Gift Card Balance:</b> ${ giftcard.remaining }</li>
        <li><b>Cart Total:</b> ${ uR.drop.cart.total_price }</li>
      </ul>
      <ur-form action={ post_url } method="POST" initial={ initial } success_text="Use Gift Card Balance"
               cancel_text="Back to Cart" cancel_function={ uR.drop.openCart }></ur-form>
    </div>
  </div>

  if (!uR.auth.user) { this.schema.push(uR.schema.fields.no_email) }
  if (!uR.storage.get("giftcard")) {
    uR.alertElement("giftcard-redeem",{in_checkout: true});
  } else {
    this.giftcard = uR.storage.get("giftcard");
    this.post_url = uR.drop.prefix+"/giftcard/payment/";
    this.initial = {
      total: Math.min(this.giftcard.remaining,parseFloat(uR.drop.cart.total_price)),
      code: this.giftcard.code,
      email: this.giftcard.extra.recipient_email,
    };
  }
  this.schema = [
    {name: "total", label: "Amount to apply", max: this.giftcard && this.giftcard.remaining },
    {name: "code", type: "hidden"},
  ];
  ajax_success(data) {
    if (data.next) {
      window.location = data.next;
    } else {
      uR.drop.cart = data;
      uR.drop.openCart();
    }
  }
</giftcard-checkout>
