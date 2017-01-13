<user-checkin>
  <div class="row">
    <div class="col m8 s12 offset-m2" if={ documents_done }>
      <div class="card green white-text">
        <div class="card-content">
          <b>{ documents_done } document{ "s": documents.length != 1 } signed. Thank you!</b>
        </div>
      </div>
    </div>
    <div if={ uR.auth.user } class="col m8 s12 offset-m2">
      <div class="card">
        <div class="card-content">
          <div class="card-title"><b>Logged in as</b></div>
          { uR.auth.user.first_name } { uR.auth.user.last_name } ({ uR.auth.user.username })
          { uR.auth.user.email }
        </div>
      </div>
    </div>
    <div class="col m8 s12 offset-m2" if={ documents.length && uR.auth.user }>
      <h4>Unsigned Documents</h4>
      <div class="card yellow">
        <div class="card-content">
          <p>
            You must sign the following document{ "s": documents.length != 1 }
            before taking any classes or working in the shop.
          </p>
          <li each={ documents }>
            <a onclick={ openDocument }>{ name }</a>
          </li>
        </div>
      </div>
    </div>
    <div class="col s6" if={ subscriptions.length }>
      <h4>Subscriptions</h4>
      <div class="card { card_class }" each={ subscriptions }>
        <div class="card-content">
          <div>
            <a href="/admin/membership/subscription/{ id }/" if={ uR.auth.user.is_superuser }
               class="fa fa-edit right"></a>
            <b>{ month_str } { level_str }</b>
          </div>
          <div>Start Date: { created_str }</div>
          { verbose_status }
        </div>
      </div>
    </div>
    <div class="col s6" if={ classtimes.length }>
      <h4>Classes Today</h4>
      <div each={ classtimes } class="card">
        <div class="card-content">
          <div class="card-title">{ time_string }</div>
          <div>
            <div if={ instructor }><b>You&rsquo;re teaching!</b></div>
            { session.course_name }.<br/>
            <div if={ first_room.name }>Meet at: { first_room.name }</div>
          </div>
        </div>
      </div>
    </div>
    <div class="col s6" if={ permissions.length }>
      <h4>Permissions</h4>
      <div each={ permissions } class="card"><div class="card-title">{ name }</div></div>
      <div class="card">
        <a href="javascript:void(0)" class="ur-tooltip">
          <div class="card-title">Missing Anything?</div>
          <div class="ur-tooltip-content card">
            <div class="card-content">
              Our record keeping on class completions does not go far back
              so please check for missing permissions.
              If you are missing any permissions please email membership@txrxlabs.org so we can get it straightened out.
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>

  var self = this;
  _mount() {
    var checkin = opts.checkin;
    if (this.mounted || !checkin) { return }
    this.documents_done = 0;
    this.permissions = checkin.permissions;
    this.subscriptions = checkin.subscriptions;
    this.documents = checkin.documents;
    uR.forEach(this.subscriptions || [],function(subscription) {
      subscription.created_str = moment(new Date(subscription.created)).format('l');
    });
    this.classtimes = checkin.classtimes;
    uR.forEach(this.classtimes || [],function(classtime) {
      classtime.session = checkin.sessions[classtime.session_id];
      var start = moment(classtime.start), end = moment(classtime.end);
      var start_format = start.minute()?"h:mm":"h";
      var end_format = end.minute()?"h:mm A":"h A";
      if (start.hour() < 12 && end.hour() > 12) { start_format += " A"; }
      classtime.time_string = start.format(start_format) + " - " + end.format(end_format);
      classtime.instructor = classtime.session.instructor_pk == checkin.user_id;
    });
    this.permissions = [];
    uR.forEach(TXRX.permissions,function(permission) {
      if (checkin.permission_ids.indexOf(permission.id) != -1) { self.permissions.push(permission) }
    });
    this.mounted = true;
  }

  reset() {
    this.permissions = this.subscriptions = this.documents = this.documents_done = this.classtimes = undefined;
  }

  this.on("update",function() {
    this._mount();
    // remove completed documents from the list.
    if (this.documents) {
      this.documents = this.documents.filter(function(document) { return !document.completed });
    }
  });
  openDocument(e) {
    self.opts.parent && self.opts.parent.countdown(); // reset countdown timer
    uR.alertElement("user-document",{ document: e.item, parent: this, rfid: self.opts.rfid });
  }
