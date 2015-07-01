<product-list>
  <div class="row">
    <product each={ product,i in opts.visible_products } data={ product } class="col-sm-6 col-md-4"></product>
  </div>
  opts.visible_products = window.PRODUCTS.list;
</product-list>

<product>
  <div class="well {incart:opts.data.quantity,out-of-stock:opts.data.in_stock==0}">
    <div class="img">
      <img src={ opts.data.img.url } />
    </div>
    <div class="name">{ opts.data.name }</div>
    <div class="row">
      <div class="col-xs-{ (opts.data.quantity!=0)?12:6 } price">
        ${opts.data.price}
        <span if={ opts.data.quantity }>x { opts.data.quantity }</span>
      </div>
      <div class="col-xs-6" if={ !opts.data.quantity }>
        <button class="btn btn-success btn-block" onclick={ plusOne }>Add to Cart</button>
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
        <div class="col-xs-12 bottom">
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

<product_admin>
  <div class="row">
    <div each={ product,i in visible_products } class="col-sm-6 col-md-4 product">
      <div class="well">
        <div class="img {out-of-stock:product.in_stock==0}">
          <img src={ product.img.url } />
        </div>
        <div class="name">{ product.name }</div>
        <div class="price">
          ${ product.price }
          <span class="pull-right">In Stock: { product.in_stock||"null" }</span>
        </div>
        <div class="row">
          <div class="col-xs-6">
            <a href="/admin/store/consumable/{ product.pk }/" class="fa fa-pencil-square btn btn-primary btn-block">
              Edit</a>
          </div>
          <div class="col-xs-6">
            <a href="{ product.purchase_url }" class="btn btn-info btn-block {hidden:!product.purchase_url}">
              { product.purchase_domain }</a>
          </div>
        </div>
        <div class="row bottom">
          <div class="col-xs-6">
            <button click={ add } class="btn btn-success btn-block">
              +{ product.purchase_quantity }</button>
          </div>
          <div class="col-xs-6">
            <button click={ subtract } class="btn btn-danger btn-block">
              -{ product.purchase_quantity }</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  this.visible_products = window.PRODUCTS.list;
</product_admin>
