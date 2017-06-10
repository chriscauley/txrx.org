(function() {
  function badLogin(t) {
    if (uR.auth.user) { uR.route("/auth/logout/") }
    return t.do("Login with a non-existant user.")
      .click("[href='\#/auth/login/']")
      .waitFor("#id_username")
      .changeValue("#id_username","monkey")
      .changeValue("#id_password","butler")
      .click("#submit_button")
      .waitFor("auth-modal .alert-danger")
      .assertEqual(
        function() { return document.querySelector("auth-modal .alert-danger").innerText },
        "Username and password do not match."
      )
      .done("Failed at logging in.")
  }

  konsole.addCommands(badLogin);
})();
