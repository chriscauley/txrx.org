<week-hours>
  <div onmouseout={ leave }>
    <div class="day" each={ days }>
      { name }
      <div class="hour { className }" each={ hours } onmousedown={ click } onmousemove={ drag }
           onmouseup={ leave } onmouseout={ noop }>
        { s } { wi }
      </div>
    </div>
  <div style="clear:both;"></div>
  </div>

  var that = this;
  this.days = [];
  var dow = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  dow.forEach(function(dname,di) {
    var _d = {name: dname, hours: []}
    var hi = 9;
    while (hi<22) {
      h = hi%12+1;
      _d.hours.push({h: hi+1, s: h+":00",checked:false, di: di })
      _d.hours.push({h: hi+1+0.5, s: h+":30",checked:false, di: di })
      hi++;
    }
    that.days.push(_d);
  });

  function eachHour(f) {
    for (var di=0;di<that.days.length;di++) {
      var day = that.days[di];
      for (var hi=0;hi<day.hours.length;hi++) {
        f(day.hours[hi]);
      }
    }
  }

  this.on("update", function() {
    if (that.start && that.stop) {
      if (that.start != that._start || that.stop != that._stop) {
        that.d_start = Math.min(that.start.di,that.stop.di),
        that.d_stop = Math.max(that.start.di,that.stop.di),
        that.h_start = Math.min(that.start.h,that.stop.h),
        that.h_stop = Math.max(that.start.h,that.stop.h);
        eachHour(function(hour) {
          hour.className = hour.has?"green":"";
          hour._has = hour.has;
          if (that.d_start <= hour.di && hour.di <= that.d_stop) {
            if (that.h_start <= hour.h && hour.h <= that.h_stop) {
              hour.className = that.adding?"pink":"red";
              hour._has = that.adding;
            }
          }
        });
        that._start = that.start, that._stop = that.stop;
      }
    }    
  });

  leave(e) {
    that.start = that.stop = null;
    eachHour(function(hour) {
      hour.has = hour._has
      hour.className = hour.has?"green":"";
    });
  }
  click(e) {
    that.adding = !e.item.has;
    that.start = e.item;
  }
  drag(e) {
    if (that.start) {
      that.stop = e.item;
    }
  }
  touch(e) {
    document.body.style.background = "pink";
  }
  noop(e) {
    e.stopPropagation();
  }
</week-hours>
