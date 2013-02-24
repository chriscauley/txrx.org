function loadJSON(url) { window.location = url; } // IE Fallback
function showLogin() {
    $("#login-dialog").toggleClass("login-visible");
}


simpleCart.successURL = "/classes/?success"
simpleCart.cartHeaders = ["Name", "Price","Remove"]

function showCart() {
    $("#cart-modal").modal({width: 400, modal: true, minHight: 300});
}
function addItem(name,price,id) {
    simpleCart.add('name='+name,'price='+price,'id='+id,'quantity=1');
}
function toggleCourses() {
    $(".in-cart").removeClass("in-cart");
    for (id in simpleCart.items) { $("#c"+id).addClass("in-cart") }
    simpleCart.update();
}
