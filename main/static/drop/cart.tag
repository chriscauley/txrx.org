(function() {
  uR.drop._addToCart = {}
})();

<add-to-cart>
  <div if={ !opts.hide_price }>
    <div class="pre-sale" if={ product.sale_price != product.price }>${ product.price.toFixed(2) }</div>
    <div class="price">${ product.sale_price.toFixed(2) }</div>
  </div>
  <button class={ btn_class } onclick={ addToCart } if={ !in_cart }>{ add_text }</button>
  <button class={ btn_class } onclick={ uR.drop.openCart } if={ in_cart }>{ show_text }</button>

  var self = this;
  this.ajax_target = this.root;
  this.on("mount",function() {
    this.add_text = this.opts.add_text || "Add to Cart";
    this.show_text = this.opts.show_text || "View in Cart";
    this.product = uR.drop.products[this.opts.product_id];
    if (!this.product) { return this.unmount() }
    this.btn_class = this.opts.btn_class || uR.config.btn_primary;
    if (this.opts.root_class) { this.root.classList.add(this.opts.root_class); }
    this.update();
  });
  this.on("update",function() {
    this.in_cart = false;
    if (!(uR.drop.cart && uR.drop.cart.all_items)) { return; }
    uR.forEach(uR.drop.cart.all_items,function(item) {
      if (self.opts.product_id == item.product_id) { self.in_cart = true }
    })
  });
  addToCart() {
    var widget = uR.drop._addToCart[this.product.model_slug] || uR.drop._addToCart[this.product.id];
    if (widget) { widget({product: this.product}); }
    else { uR.drop.saveCartItem(this.opts.product_id,this.opts.quantity || 1,this) }
  }
</add-to-cart>

<cart-button>
  <button class={ uR.config.btn_primary } onclick={ uR.drop.openCart }>
    <i class="fa fa-shopping-cart"></i>
    { uR.drop.cart.all_items.length } items ${ total_price.toFixed(2) }
  </button>

  this.on("update",function() {
    this.total_price = parseFloat(uR.drop && uR.drop.cart && uR.drop.cart.total_price);
    if (!this.total_price) { this.root.style.display = "none"; }
    else { this.root.style.display = "block"; }
  })
</cart-button>

<cart-quantity>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>{ product.display_name }</h3></div>
    <div class={ theme.content }>
      <ur-form submit={ updateAndClose } initial={ initial } cancel_function={ cancelFunction }><ur-form>
    </div>
  </div>

  this.on("mount",function() {
    this.product = this.opts.product;
    this.initial = opts.initial || {};
    this.initial.quantity = this.initial.quantity || 1;
    this.update()
  });

  cancelFunction() {
    if (this.opts.product.quantity) { uR.drop.saveCartItem(this.product.id,0,this); }
    else { this.unmount() }
  }

  updateAndClose(e) {
    uR.drop.saveCartItem(this.product.id,this.root.querySelector("input").value,this);
  }
</cart-quantity>

