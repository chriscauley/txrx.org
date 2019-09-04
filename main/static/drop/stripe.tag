uR.ready(function() {
  var o = {
    tagname: 'stripe-checkout',
    copy: "Credit Card",
    className: uR.config.btn_primary,
    icon: "fa fa-cc-stripe",
    name: 'stripe',
  };
  uR.drop.payment_backends.push(o);
});

<stripe-checkout>
  <div class={ theme.outer }>
    <div class={ theme.header }>
      <h3>Checkout with Stripe</h3>
    </div>
    <div class={ theme.content }>
      <ur-form schema={ schema } initial={ initial } success_text="Pay ${ uR.drop.cart.total_price }"></ur-form>
      <center>
        <a onclick={ uR.drop.openCart }>&laquo; Back to cart</a>
      </center>
    </div>
  </div>

  var self = this;
  this.schema = [
    {
      name: 'number', label: "Credit Card Number", type: "tel",
      onMount: function() { $("stripe-checkout [name=number]").payment("formatCardNumber"); }
    },
    { name: 'expiry', label: "Expiration Date", max_length: 2,
      onMount: function() { $("stripe-checkout [name=expiry]").payment("formatCardExpiry"); }
    },
    {
      name: 'cvc', label: "CVC Code",
      onMount: function() { $("stripe-checkout [name=cvc]").payment("formatCardCVC"); }
    },
  ];
  if (!uR.auth.user) {
    // stripe doesn't give us email, so we need it
    this.schema.push(uR.schema.fields.no_email);
  }
  if (uR.DEBUG && window.location.search.indexOf("cheat") != -1) {
    this.initial = {number: "4111 1111 1111 1111", cvc: '123', exp_month: "01", exp_year: "2019" }
  }
  submit(ur_form) {
    self.ajax_target = self.root.querySelector("."+self.theme.outer);
    self.error = undefined;
    self.ajax_target.setAttribute("data-loading","fade");
    var data = ur_form.getData();
    var expiry = data.expiry.replace(/ /g,"").split("/");
    data.exp_month = expiry[0];
    data.exp_year = expiry[1];
    self.email = data.email;
    delete data.email; delete data.expiry;
    Stripe.card.createToken(data,this.stripeResponseHandler)
  }
  setError(error) {
    var ur_form = self.tags['ur-form'];
    ur_form.non_field_error = "An error occurred while processing your payment";
    if (error) { ur_form.non_field_error += ": "+ error }
    ur_form.update();
  }
  this.stripeResponseHandler = function(status,response) {
    if (response.error) {
      self.ajax_target.removeAttribute('data-loading');
      self.setError(response.error.message);
      return;
    }
    uR.drop.ajax({
      method: "POST",
      url: "/stripe/payment/",
      data: {token: response.id,total:uR.drop.cart.total_price,email: self.email},
      target: self.ajax_target,
      success: function(data) {
        self.ajax_target.setAttribute("data-loading","fade");
        window.location = data.next;
      },
      error: function(data) { self.setError(data.error); }
    });
  }
  close(e) {
    this.unmount();
  }
</stripe-checkout>