</user-checkin>

<user-document>
  <modal>
    <h5>{ parent.opts.document.name }</h5>
    <markdown content={ parent.opts.document.content }></markdown>
    <ur-form schema={ parent.opts.document.schema } no_focus={ true } action={ parent.action } method="POST"
             ajax_success={ parent.ajax_success }></ur-form>
  </modal>

  ajax_success(data) {
    uR.forEach(opts.parent.documents,function(document,i) {
      if (document.id == data.document.id) { opts.parent.documents[i].completed = new Date(); }
    });
    opts.parent.documents_done++;
    opts.parent.update();
    this.unmount();
  }
  this.on("mount", function() {
    this.action = "/redtape/save/" + opts.document.id + "/";
  });
</user-document>

<todays-checkins>
  <search-users empty={ data.todays_ids }></search-users>
  <div class="checkin-div"></div>

  var self = this;
  select(e) {
    uR.ajax({
      url: "/api/user_checkin/",
      data: {user_id: e.item.id},
      success: function(data) {
        self.active_user = data;
        var e = document.createElement("user-checkin");
        this.root.querySelector(".checkin-div").appendChild(e);
        riot.mount(e,{checkin: self.active_user,parent: self});
      },
      that: this,
      target: self.root,
    });
  }
  back(e) {
    this.root.querySelector(".checkin-div").innerHTML = "";
  }
  toggleIt(e) {
    this.active = (e.item.i==this.active)?undefined:e.item.i;
  }
  changeImage(e) {
    uR.mountElement("change-headshot",{mount_to: "#alert-div"})
  }
</todays-checkins>

<change-headshot>
  <modal>
    <label class="box">
    </label>
    <form><input type="file" onchange={ parent.uploadImage }/></form>
  </modal>

  uploadImage() {
    uR.ajax({
      url: "/api/change_headshot/",
      form: this.root.querySelector("form"),
      method: "POST",
    })
  }
</change-headshot>

<checkin-new-user>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Welcome visitor!</h3></div>
    <div class={ theme.content }>
      <p class="lead">
        We could not find the email you entered in our database.
        Please let us know your name so that we can print a visitor badge.
      </p>
      <ur-form action="/checkin_register/" button_text="Continue" schema={ schema } method="POST"
               initial={ initial }></ur-form>
    </div>
  </div>

  this.schema = ["email","first_name","last_name"];
  this.initial = {email: this.opts.email};
  console.log(this.initial);
</checkin-new-user>

