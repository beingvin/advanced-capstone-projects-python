console.log("connected to cart.js");


// fetch cart items from the server
fetch("/cartItems")
.then(response => response.json())
.then((data) => {
    console.log(data.username)
    cart = data.cart
    for (var i=0; i< cart.length ; i++) {
      id = cart[i]._id.$oid
      title = cart[i].title
      price = cart[i].price
      brand = cart[i].brand
      imageSrc = cart[i].imageLink

      addToCart(id,title, price, imageSrc);
      updateCartTotal();
    }
      
  var total =  document.getElementsByClassName('section-header')[0].innerHTML
  // console.log(total.innerHTML)
});


if (document.readyState == "loading") {
  document.addEventListener("DOMContainerLoaded", ready);
} else {
  ready();
}

function ready() {



  var removeCartButtons = document.getElementsByClassName("btn-danger");

  for (var i = 0; i < removeCartButtons.length; i++) {
    var button = removeCartButtons[i];
    button.addEventListener("click", removeCartItem);
  }

  var quantityInputs = document.getElementsByClassName("cart-quantity-input");
  for (var i = 0; i < quantityInputs.length; i++) {
    var input = quantityInputs[i];
    input.addEventListener("change", quantityChanged);
  }

  var addToCartButtons = document.getElementsByClassName("shop-item-button");
  for (var i = 0; i < addToCartButtons.length; i++) {
    var button = addToCartButtons[i];
    button.addEventListener("click", addToCartClicked);
  }

  document.getElementsByClassName("btn-purchase")[0].addEventListener('click', purchaseClicked)


}

function purchaseClicked(event) {
    alert('Thank you for your purchase')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    while (cartItems.hasChildNodes()){
        cartItems.removeChild(cartItems.firstChild)
    }
    updateCartTotal()
}

function removeCartItem(event) {
  var buttonClicked = event.target;
  buttonClicked.parentElement.parentElement.remove();
  updateCartTotal();
}

function quantityChanged(event) {
  var input = event.target;
  if (isNaN(input.value) || input.value <= 0) {
    input.value = 1;
  }
  updateCartTotal();
}

function addToCartClicked(event) {
  var button = event.target;
  var shopItems = button.parentElement.parentElement;
  var title = shopItems.getElementsByClassName("shop-item-title")[0].innerHTML;
  var price = shopItems.getElementsByClassName("shop-item-price")[0].innerHTML;
  var imageSrc = shopItems.getElementsByClassName("shop-item-image")[0].src;
  addToCart(title, price, imageSrc);
  updateCartTotal();
}

function addToCart(id, title, price, imageSrc) {

  console.log("add to cart")
  var cartRow = document.createElement("div");
  cartRow.classList.add("cart-row") 
  var cartItems = document.getElementsByClassName("cart-items")[0];
  var cartItemName = document.getElementsByClassName('cart-item-title')
  for (var i=0;i<cartItemName.length;i++){
      if(cartItemName[i].innerHTML == title){
          alert('This item is already added to the cart')
          return
      }
  }
  var cartRowContents = `
        <div class="cart-item cart-column">
        <img class="cart-item-image" src="${imageSrc}" width="100" height="100">
        <span class="cart-item-title">${title}</span>
        </div>
        <span class="cart-price cart-column">${price}</span>
        <div class="cart-quantity cart-column">
            <input class="cart-quantity-input" type="number" value="1">
            <a href="/deletItem?id=${id}"><button class="btn btn-danger" type="button">REMOVE</button> </a>
        </div>
    `;
  cartRow.innerHTML = cartRowContents
  cartItems.append(cartRow);
  cartRow.getElementsByClassName("btn-danger")[0].addEventListener('click', removeCartItem)
  cartRow.getElementsByClassName("cart-quantity-input")[0].addEventListener('change', quantityChanged) 
}

function updateCartTotal() {
  var cartItemsContainer = document.getElementsByClassName("cart-items")[0];
  var carRows = cartItemsContainer.getElementsByClassName("cart-row");
  var total = 0;
  for (var i = 0; i < carRows.length; i++) {
    var cartRow = carRows[i];
    var priceElement = cartRow.getElementsByClassName("cart-price")[0];
    var quantityElement = cartRow.getElementsByClassName(
      "cart-quantity-input"
    )[0];
    var price = parseFloat(priceElement.innerHTML.replace("$", ""));
    var quantity = quantityElement.value;
    total = total + price * quantity;
  }
  total = Math.round(total * 100) / 100;
  document.getElementsByClassName("cart-total-price")[0].innerHTML =
    total + " Rs ";
}
