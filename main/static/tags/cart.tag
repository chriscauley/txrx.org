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
            <button class="btn remove" onclick={ parent.remove }>Remove</div>
        </div>
      </div>
      <div class="checkout-box">
        <div class="subtotals"></div>
        Order Total: <b>{ total }</b>
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
    </div>
    <div class="modal-footer">
      <button type="button" class="pull-left btn btn-default" data-dismiss="modal" onclick="toggleCourses();">
        &laquo; Keep Shopping</button>
      <a>
        <img src="{{ STATIC_URL }}img/paypal.png"></a>
    </div>
  </div>

  this.cart_items = PRODUCTS.list.filter(function(l){return l.quantity});
  this.on("update",function() {
    this.total = 0;
    for (var i=0;i<this.cart_items.length;i++) {
      var c = this.cart_items[i];
      console.log(c);
      this.total += c.quantity*c.price;
    }
  });

  close(e) {
    this.unmount();
  }

</cart>