<checkin-home>
  <div class="inner">
    <img class="logo" src="/static/logos/Logo-1_vertical_color_475x375.png" width="200" />
    <div if={ kiosk && !email_checkin && !checkin } class="center">
      <p class="lead">
        Please swipe your RFID to checkin. If you do not have an RFID badge you can checkin using your email instead.
      </p>
      <button onclick={ toggleCheckin } class="btn btn-success">Checkin with Email</button>
    </div>
    <div if={ email_checkin && !checkin } class="center">
      <p class="lead">Enter your email below to checkin. After you checkin you can print a name badge.</p>
      <ur-form action="/checkin_email/" button_text="Check In" schema={ email_schema } method="POST"></ur-form>
      <button if={ kiosk } onclick={ toggleCheckin } class="btn btn-success">Checkin with RFID</button>
    </div>
    <ul if={ messages.length } class={ uR.theme.message_list }>
      <li each={ messages } class={ uR.theme[level+'_class'] }>{ body }</li>
    </ul>
    <center if={ checkin && !uR.auth.user }>
      <br/>
      <button class="btn btn-error red" onclick={ clear }>Done</button>
    </center>
    <div id="checkin_div"></div>
    <center if={ checkin && !uR.auth.user }>
      <button class="btn btn-error red" onclick={ clear }>Done</button>
    </center>
    <div if={ TXRX.DEBUG } class="debug-console">
      <button onclick={ fakeRFID } class="btn btn-warning">Fake new RFID</button>
      <button onclick={ fakeRFID } data-key="0" class="btn btn-warning">Fake CCC</button>
    </div>
  </div>

  var self = this;
  this.email_schema = [
    { name: "email", type: "email" },
  ];
  this.on("mount", function() {
    if (window.location.search.indexOf("kiosk") != -1) {
      this.kiosk = true;
    }
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
    if (e) { uR.mountElement("checkin-register",{ email: "arst@oairesnt.com" }) }
    uR.ready(function() {
      self.email_checkin = !self.kiosk;
      if (uR.auth.user) {
        self.email_checkin = false;
        self.auth_user_checkin = true;
        uR.ajax({
          url: "/checkin_ajax/",
          data: { user_id: uR.auth.user, no_checkin: "true" },
          method: "POST",
          success: self.ajax_success,
          target: self.root,
          that: self,
        });
      }
    });
    cheatCode(function() { window.location.reload(false) });
  });
  window.fakeCheckin = function(rfid) {
    uR.ajax({
      url: "/checkin_ajax/",
      data: { rfid: rfid },
      method: "POST",
      success: self.ajax_success,
      target: self.root,
      that: self,
    });
  }
  toggleCheckin(e) {
    this.email_checkin = !this.email_checkin;
  }
  fakeRFID(e) {
    var i = 10;
    var key = e.target.dataset['key'];
    while (i--) {
      var num = (key !== undefined)?key:Math.floor(Math.random()*10);
      this.press({keyCode: num+48,timeStamp: new Date() });
    }
    this.press({keyCode:13});
  }
  this.ajax_success = function(data,response) {
    if (data.next) {
      data.parent = self;
      uR.alertElement(data.next,data);
      return;
    }
    self.messages = data.messages;
    self.checkin = data.checkin;
    self.update()
    self.checkin_div.innerHTML = "<user-checkin>";
    riot.mount("#checkin_div user-checkin",{checkin:data.checkin, parent: self, rfid: data.rfid})
    self.countdown();
    if (data.badge) {
      var i = document.createElement("iframe");
      i.src = "/static/badge.html?name="+data.checkin.user_display_name;
      i.style="display:none;"
      document.body.appendChild(i);
      window.kill = function() { document.body.removeChild(i); }
    }
  }
  countdown() {
    clearTimeout(self.timeout);
    if (!uR.auth.user) { self.timeout = setTimeout(self.clear,240000); }
  }
  clear(e) {
    clearTimeout(this.timeout);
    uR.route("/checkin/?kiosk")
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
        method: "POST",
        that: this,
      });
      self.current_number = "";
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
  ajax_success(data) {
    parent = self.opts.parent;
    parent.messages = data.messages;
    parent.update();
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
    if (data.no_user) { uR.mountElement("checkin-register",{ email: data.no_user }) }
    else if (data.no_waiver) { uR.mountElement("checkin-waiver",{ email: data.no_waiver }) }
    else { uR.mountElement('checkin',{status: data}) }
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

<maintenance>
  <div class="inner">
    <img class="logo" src="/static/logos/Logo-1_vertical_color_475x375.png" width="200" />
    <h2><center>Under Construction</center></h2>
    <center style="font-size: 1.4em;">
      TXRX Labs is down for scheduled maintenance. <br/> Please check back in 15 minutes.
    </center>
  </div>
</maintenance>
