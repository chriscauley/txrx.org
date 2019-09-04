(function() {
  function ajax(options) {
    options.url = uR.drop.prefix + options.url;
    var _success = options.success || function() {};
    options.success = function(data,request) {
      _success(data,request);
      uR.drop.updateTags();
    }
    uR.ajax(options);
  }
  function updateProducts() {
    uR.drop.ajax({
      url: '/products.js',
      success: function(data) {
        uR.drop.products_list = data.products;
        uR.drop.products = {};
        uR.forEach(data.products,function(product) {
          uR.drop.products[product.id] = product;
          product.price = product.sale_price = parseFloat(product.unit_price);
        });
        uR.drop.discounts = data.discounts || [];
        uR.forEach(uR.drop.discounts,function(discount) {
          uR.forEach(discount.product_ids, function(product_id) {
            var product = uR.drop.products[product_id];
            var discount_price = product.price*(1-discount.percentage/100)
            if (product.sale_price > discount_price) {
              product.discount = discount;
              product.sale_price = discount_price;
            }
          });
        });
        uR.drop.ready("Products loaded")
      }
    });
  }
  function updateCart() {
    uR.drop.ajax({
      url: '/cart.js',
      success: function(data) {
        uR.drop.cart = data;
        uR.drop.ready("Cart loaded")
      },
      error: function() {}
    });
  }
  function saveCartItem(product_id, quantity, riot_tag, options) {
    options = options ||{};
    options.id = product_id;
    options.quantity = quantity;
    uR.drop.ajax({
      url: "/ajax/edit/",
      tag: riot_tag,
      data: options,
      success: function(data) {
        uR.drop.cart = data.cart;
        riot_tag && riot_tag.update();
        riot_tag && riot_tag.add_successful && riot_tag.add_successful();
        !options.no_cart && uR.drop.cart.all_items.length && uR.drop.openCart();
        riot.update(uR.drop.store_tags);
      },
      error: function(data) {
        console.log(data);
      },
      method: "POST",
    });
  }
  function openCart(data) {
    if (document.querySelector(uR.drop.cart_tag)) { return; } // cart is already open!
    uR.alertElement(uR.drop.cart_tag,data)
  }
  function updateTags() {
    if (!uR.drop.products_list || !uR.drop.cart) { return }
    uR.drop.checkoutReady = true;
    uR.forEach(uR.drop.cart.all_items,function(item) {
      var product = uR.drop.products[item.product_id];
      uR.drop.requires_shipping = uR.drop.requires_shipping || product.requires_shipping;
    });
    if (uR.drop.requires_shipping && !uR.drop.shipping_address) { uR.drop.checkoutReady = false }

    uR.forEach(uR.drop.products_list,function (p) { p.quantity = 0; })
    uR.forEach(uR.drop.cart.all_items,function (item) {
      if (uR.drop.products[item.product_id]) { uR.drop.products[item.product_id].quantity = item.quantity; }
    });
    if (!uR.drop._mounted) {
      riot.mount(uR.drop.store_tags);
      uR.drop._mounted = true;
    } else {
      riot.update(uR.drop.store_tags);
    }
  }
  function emptyCart() {
    uR.forEach(uR.drop.cart.all_items,function(item) {
      uR.drop.saveCartItem(item.product_id,0)
    })
  }
  uR.drop = {
    saveCartItem: saveCartItem,
    updateProducts: updateProducts,
    updateCart: updateCart,
    updateTags: uR.debounce(updateTags,100),
    emptyCart: emptyCart,
    store_tags: "cart-button,add-to-cart",
    openCart: openCart,
    modal_cart: true,
    ajax: ajax,
    cart_tag: 'shopping-cart',
    prefix: "",
    ready: new uR.Ready(function dropReady() { return uR.drop.products && uR.drop.cart }),
    login_required: true,
    payment_backends: [],
    $: function(amount) {
      var start = "$";
      if (amount < 0) {
        start = "- "+start;
        amount = Math.abs(amount);
      }
      amount = (amount == Math.floor(amount))?Math.floor(amount):parseFloat(amount).toFixed(2);
      return start+Math.abs(amount);
    },
    addRoutes: function addRoutes(_routes) {
      var out = {}
      for (var key in _routes) { out[uR.drop.prefix+key] = _routes[key] }
      uR.addRoutes(out);
    },
  };
  uR.schema.fields.no_email = {
    name: 'email', type: 'email', label: 'Email Address',
    help_text: "Since you are not logged in, we'll look up or create an account using this email address. We promise to only use this for comminication about your purchase."
  }
  uR.theme.checkout_button = uR.config.btn_primary;
  uR.ready(uR.drop.updateProducts,uR.drop.updateCart)
})();
