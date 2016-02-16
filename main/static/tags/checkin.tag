<checkin-home>
  <h1>Welcome to { TXRX.SITE_NAME }</h1>
  <p class="lead">
    Please swipe your RFID card to checkin.
    <br />
    If you do not have an RFID card...
  </p>
  <button class="btn btn-primary" onclick={ emailCheckin }>Checkin using email address</button>
  <div if={ rfid_error } class="alert alert-danger">
    Unknown RFID card. Please go find Chris or Gaby to get it entered in the system
  </div>
  <div if={ by_email }>
    <div><input name="email" id="id_email" autocomplete="off" onkeyup={ press } /></div>
    <input type="submit" class="btn btn-primary" />
  </div>
  <div if={ status } class="alert alert-success">
    { status.user } checked in at { status.sin }
    <div if={ status.time_out }>
      Checked out at { status.sout }<br/>
    </div>
  </div>

  var self = this;
  this.on("mount", function() {
    this.last_press = new Date();
    this.status = this.opts.status;
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
    if (e) { TXRX.mainMount("checkin-register",{ email: 'arst@oairesnt.com' }) }
  });
  this.on("update", function() {
    if (this.status) {
      this.status.sin = moment(this.status.time_in).format("h:mm a");
      this.status.sout = moment(this.status.time_out).format("h:mm a");
    }
  });
  emailCheckin(e) {
    TXRX.mainMount("checkin-email");
  }
  press(e) {
    var num = e.keyCode - 48;
    if (num > 9 || num < 0) { return };
    // my rfid reader is never > 25ms between digits
    if (e.timeStamp - self.last_press > 100) { self.current_number = ""; }
    self.last_press = e.timeStamp;
    self.current_number += num;
    if (self.current_number.length == 10) { self.checkRFID(); }
  }
  checkRFID(e) {
    uR.ajax({
      url: '/checkin/',
      data: {rfid: self.current_number},
      success: function(data) {
        if (data.status == 404) { self.rfid_error = true; return }
        data.time_in = new Date(data.time_in);
        data.time_ins = data.time_in.getHours()%12 + ":" + data.time_in.getMinutes()
        if (data.time_out) {
          data.time_out = new Date(data.time_out);
          data.time_outs = data.time_out.getHours()%12 + ":" + data.time_out.getMinutes()
          var minutes = (data.time_out.valueOf() - data.time_in.valueOf())*0.001/60;
          data.diffs = Math.floor(minutes/60) + " hours " + Math.floor(minutes % 60) + " minutes"
        }
        self.status = data;
      },
      target: self.root,
      that: self
    });
  }
  this.checkRFID = uR.debounce(this.checkRFID,100);

</checkin-home>

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
