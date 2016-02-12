<checkin>
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
    { status.user } checked in at { status.time_ins }
  </div>
  <div if={ status.time_out } class="alert alert-success">
    { status.user } checked out at { status.time_outs }<br/>
    Time Difference: { status.diffs }
  </div>

  var self = this;
  this.on("mount", function() {
    this.last_press = new Date();
    document.body.classList.add("kiosk");
    document.addEventListener("keypress",this.press);
  });
  emailCheckin(e) {
    TXRX.mainMount("email-checkin");
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

</checkin>

<email-checkin>
  <h1>Welcome to { TXRX.SITE_NAME }</h1>
  <p class="lead">Enter your email below to checkin.</p>
  <ur-form schema={ schema }></ur-form>
  schema = [
    { name: 'email', type: 'email' },
  ]
</email-checkin>
