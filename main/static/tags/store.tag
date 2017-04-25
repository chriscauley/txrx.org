<category-list>
  <button class="btn btn-default btn-block {active:!uR.drop.active_category}" onclick={ click }>
    Any Category</button>
  <button class="btn btn-default btn-block {active:uR.drop.active_category==category.id}"
          onclick={ parent.click } each={ category,i in uR.drop.categories }>
    { category.name }</button>

  this.on("mount",function() {
    this.ajax({
      url: "/shop/categories.js",
      success: function(data) {
        uR.drop.categories = data.categories;
        uR.drop.active_category = undefined;
      },
    });
  });

  click(e) {
    uR.drop.active_category = e.item && e.item.category && e.item.category.id; 
    uR.drop.visible = 18;
    uR.drop.updateTags();
  }
</category-list>

<product-list>
  <div class="row">
    <product each={ products } class={ parent.className }></product>
    <product-admin each={ admin_products } class="col-sm-6 col-md-4"></product-admin>
  </div>
  <button class="btn btn-warning btn-block" onclick={ more } if={uR.drop.visible<this.max_products}>
    Load More</button>

  var self = this;
  this.on("mount",function() {
    this.className = this.opts.className || "col-sm-6 col-md-4";
    uR.drop.visible = 18;
    this.update();
    if (window.PRODUCTS_EXTRA) {
      uR.forEach(uR.drop.products_list,function(p) {
        var extra  = window.PRODUCTS_EXTRA[p.id] || {};
        for (var key in extra) {
          p[key] = extra[key]
        }
      });
    }
  });
  this.on("update",function() {
    if (!uR.drop.products) { return }
    if (this.opts.ids) {
      this.products = [];
      uR.forEach(this.opts.ids,function(id) { self.products.push(uR.drop.products[id]); });
    } else {
      this.products = uR.drop.products_list;
    }
    if (this.opts.model_slugs) {
      var model_slugs = this.opts.model_slugs.split(",");
      this.products = this.products.filter( function(p) { return model_slugs.indexOf(p.model_slug) != -1; })
    }
    if (uR.drop.active_category) {
      this.products = this.products.filter(function(p){
        return p.category_ids && p.category_ids.indexOf(uR.drop.active_category) != -1;
      });
    }
    this.max_products = this.products.length;
    this.products = this.products.slice(0,uR.drop.visible);
    if (window.PRODUCTS_EXTRA) {
      this.admin_products = this.products;
      this.products = [];
    }
  });
  more(e) {
    uR.drop.visible += 12;
  }
</product-list>

<product>
  <div class="well { out-of-stock:in_stock==0 }">
    <div class="img" style="background-image: url({ thumbnail })"></div>
    <div class="bottom">
      <div class="name">
        <a href="/admin/{ model_slug.replace('.','/') }/{ id }/" if={ uR.auth.user.is_superuser }
           class="superuseronly fa fa-pencil-square"></a>
        { display_name }
      </div>
      <div class="row">
        <div class="col-xs-6 price">
          ${unit_price}
          <span if={ quantity }>x { quantity }</span>
        </div>
        <div class="col-xs-6">
          <button class="btn btn-success btn-block" onclick={ addToCart } if={ !quantity }>Add to Cart</button>
          <button class="btn btn-primary btn-block" onclick={ uR.drop.openCart } if={ quantity }>Checkout</button>
        </div>
      </div>
    </div>
  </div>

  var update_timeout;
  addToCart(e) {
    var widget = uR.drop._addToCart[this.id]
    if (widget) { widget({product: uR.drop.products[this.id]}) }
    else { uR.drop.saveCartItem(this.id, 1, self); }
  }
</product>

<product-admin>
  <div class="well">
    <div class="img {out-of-stock:in_stock==0}">
      <img src={ img.url } />
    </div>
    <div class="name">{ display_name }</div>
    <div class="price">
      ${ price }
      <span class="pull-right">In Stock: { in_stock||"null" }</span>
    </div>
    <div class="row">
      <div class="col-xs-6">
        <a href="/admin/store/consumable/{ pk }/" class="fa fa-pencil-square btn btn-primary btn-block">
          Edit</a>
      </div>
      <div class="col-xs-6">
        <a href="{ purchase_url }" class="btn btn-info btn-block {hidden:!purchase_url}">
          <i class="fa fa-shopping-cart"></i> { purchase_domain }</a>
      </div>
    </div>
    <div class="flexy">
      <button onclick={ add1 } class="btn btn-success" if={ purchase_quantity != 1 }>
        +1</button>
      <button onclick={ subtract1 } class="btn btn-danger" if={ purchase_quantity != 1 }>
        -1</button>
      <button onclick={ add } class="btn btn-success">
        +{ purchase_quantity }</button>
      <button onclick={ subtract } class="btn btn-danger">
        -{ purchase_quantity }</button>
    </div>
  </div>

  var self = this;
  function modify(quantity) {
    $.post(
      '/shop/admin/add/',
      {quantity:quantity,pk:self.pk},
      function(data) {
        self.in_stock = data;
        self.update();
      }
    )
  }
  add1(e) {
    modify(1);
  }
  subtract1(e) {
    modify(-1);
  }
  add(e) {
    modify(e.item.purchase_quantity);
  }
  subtract(e) {
    modify(-e.item.purcase_quantity);
  }
</product-admin>
