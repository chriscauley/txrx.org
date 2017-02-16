(function() {
  function fromTemplate(template_name,data) {
    template_name = template_name.match(/[^\/].+[^\/]/)[0].replace(/\//g,"-");
    riot.compile(
      "/static/templates/"+template_name+".html",
      function(html) { uR.mountElement(template_name,data); }
    );
  }
  uR.addRoutes({
    "^/(checkin)/": function() { uR.mountElement("checkin-home"); },
    "^/(checkout)/": function() { uR.mountElement("tool-checkout"); },
    "^/(rooms)/(\d*)": function(path,data) { fromTemplate("room-list",data); },
    "^/(toolmaster)/": function(search_term) {
      uR.mountElement("toolmaster",{search_term:search_term});
    },
    "^/me/": uR.auth.loginRequired("checkin-home"),
    "^/my-permissions/": uR.auth.loginRequired('badge'),
    "^/rfid/": function() { uR.mountElement("set-rfid"); },
    "^/(week-hours|todays-checkins|maintenance)/": uR.auth.loginRequired(uR.mountElement),
    "^/(admin/dashboard|needed-sessions)/$": uR.auth.loginRequired(fromTemplate),
  });
})();
