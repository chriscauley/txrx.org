<product-list>
  <div class="row">
    <product each={ product,i in opts.visible_products } data={ product } class="col-sm-6 col-md-4"></product>
  </div>
  opts.visible_products = window.PRODUCTS.list;
</product-list>

<product>
  <div class="well {incart:opts.data.quantity}">
    <div class="img">
      <img src={ opts.data.img.url } />
    </div>
    <div class="name">{{ opts.data.name }}</div>
    <div class="row">
      <div class="col-xs-6 price">
        ${opts.data.price}
        <span if={ opts.data.quantity }>x { opts.data.quantity }</span>
      </div>
      <div class="col-xs-6">
        <button class="btn btn-success btn-block" onclick={ plusOne } if={ !opts.data.quantity }>Add to Cart</button>
      </div>
    </div>
    <div class="row cart-buttons">
      <div if={ has_buttons }>
        <div class="col-xs-6">
          <button class="btn btn-success btn-block" onclick={ plusOne }>+1</button>
        </div>
        <div class="col-xs-6">
          <button class="btn btn-danger btn-block" onclick={ minusOne }>-1</button>
        </div>
        <div class="col-xs-12">
          <button class="btn btn-primary btn-block" onclick={ openCart }>Checkout</button>
        </div>
      </div>
    </div>
  </div>
  var update_timeout;
  this.has_buttons = false;
  this.on("update",function() {
    if (this.opts.data.quantity) { this.has_buttons = true }
    updateCartButton();
  });
  function updateCart() {
    clearTimeout(update_timeout);
    update_timeout = setTimeout(_updateCart,250);
  }
  function _updateCart() {
    $.post(
      '/shop/edit/',
      {pk: opts.data.pk,quantity: opts.data.quantity}
    );
  }
  plusOne(e) {
    opts.data.quantity++;
    updateCart();
  }
  minusOne(e) {
    opts.data.quantity--;
    updateCart();
  }
  openCart(e) {
    $("body").append("<cart>");
    riot.mount("cart")
  }
</product>
