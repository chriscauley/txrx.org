<checkin>
  <h2>Swipe RFID Card</h2>
  <input name="rfid" id="rfid" autocomplete="off" onkeyup={ press } />
  <div if={ status } class="alert alert-success">
    { status.user } checked in at { status.time_ins }
  </div>
  <div if={ status.time_out } class="alert alert-success">
    { status.user } checked out at { status.time_outs }<br/>
    Time Difference: { status.diffs }
  </div>

  var that = this;
  var timeout;
  function press(e) {
    var rfid = that.rfid.value;
    if (!rfid) { return }
    that.root.classList.add('loading');
    $.get(
      '/checkin/',
      {rfid: rfid},
      function(data) {
        that.root.classList.remove('loading');
        if (data.status == 404) { that.error = true }
        else {
          data.time_in = new Date(data.time_in);
          data.time_ins = data.time_in.getHours()%12 + ":" + data.time_in.getMinutes()
          if (data.time_out) {
            data.time_out = new Date(data.time_out);
            data.time_outs = data.time_out.getHours()%12 + ":" + data.time_out.getMinutes()
            var minutes = (data.time_out.valueOf() - data.time_in.valueOf())*0.001/60;
            data.diffs = Math.floor(minutes/60) + " hours " + Math.floor(minutes % 60) + " minutes"
          }
          that.status = data;
          that.update();
        }
      },
      "json"
    );
  }
  this.press = uR.debounce(this.press);
</checkin>