<shopping-cart>
  <div class={ theme.outer } name="ajax_target">
    <div class={ theme.header }>
      <h3>Shopping Cart</h3>
    </div>
    <div class={ theme.content }>
      <div if={ !uR.drop.cart.all_items.length }>
        Your cart is empty. Please close me. Thank you.
      </div>
      <div if={ uR.drop.cart.all_items.length }>
        <div class={ uR.theme.cart_items }>
          <div class="item { uR.theme.cart_item }" each={ uR.drop.cart.all_items }>
            <div class="left">
              <div class="name"><b>{ display_name }</b> { after }</div>
              <div if={ extra.display }>{ extra.display }</div>
              <a class="remove" onclick={ parent.remove }>Remove</a>
            </div>
            <div class="price-box has_quantity" if={ has_quantity && !widget }>
              <span class="quantity">{ quantity }</span>
              <i class="fa fa-times"></i>
              <span class="unit-price"> { uR.drop.$(unit_price) }</span>
              <div class="change">
                <a class="fa fa-plus-circle increment" onclick={ parent.plusOne }></a>
                <a class="fa fa-minus-circle decrement" onclick={ parent.minusOne }></a>
              </div>
            </div>
            <div if={ !has_quantity || widget } class="price-box">
              <span class="unit-price">{ uR.drop.$(line_subtotal) }</span>
              <a onclick={ parent.editCartItem } if={ widget && !extra.no_edit } class="edit">
                <i class="fa fa-edit"></i> edit</a>
            </div>
            <div class="extra_price_field" each={ field in extra_price_fields }>
              <div class="description">{ field[0] }</div>
              <div class="amount">{ uR.drop.$(field[1]) }</div>
            </div>
          </div>
          <div class="extra_price_field item" each={ field in uR.drop.cart.extra_price_fields }>
            <div class="description"><b>{ field[0] }</b></div>
            <div class="amount">{ uR.drop.$(field[1]) }</div>
          </div>
        </div>
        <div class="totals-box">
          <div class="subtotals"></div>
          Order Total: <b>{ uR.drop.$(uR.drop.cart.total_price) }</b>
        </div>
        <div class={ uR.theme.error_class } style="margin:10px 0 0" each={ n,i in errors }>{ n }</div>
      </div>
    </div>
    <div class="{ theme.footer } valign-wrapper" if={ !uR.drop.cart.all_items.length }>
      <button class={ uR.config.btn_cancel } onclick={ close }>Close</button>
    </div>
    <div class="{ theme.footer } valign-wrapper" if={ uR.drop.cart.all_items.length }>
      <div class="shipping_choice" if={ requires_shipping }>
        <div if={ !shipping_address }>
          <button class={ uR.config.btn_primary } onclick={ selectShipping }>Checkout</button>
        </div>
        <div if={ shipping_address }>
          <div>
            <h5>Ship to:</h5>
            { shipping_address.name }<br/>
            { shipping_address.address }<br/>
            { shipping_address.city }
          </div>
          <div>
            <button class={ uR.config.btn_primary } onclick={ selectShipping }>Change Shipping Address</button>
          </div>
        </div>
      </div>
      <payment-buttons></payment-buttons>
      <a onclick={ close }>&laquo; Keep Shopping</a>
    </div>
  </div>

  var self = this;
  uR.drop.payment_backends.sort(function(a,b) { return (a.order||0) > (b.order||0); });

  close(e) {
    this.unmount();
  }
  saveCart(e) {
    uR.drop.saveCartItem(e.item.product_id,e.item.quantity,this);
  }
  plusOne(e) {
    e.item.quantity++;
    this.saveCart(e);
  }
  minusOne(e) {
    e.item.quantity--;
    this.saveCart(e);
  }
  remove(e) {
    e.item.quantity=0;
    this.saveCart(e);
  }
  selectShipping(e) {
    uR.alertElement('select-address',{success: uR.drop.openCart});
  }
  if (uR.drop.login_required) {
    this.checkout = uR.auth.loginRequired(this.checkout)
    this.selectShipping = uR.auth.loginRequired(this.selectShipping);
  }
  editCartItem(e) {
    e.item.widget({product:uR.drop.products[e.item.product_id],initial:e.item.extra});
  }
  this.on("update",function() {
    uR.forEach(uR.drop.cart.all_items,function(item) {
      var product = uR.drop.products[item.product_id];
      item.display_name = product.display_name;
      item.unit_price = product.unit_price;
      item.has_quantity = product.has_quantity;
      item.widget = uR.drop._addToCart[product.model_slug] || uR.drop._addToCart[item.product_id];
      item.model_slug = product.model_slug;
    }.bind(this));
    uR.drop.shipping_address = this.opts.selected_address;
    riot.update("cart-button");
  });
</shopping-cart>

<payment-buttons>
  <div class="payment_buttons" if={ uR.drop.checkoutReady }>
    <b if={ backends.length != 1 }>Select Payment Method</b>
    <b if={ backends.length == 1 }>Checkout</b>
    <button each={ backends } onclick={ parent.checkout } class={ className } alt={ copy }>
      <i class={ icon }></i> { copy }</button>
  </div>

  this.on("mount", function() {
    this.backends = [];
  uR.forEach(uR.drop.payment_backends, function(backend) {
      if (uR.drop.allowed_backends && uR.drop.allowed_backends.indexOf(backend.name) == -1) { return }
      if (backend.test && !backend.test()) { return; }
      if (backend.get_copy) { backend.copy = backend.get_copy(); }
      this.backends.push(backend);
      backend.className += " button_" + backend.name;
    }.bind(this));
    this.update();
  });
  checkout(e) {
    this.errors = undefined;
    function success(data) { uR.alertElement(e.item.tagname,data); };
    if (e.item.skip_checkout) { return success(); } // currently only used for promocode
    uR.drop.ajax({
      url: "/ajax/start_checkout/",
      success: success,
      error: function(data) { this.errors = data.errors || ["An unknown error has occurred"] },
      self: this,
    });
  }
</payment-buttons>
