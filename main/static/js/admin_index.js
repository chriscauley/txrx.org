$(function() {
  if ($("flag-list").length) {
    $.get(
      "/api/membership/activeflag/",
      function(data) {
        var now = [], then = [], later = [], flag, days;
        for (var i=0;i<data.length;i++) {
          flag = data[i];
          days = flag.days_until_next_action;
          if (days == 0) { now.push(flag); }
          else if (days > 0) { later.push(flag); }
          else { then.push(flag) }
        }
        var flagsets = [
          {verbose: "Overdue Flags", flags: then},
          {verbose: "Todays Flags", flags: now},
          {verbose: "Upcoming Flags", flags: later},
        ];
        riot.mount("flag-list",{flagsets:flagsets});
      },
      "json"
    )
  }
});
