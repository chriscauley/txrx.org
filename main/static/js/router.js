(function() {
  uR.config.form_prefix = "^#?/form"; // triggers the form route!
  function fromTemplate(template_name,data) {
    template_name = template_name.match(/[^\/].+[^\/]/)[0].replace(/\//g,"-");
    riot.compile(
      uR.static("templates/"+template_name+".html"),
      function(html) { uR.mountElement(template_name,data); }
    );
  }
  uR.addRoutes({
    "^/(checkin)/": function() { uR.mountElement("checkin-home"); },
    "^/(checkout)/": function() { uR.mountElement("tool-checkout"); },
    "^/(rooms)/(\d*)": function(path,data) { fromTemplate("room-list",data); },
    "^/(toolmaster)/": uR.auth.loginRequired(function(search_term) {
      uR.mountElement("toolmaster",{search_term:search_term});
    }),
    "^/me/": uR.auth.loginRequired("checkin-home"),
    "^/my-permissions/": uR.auth.loginRequired('badge'),
    "^/(week-hours|todays-checkins|maintenance)/": uR.auth.loginRequired(uR.mountElement),
    "^/(admin/dashboard|needed-sessions)/$": uR.auth.loginRequired(fromTemplate),
    "^/(event/bulk)/$": uR.auth.loginRequired(fromTemplate),
  });
  uR.startRouter();
})();
