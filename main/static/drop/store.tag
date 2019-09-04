uR.ready(function() {
  uR.addRoutes({
    "/categories/": uR.router.routeElement("category-list"),
    "/products/": uR.router.routeElement("product-list"),
  });
});

<category-list>
  <button class="btn btn-default btn-block {active:!uR.drop.active_category}" onclick={ reset }>
    Any Category</button>
  <button class="btn btn-default btn-block {active:uR.drop.active_category==category.pk}"
          onclick={ parent.click } each={ category,i in categories }>
    { category.name }</button>

  this.categories = window.PRODUCTS.categories;
  this.active_category = undefined;
  click(e) {
    uR.drop.active_category = e.item.category.pk;
    window.PRODUCTS.visible = 18;
    resetProductList();
  }
  reset(e) {
    uR.drop.active_category = undefined;
    window.PRODUCTS.visible = 18;
    resetProductList();
  }
</category-list>

<product-list>
  <div class="row">
    <product each={ product,i in products } product={ product } class="col-sm-6 col-md-4"></product>
    <product-admin each={ product,i in admin_products } product={ product } class="col-sm-6 col-md-4"></product-admin>
  </div>
  <button class="btn btn-warning btn-block" onclick={ more } if={window.PRODUCTS.visible<this.max_products}>
    Load More</button>

  var self = this;
  window.PRODUCTS.visible = 18;
  this.on("mount",function() {
    this.ajax({
      url: '/drop/products.js',
      success: function(data) {
        self.all_products = data.products
      },
    });
    window.PRODUCT_LIST = this;
  });
  this.on("update",function() {
    this.products = window.PRODUCTS.list;
    if (uR.drop.active_category) {
      this.products = this.products.filter(function(p){
        return p.categories.indexOf(uR.drop.active_category) > -1;
      });
    }
    this.max_products = this.products.length
    this.products = this.products.slice(0,window.PRODUCTS.visible);
    if (window.PRODUCTS.extra) {
      this.admin_products = this.products;
      this.products = [];
    }
  });
  more(e) {
    window.PRODUCTS.visible += 12;
    resetProductList();
  }
</product-list>

<product>
  <div class="well {incart:product.quantity,out-of-stock:product.in_stock==0,hidden:data.categories.indexOf(uR.drop.active_category)==-1}">
    <div class="img">
      <img src={ product.img.url } />
    </div>
    <div class="name">{ product.name }</div>
    <div class="row">
      <div class="col-xs-{ (product.quantity!=0)?12:6 } price">
        ${product.price}
        <span if={ product.quantity }>x { product.quantity }</span>
      </div>
      <div class="col-xs-6" if={ !product.quantity }>
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
  var that = this;
  that.product = opts.product;
  this.has_buttons = false;
  this.on("update",function() {
    if (that.product.quantity) { this.has_buttons = true }
    updateCartButton();
  });
  function updateCart() {
    clearTimeout(update_timeout);
    update_timeout = setTimeout(_updateCart,250);
  }
  function _updateCart() {
    $.post(
      '/shop/edit/',
      {pk: that.product.pk,quantity: that.product.quantity}
    );
  }
  plusOne(e) {
    that.product.quantity++;
    updateCart();
  }
  minusOne(e) {
    that.product.quantity--;
    updateCart();
  }
  openCart(e) {
    $("body").append("<cart>");
    riot.mount("cart")
  }
</product>

<product-admin>
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
          <i class="fa fa-shopping-cart"></i> { product.purchase_domain }</a>
      </div>
    </div>
    <div class="row bottom">
      <div class="col-xs-6">
        <button onclick={ add } class="btn btn-success btn-block">
          +{ product.purchase_quantity }</button>
      </div>
      <div class="col-xs-6">
        <button onclick={ subtract } class="btn btn-danger btn-block">
          -{ product.purchase_quantity }</button>
      </div>
    </div>
  </div>

  var that = this;
  that.product = this.opts.product;
  function modify(sign) {
    $.post(
      '/shop/admin/add/',
      {quantity:that.product.purchase_quantity*sign,pk:that.product.pk},
      function(data) {
        that.product.in_stock = data;
        that.update();
      }
    )
  }
  add(e) {
    modify(1);
  }
  subtract(e) {
    modify(-1);
  }
</product-admin>
