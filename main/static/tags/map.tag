<floorplan>
  <div class="left">
    <h1>Today at TXRX Labs</h1>
    <div class="well" each={ event_blocks }>
      <h2>{ time }</h2>
      <ul class="event_list">
        <li class="room" each={ events }>
          <span class="room_marker" style="background: { color };">{ map_key }</span>
          <span>{ name }</span>
        </li>
      </ul>
    </div>
  </div>
  <div id="floorplan_wrapper">
    <canvas onclick={ findRoom }></canvas>
    <div class="legend">
      <h1>Legend</h1>
      <ul class="event_list">
        <li class="room" each={ roomgroups }>
          <span class="room_marker" style="background: url({ fill }) center"></span>
          <span>{ name }</span>
        </li>
      </ul>
    </div>
  </div>

  var that = this;
  findRoom(e) {
    var x = e.offsetX;
    var y = e.offsetY;
    uR.forEach(that.dxfs, function(room) {
      if ((room.x < x) && (x < room.x + room.w) && (room.y < y) && (y < room.y + room.h)) {
        console.log(room.id);
      }
    });
  }
  that.bounceUp = uR.debounce(that.update.bind(that));
  this.on("mount",function() {
    this._location = -1;
    that.fill_images = {};
    $.get(
      '/geo/locations.json?pks='+this.opts.locations,
      function(data) {
        that.data = data;
        that.update();
        that.roomgroups = [];
        for (rg_id in that.data.roomgroups) { that.roomgroups.push(that.data.roomgroups[rg_id]); }
        for (room_id in that.data.rooms) {
          var room = that.data.rooms[room_id];
          var roomgroup = that.data.roomgroups[room.roomgroup_id];
          if (!roomgroup) { continue; }
          room.fill = roomgroup.fill;
          room.color = roomgroup.color;
          that.bounceUp();
        };
        loadEvents();
      },
      'json'
    );
  });
  function loadEvents() {
    $.get(
      '/geo/events.json',
      function(data) {
        that.event_blocks = data;
        uR.forEach(that.event_blocks,function(block) {
          block.time = moment(block.datetime).format('h:mm a')
          uR.forEach(block.events,function(event) {
            event.color = that.data.rooms[event.room_id].color;
            event.map_key = that.data.rooms[event.room_id].map_key;
          });
        });
        that.bounceUp();
      },
      'json'
    )
  }
  this.on("update",function() {
    if (!this.data) { this.root.setAttribute('ur-loading','mask'); return; }
    this.root.removeAttribute('ur-loading');
    //this._location ++;
    //if (this._location >= this.opts.locations.length) { this._location = 0; }
    that._location = 0;
    this.location = this.data.locations[this.opts.locations[this._location]];
    calculateBounds();
    initCanvas();
    createRooms();
  });

  // Math for the canvas
  var x_max, y_max, x_min, x_max, WIDTH, HEIGHT, scale, durn;
  var rotate = true, mirror_x = false, mirror_y = true;

  function calculateBounds() {
    // these next two lines are lame, it should be done in some othe manner
    if (durn) { return }
    durn = true;
    x_max = -Infinity, y_max = -Infinity, x_min = Infinity, y_min = Infinity;
    for (var di=0;di<that.location.dxfs.length;di++) {
      var dxf = that.location.dxfs[di];
      for (pi=0;pi<dxf.points.length;pi++) {
        p = dxf.points[pi];
        x_max = Math.max(x_max,p[0]);
        x_min = Math.min(x_min,p[0]);
        y_max = Math.max(y_max,p[1]);
        y_min = Math.min(y_min,p[1]);
      }
    }
    var bar_width = 340;
    var wrapper = document.getElementById("floorplan_wrapper");
    var wrapper_width = wrapper.offsetWidth;
    var wrapper_height = wrapper.offsetHeight;
    var wrapper_ratio = wrapper_width/wrapper_height;
    WIDTH = (x_max - x_min)
    HEIGHT = (y_max - y_min);
    if (rotate) {
      HEIGHT = (x_max - x_min);
      WIDTH = (y_max - y_min);
    }
    var ratio = WIDTH/HEIGHT;
    scale = (wrapper_ratio < ratio)?wrapper_width/WIDTH:wrapper_height/HEIGHT;
    HEIGHT *= scale;
    WIDTH *= scale;

    // correct so that it's 0,0 for x_min,y_min
    for (var di=0;di<that.location.dxfs.length;di++) {
      var dxf = that.location.dxfs[di];
      for (pi=0;pi<dxf.points.length;pi++) {
        p = dxf.points[pi];
        if (rotate) {
          dxf.points[pi] = [WIDTH-scale*(p[1]-y_min),scale*(p[0]-x_min)];
        } else {
          dxf.points[pi] = [scale*(p[0]-x_min),HEIGHT-scale*(p[1]-y_min)];
        }
        if (mirror_x) { dxf.points[pi][0] = WIDTH - dxf.points[pi][0]; }
        if (mirror_y) { dxf.points[pi][1] = HEIGHT - dxf.points[pi][1]; }
      }
    }
  }
  function createRooms() {
    that.dxfs = [];
    var floorplan_wrapper = document.getElementById('floorplan_wrapper');
    var room_map = {};
    for (var di=0;di<that.location.dxfs.length;di++) {
      var dxf = that.location.dxfs[di];
      var room = that.data.rooms[dxf.room_id];
      if (room) {
        dxf.in_calendar = room.in_calendar
        dxf.map_key = room.map_key;
        dxf.name = room.name;
        if (room && that.data.roomgroups[room.roomgroup_id]) {
          var roomgroup = that.data.roomgroups[room.roomgroup_id];
          dxf.fill = roomgroup.fill;
          dxf.color = roomgroup.color;
        }
      }
      var x_max = -Infinity, y_max = -Infinity, x_min = Infinity, y_min = Infinity;
      for (pi=0;pi<dxf.points.length;pi++) {
        p = dxf.points[pi];
        x_max = Math.max(x_max,p[0]);
        x_min = Math.min(x_min,p[0]);
        y_max = Math.max(y_max,p[1]);
        y_min = Math.min(y_min,p[1]);
      }
      if (dxf.fill && !that.fill_images[dxf.fill]) {
        var img = document.createElement('img');
        img.src = dxf.fill;
        that.fill_images[dxf.fill] = img;
        $(img).load(draw);
      }
      that.dxfs.push({
        id: dxf.id,
        x: x_min,
        y: y_min,
        w: x_max-x_min,
        h: y_max-y_min,
        color: room?dxf.color:"white",
        fill: room?dxf.fill:'',
        stroke: "black"
      });
      if (dxf.in_calendar) {
        var color = dxf.color || 'white';
        var room_marker = document.createElement('div');
        room_marker.style.backgroundColor = color;
        room_marker.className = 'room_marker';
        room_map[color] = room_map[color] || [];
        room_map[color].push(dxf);
        room_marker.innerHTML = dxf.map_key;
        room_marker.style.left = (x_max+x_min)/2+"px";
        room_marker.style.top = (y_max+y_min)/2+"px";
        room_marker.title = dxf.name;
        floorplan_wrapper.appendChild(room_marker);
      }
    }
    draw();
  }
  function rect(r,ctx) {
    ctx.beginPath();
    ctx.rect(r.x,r.y,r.w,r.h);
    ctx.fillStyle = r.color;
    if (r.fill) {
      pattern = ctx.createPattern(that.fill_images[r.fill],'repeat');
      ctx.fillStyle = pattern;
    }
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = r.stroke;
    ctx.stroke();
  }

  function draw () {
    context.clearRect(0,0,canvas.width,canvas.height);
    for (var ri=0;ri<that.dxfs.length;ri++) { rect(that.dxfs[ri],context); }
  }

  var canvas, context;
  function initCanvas() {
    canvas = that.root.querySelector("canvas");
    context = canvas.getContext("2d");
    canvas.width = WIDTH+2;
    canvas.height = HEIGHT+2;
  }
</floorplan>
