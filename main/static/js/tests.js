(function() {
  function badLogin() {
    if (uR.auth.user) { uR.route("/auth/logout/") }
    return this.do("Login with a non-existant user.")
      .click("[href='#/auth/login/']")
      .wait("#id_username")
      .changeValue("#id_username","monkey")
      .changeValue("#id_password","butler")
      .click("#submit_button")
      .wait("auth-modal .non_field_error")
      .checkResults()
      .done("Failed at logging in.")
  }

  function doLogin() {
    var context = {
      "#id_username": "tester",
      "#id_password": "password",
    };
    if (uR.auth.user && uR.auth.username == "tester") { return }
    this.do("Login as user")
      .wait("[href='#/auth/login/']")
      .click()
      .changeValue("#id_username",'tester')
      .changeValue("#id_password",'password')
      .click("#submit_button")
      .done("Login complete")
  }

  function addToCart() {
    this.do("Add item to cart")
      .setPath("/classes/338/healthy-eating-introduction-to-juicing/")
      .wait(function cartLoaded() { return uR && uR.drop && uR.drop.cart && uR.drop.cart.all_items } )
      .then(uR.drop.emptyCart)
      .wait("#s1715 add-to-cart button")
      .click()
      .wait("shopping-cart a.decrement")
      .click()
      .done("Item in cart");
  }

  function makeComment() {
    var rando = Math.random();
    var matched_comment_id;
    this.do("Testing comment")
      .setPath("/blog/192/houston-vr-and-txrx/")
      .test(doLogin)
      .wait("#f0 textarea")
      .changeValue("#f0 textarea","top "+rando)
      .click("#f0 .submit-post")
      .wait(function() {
        uR.forEach(document.querySelectorAll("comment .comment_content"),function(comment) {
          if (comment.innerHTML.indexOf("top "+rando) != -1) { matched_comment_id = comment.id }
        });
        console.log(document.querySelector("#"+matched_comment_id+" a[title='reply']"))
        return matched_comment_id;
      })
      .click("#"+matched_comment_id+" a[title='reply']")
      .wait("#"+matched_comment_id+" comment-form textarea")
      .changeValue("#"+matched_comment_id+" comment-form textarea","reply to "+rando)
      .click("#"+matched_comment_id+" comment-form .submit-post")
      .wait("#"+matched_comment_id+" comment-form textarea")
  }

  konsole.addCommands(badLogin, addToCart) //,addToCart,makeComment);
})();
