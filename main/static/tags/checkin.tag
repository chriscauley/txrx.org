<user-checkin>
  <div class="row">
    <div class="col m8 s12" if={ documents.length }>
      <h4>Required Documents</h4>
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
      <div class="card { card_class } white-text" each={ subscriptions }>
        <div class="card-content">
          <div>
            <a href="/admin/membership/subscription/{ id }/" if={ TXRX.user.is_superuser }
               class="fa fa-edit white-text right"></a>
            <b>{ month_str } { level }</b>
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
          <div class="card-title">{ start_string }-{ end_string }</div>
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
              If you are missing any permissions please email info@txrxlabs.org so we can get it straightened out.
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>

  var self = this
  this.on("mount",function() {
    var checkin = opts.checkin;
    this.permissions = checkin.permissions;
    this.subscriptions = checkin.subscriptions;
    this.documents = checkin.documents;
    uR.forEach(this.subscriptions || [],function(subscription) {
      subscription.created_str = moment(new Date(subscription.created)).format('l');
    });
    this.classtimes = checkin.classtimes;
    uR.forEach(this.classtimes || [],function(classtime) {
      classtime.session = checkin.sessions[classtime.session_id];
      classtime.start_string = moment(classtime.start).format("h:mm A");
      classtime.end_string = moment(classtime.end).format("h:mm A");
      classtime.instructor = classtime.session.instructor_pk == checkin.user_id;
    });
    this.permissions = [];
    uR.forEach(TXRX.permissions,function(permission) {
      if (checkin.permission_ids.indexOf(permission.id) != -1) { self.permissions.push(permission) }
    });
    this.update()
  })

  this.on("update",function() {
    // remove completed documents from the list.
    if (this.documents) {
      this.documents = this.documents.filter(function(document) { return !document.completed });
    }
  });
  openDocument(e) {
    uR.mountElement("user-document",{ mount_to: uR.config.mount_alerts_to, document: e.item, parent: this });
  }
</user-checkin>

<user-document>
  <modal>
    <h5>{ parent.opts.document.name }</h5>
    <markdown content={ parent.opts.document.content }></markdown>
    <ur-form schema={ parent.opts.document.schema } no_focus={ true } action={ parent.action } method="POST"
             ajax_success= { parent.ajax_success }></ur-form>
  </modal>

  ajax_success(data) {
    uR.forEach(opts.parent.documents,function(document,i) {
      if (document.id == data.document.id) { opts.parent.documents[i].completed = new Date(); }
    });
    opts.parent.update();
    this.unmount();
  }
  this.on("mount", function() {
    this.action = "/redtape/save/" + opts.document.id + "/";
  });
</user-document>

<todays-checkins>
  <div class="collapsible collapsible-accordion">
    <div each={ checkin,i in checkins } onclick={ toggleIt } class={ active: active == i }>
      <div class="collapsible-header">
        { checkin.user_display_name } ({ checkin.sub_str })
      </div>
      <div class="collapsible-body">
        <div class="collapsible-inner">
          <user-checkin checkin={ checkin }></user-checkin>
        </div>
      </div>
    </div>
  </div>

  var self = this;
  uR.ajax({
    url: "/todays_checkins.json",
    success: function(data) {
      self.checkins = data.checkins;
      uR.forEach(self.checkins,function(checkin) {
        var _s = checkin.subscriptions[0];
        checkin.sub_str = _s?(_s.level+" "+_s.verbose_status):"Non-member";
      });
    },
    that: this
  });
  toggleIt(e) {
    this.active = (e.item.i==this.active)?undefined:e.item.i;
  }
</todays-checkins>

<checkin-home>
  <div class="inner">
    <img class="logo" src="/static/logos/Logo-1_vertical_color_475x375.png" width="200" />
    <div if={ kiosk && !email_checkin }>
      <p class="lead" style="text-align: center;">Please swipe your RFID to checkin.</p>
      <button if={ TXRX.DEBUG } onclick={ toggleCheckin } class="btn btn-success">Checking Using Email</button>
      <br />
      <button if={ TXRX.DEBUG } onclick={ fakeRFID } class="btn btn-warning">Fake RFID</button>
      <div if={ rfid_error } class="alert alert-danger">
        Unknown RFID card. Please go find Chris or Gaby to get it entered in the system.
      </div>
    </div>
    <div if={ email_checkin }>
      <p class="lead"><center>Enter your email below to checkin</center></p>
      <ur-form action="/checkin_ajax/" button_text="Check In" schema={ email_schema }></ur-form>
      <button if={ kiosk } onclick={ toggleCheckin } class="btn btn-success">Checkin Using RFID</button>
    </div>
    <center if={ DEPRACATED && auth_user_checkin }>
      <br />
      <button class="btn btn-success">Checkin as { TXRX.user.username }</button>
    </center>
    <ul if={ messages.length } class="messagelist">
      <li each={ messages } class="alert alert-{ level }">{ body }</li>
    </ul>
    <user-checkin if={ checkin } checkin={ checkin }></user-checkin>
    <center if={ !TXRX.user.id }>
      <button if={ classtimes.length || permissions.length || messages.length }
              class="btn btn-success" onclick={ clear }>Back</button>
    </center>
  </div>

  var self = this;
  this.email_schema = [
    { name: "email", type: "email" }
  ];
  this.on("mount", function() {
    this.email_checkin = true;
    if (window.location.search.indexOf("kiosk") != -1) {
      this.kiosk = true;
      this.email_checkin = false;
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
    if (e) { TXRX.mainMount("checkin-register",{ email: "arst@oairesnt.com" }) }
    TXRX.ready(function() {
      if (TXRX.user.id) {
        self.email_checkin = false;
        self.auth_user_checkin = true;
        uR.ajax({
          url: "/checkin_ajax/",
          data: { user_id: TXRX.user.id, no_checkin: "true" },
          success: self.ajax_success,
          target: self.root,
          that: self,
        });
      }
    });
    cheatCode(function() { window.location.reload(false) });
  });
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
    self.checkin = data.checkin;
    clearTimeout(this.timeout);
    if (!(TXRX.user && TXRX.user.id)) { this.timeout = setTimeout(self.clear,30000); }
  }
  clear(e) {
    clearTimeout(this.timeout);
    self.permissions = [];
    self.classtimes = [];
    self.ur_form.clear();
    self.update();
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
