(function() {
  uR.addRoutes({
    "/select-address/": uR.auth.loginRequired("select-address"),
  });
})()

<select-address>
  <div class={ theme.outer }>
    <div class={ theme.header }>
      <h3>Select Address</h3>
    </div>
    <div class={ theme.content }>
      <div each={ addresses } onclick={ selectAddress }>
        { name }<br />
        { address }<br />
        <div if={ address2 }>{ address2 }</div>
        { city }, { state } { zip_code }<br />
        { country.name }<br />
      </div>
      <ur-form schema="/api/schema/address.Address/" action="/address/add/" method="POST"></ur-form>
    </div>
  </div>

  var self = this;
  this.on("mount", function() {
    var query = `
    query {
      myAddresses {
        id,
        name,
        address,
        address2,
        city,
        state,
        country,
        zipCode,
      }
    }`;
    uR.ajax({
      url: "/graphql",
      data: {query: query},
      success: function(data) {
        self.addresses = data.data.myAddresses;
      },
      that: this,
      target: this.root,
    });
  });
  this.ajax_success = function(data,request) {
    if (self.opts.post_to) {
      uR.ajax({
        url: self.opts.post_to,
        method: "POST",
        data: data,
      });
    }
    if (self.opts.success) { self.opts.success({selected_address: data}) }
  }
  selectAddress(e) {
    this.ajax_success(e.item);
  }
</select-address>
