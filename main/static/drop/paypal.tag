uR.ready(function() {
  var o = {
    tagname: 'paypal-checkout',
    copy: " Paypal",
    className: uR.config.btn_primary,
    icon: "fa fa-cc-paypal",
    name: 'paypal',
  };
  uR.drop.payment_backends.push(o);
  uR.drop.base_url = uR.drop.base_url || window.location.origin;
});

<paypal-checkout>
  <div class="target { theme.outer }">
    <form action="https://www.paypal.com/cgi-bin/webscr" method="POST">
      <input name="business" type="hidden" value="{ uR.drop.paypal_email }">
      <span each={ n,i in uR.drop.cart.all_items }>
        <input name="item_name_{ i+1 }" type="hidden" value="{ n.display_name }">
        <input name="item_number_{ i+1 }" type="hidden" value="{ n.product_id }">
        <input name="quantity_{ i+1 }" type="hidden" value="{ n.quantity }">
        <input name="amount_{ i+1 }" type="hidden" value="{ n.line_unit_price }">
      </span>
      <input name="notify_url" type="hidden" value="{ uR.drop.base_url }/tx/rx/ipn/handler/">
      <input name="cancel_return" type="hidden" value="{ uR.drop.base_url }/shop/">
      <input name="return" type="hidden" value="{ uR.drop.base_url }/shop/">
      <input name="invoice" type="hidden" value={ opts.order_id }>
      <input name="cmd" type="hidden" value="_cart">
      <input type="hidden" name="upload" value="1">
      <input type="hidden" name="tax_cart" value="0">
      <input name="charset" type="hidden" value="utf-8">
      <input name="currency_code" type="hidden" value="USD">
      <input name="no_shipping" type="hidden" value="1">
    </form>
    <div class={ theme.content }>
      Redirecting to PayPal to complete transaction.
    </div>
  </div>

  this.on("mount",function() {
    this.update();
    this.root.querySelector(".target").setAttribute("data-loading",uR.config.loading_attribute);
    this.root.querySelector("form").submit();
  });
</paypal-checkout>
