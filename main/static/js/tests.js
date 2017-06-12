(function() {
  function badLogin(t) {
    if (uR.auth.user) { uR.route("/auth/logout/") }
    return t.do("Login with a non-existant user.")
      .click("[href='\#/auth/login/']")
      .wait("#id_username")
      .changeValue("#id_username","monkey")
      .changeValue("#id_password","butler")
      .click("#submit_button")
      .wait("auth-modal .alert-danger")
      .assertEqual(
        function() { return document.querySelector("auth-modal .alert-danger").innerText },
        "Username and password do not match."
      )
      .done("Failed at logging in.")
  }

  function addToCart(t) {
    t.do("Add item to cart")
      //.setPath("/classes/225/woodworking-ii-milling-dimensioning/")
      .then(uR.drop.emptyCart)
      .click("#s1594 add-to-cart button")
      .wait("shopping-cart a.decrement")
      .click()
      .done("Item in cart");
  }

  konsole.addCommands(badLogin,addToCart);
})();
