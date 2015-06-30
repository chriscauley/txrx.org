<cart>
  <div class="mask" onclick={ close }></div>
  <div class="content">
    <div class="header">
      <button class="close" onclick={ close }>&times;</button>
      <h4 class="modal-title">Shopping Cart</h4>
    </div>
    <div class="body">
      <div class="well">
        <div if={ !CART }>Your cart is empty</div>
        <div class="items">
          <div class="item" each={ cart_items }>
            <div class="name"><b>{ name }</b> { after }</div>
            <div class="quantity">{ quantity }</div>
            <i class="fa fa-plus-circle increment" onclick={ parent.plusOne }></i>
            <i class="fa fa-minus-circle decrement" onclick={ parent.minusOne }></i>
            <div class="total">${ (quantity*price).toFixed(2) }</div>
            <i class="fa fa-times remove" onclick={ parent.remove }></i>
          </div>
        </div>
      </div>
      <div class="checkout-box">
        <div class="subtotals"></div>
        Order Total: <b>${ total.toFixed(2) }</b>
      </div>
      <div if={ !window._USER_NUMBER }>
        <center>
          <label>Alternate Contact Email:</label>
          <input type="email" id="custom_email" />
        </center>
        <div class="help-block">
          When you sign up for a class your PayPal email address will be used to send you a confirmation
          and reminder the day before your class. If you want to use a different email, enter it above.
        </div>
      </div>
      <center><button class="btn btn-danger return_policy" onclick="$('.return_policy').toggle();return false;">
          View our return policy</button></center>
      <div class="alert alert-danger return_policy" style="display:none;">
        If you cannot make a class please <a href="https://txrxlabs.org/contact/?slug=cancel_class">request a cancellation</a>.
        Cancellations and rescheduling requests must be made at least one week prior to the class for a full refund.
        Cancellations submitted less than one week before the class will only be refunded if we can fill your slot.
      </div>
      <div class="alert alert-danger" style="margin:10px 0 0" each={ n,i in errors }>{ n }</div>
    </div>
    <div class="modal-footer">
      <button type="button" class="pull-left btn btn-default" data-dismiss="modal" onclick="toggleCourses();">
        &laquo; Keep Shopping</button>
      <form action="https://www.paypal.com/cgi-bin/webscr" method="post">
        <input name="business" type="hidden" value="{ SHOP.email }">
        <span each={ n,i in cart_items }>
          <input name="item_name_{ i+1 }" type="hidden" value="{ n.name }">
          <input name="item_number_{ i+1 }" type="hidden" value="{ n.pk }">
          <input name="quantity_{ i+1 }" type="hidden" value="{ n.quantity }">
          <input name="amount_{ i+1 }" type="hidden" value="{ n.price }">
        </span>
        <input name="notify_url" type="hidden" value="{ SHOP.base_url}/tx/rx/ipn/handler/">
        <input name="cancel_return" type="hidden" value="{ SHOP.base_url }/shop/checkout/pay/">
        <input name="return" type="hidden" value="{ SHOP.base_url }/shop/pay/paypal/success/">
        <input name="invoice" type="hidden" value="3">
        <input name="cmd" type="hidden" value="_cart">
        <input type="hidden" name="upload" value="1">
        <input type="hidden" name="tax_cart" value="0">
        <input name="charset" type="hidden" value="utf-8">
        <input name="currency_code" type="hidden" value="USD">
        <input name="no_shipping" type="hidden" value="1">
        <input type="image" src="/static/img/paypal.png" border="0" onclick={ startCheckout } alt="Buy it Now">
      </form>
    </div>
  </div>

  this.SHOP = window.SHOP;
  var that = this;
  document.body.style.overflowY = document.documentElement.style.overflowY = "hidden";
  document.body.style.paddingRight = "17px";
  document.body.scrolling = "no";
  this.on("update",function() {
    this.cart_items = PRODUCTS.list.filter(function(l){return l.quantity});
    this.total = 0;
    for (var i=0;i<this.cart_items.length;i++) {
      var c = this.cart_items[i];
      this.total += c.quantity*c.price;
    }
    updateCartButton();
  });

  close(e) {
    this.unmount();
    riot.update("*");
    document.body.style.overflowY = document.documentElement.style.overflowY = "";
    document.body.scrolling = "yes";
    document.body.style.paddingRight = "";
  }
  function updateCart(e) {
    $.post(
      '/shop/edit/',
      {pk: e.item.pk,quantity:e.item.quantity}
    );
  }
  plusOne(e) {
    e.item.quantity++;
    updateCart(e);
  }
  minusOne(e) {
    e.item.quantity--;
    updateCart(e);
  }
  remove(e) {
    e.item.quantity = 0;
    updateCart(e);
  }
  startCheckout(e) {
    var form = $(e.target).closest('form');
    $.get(
      '/shop/start_checkout/',
      function(data) {
        if (data.errors.length) {
          that.errors = data.errors;
          that.update();
        } else {
          form.find("[name=invoice]").val(data.order_pk);
          form.submit();
        }
      },
      "json"
    )
  }
</cart>
