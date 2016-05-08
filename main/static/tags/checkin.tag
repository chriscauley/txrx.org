<checkin-home>
  <h1>Welcome to { TXRX.SITE_NAME }</h1>
  <div if={ !email_checkin }>
    <p class="lead">Please swipe your RFID to checkin.</p>
    <button if={ TXRX.DEBUG } onclick={ toggleCheckin } class="btn btn-primary">Checking Using Email</button>
    <br />
    <button if={ TXRX.DEBUG } onclick={ fakeRFID } class="btn btn-warning">Fake RFID</button>
    <div if={ rfid_error } class="alert alert-danger">
      Unknown RFID card. Please go find Chris or Gaby to get it entered in the system.
    </div>
  </div>
  <div if={ email_checkin }>
    <p class="lead">Enter your email below to checkin</p>
    <ur-form action="/checkin_ajax/" button_text="Check In" schema={ email_schema }></ur-form>
  </div>
  <ul if={ messages } class="messagelist">
    <li each={ messages } class="alert alert-{ level }">{ body }</li>
  </ul>

  var self = this;
  this.email_schema = [
    { name: "email", type: "email" }
  ];
  this.on("mount", function() {
    this.current_number = ""
    this.last_press = new Date();
    document.body.classList.add("kiosk");
    document.addEventListener("keypress",this.press);
    this.update();
    uR.ajax({
      url: "/redtape/documents.json",
      success: function(data) {
        TXRX.documents = {};
        uR.forEach(data,function(d) { TXRX.documents[d.id] = d });
      }
    });
    var e = uR.getQueryParameter("e");
    if (e) { TXRX.mainMount("checkin-register",{ email: "arst@oairesnt.com" }) }
  });
  emailCheckin(e) {
    TXRX.mainMount("checkin-email");
  }
  toggleCheckin(e) {
    this.email_checkin = !this.email_checkin;
  }
  fakeRFID(e) {
    var i = 10;
    while (i--) { this.press({keyCode: Math.floor(Math.random()*10)+48,timeStamp: new Date() }); }
    this.press({keyCode:13});
  }
  this.ajax_success = function(data,response) {
    if (data.next) {
      data.parent = self;
      if (!self.root.querySelector(data.next)) {
        var element = document.createElement(data.next);
        self.root.appendChild(element);
      }
      riot.mount(data.next,data);
      return;
    }
    clearTimeout(this.timeout);
    this.messages = data.messages;
    this.timeout = setTimeout(function() { self.messages = []; self.update(); },10000);
  }
  press(e) {
    var num = e.keyCode - 48;
    if (self.current_number && self.current_number.length == 10 && e.keyCode == 13) {
      // enter pressed after 10 fast numbers
      uR.ajax({
        url: "/checkin_ajax/",
        data: { rfid: self.current_number },
        target: this.root.querySelector("button"),
        success: this.ajax_success,
        that: this,
      });
      return e;
    }
    if (num > 9 || num < 0) { return e };
    // my rfid reader is never > 25ms between digits
    if (e.timeStamp - self.last_press > 200) { self.current_number = ""; }
    self.last_press = e.timeStamp;
    self.current_number += num;
  }

</checkin-home>

<new-rfid>
  <modal>
    <h1>Unknown RFID</h1>
    <p class="lead">
      The RFID card you used is not in our system. Please enter your email and password to have this RFID affiliated with your account.
    </p>
    <ur-form schema={ TXRX.schema.new_rfid } initial={ parent.opts } action="/add_rfid/" method="POST"
             ajax_success={ parent.ajax_success }></ur-form>
  </modal>

  var self = this;
  self.parent = self.opts.parent;
  ajax_success(data) {
    self.parent.messages = data.messages;
    self.parent.update();
    self.unmount();
  }
</new-rfid>

<checkin-email>
  <p class="lead">
    Enter your email below to checkin.
  </p>
  <ur-form schema={ schema } action="/checkin_ajax/"></ur-form>
  schema = [
    { name: 'email', type: 'email' },
  ]
  ajax_success(data,response) {
    if (data.no_user) { TXRX.mainMount("checkin-register",{ email: data.no_user }) }
    else if (data.no_waiver) { TXRX.mainMount("checkin-waiver",{ email: data.no_waiver }) }
    else { TXRX.mainMount('checkin',{status: data}) }
  }
</checkin-email>

<checkin-register>
  <p class="lead">
    We could not find an account with that email.<br/>
    Please create one now or press "Go Back".
  </p>
  <ur-form action="/checkin/signup/"></ur-form>

  this.schema = [
    { name: "email", type: "email", value: this.opts.email },
    { name: "first_name" },
    { name: "last_name" },
    { name: "password", type: "password", minlength: 8 }
  ]
</checkin-register>

<checkin-waiver>
  <p class="lead">
    We could not find a safty waiver on file for you.<br/>
    Please read and sign the following document.
    If you want to try a different email or RFID card,
    <a onclick={ goBack }>go back</a> to the previous screen.
  </p>
  <ur-form action="/checkin/waiver/">
  <h2>{ TXRX.documents[2].name }</h2>
  <ur-markdown>{ TXRX.documents[2].content }</ur-markdown>
  </ur-form>

  this.schema = TXRX.documents[2].schema;
  this.schema.push({ name: "name_typed", })
  this.schema.push({ name: "date_typed", })

</checkin-waiver>
