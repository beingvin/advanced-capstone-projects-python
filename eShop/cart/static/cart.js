console.log("connected to cart.js");


// fetch cart items from the server(/cartItems)
fetch("/cart/cartItems")
.then(response => response.json())
.then((data) => {
   
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



// remove items from the cart 

function removeCartItem(event) {
  var buttonClicked = event.target;
  buttonClicked.parentElement.parentElement.remove();
  updateCartTotal();
}

// item quantity change

function quantityChanged(event) {
  var input = event.target;
  if (isNaN(input.value) || input.value <= 0) {
    input.value = 1;
  }
  updateCartTotal();
}


function addToCart(id, title, price, imageSrc) {

  
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
            <input class="cart-item-id" type="hidden" value=${id}>
            <a href="/cart/deletItem?id=${id}"><button class="btn btn-danger" type="button">REMOVE</button> </a>
        </div>
    `;
  cartRow.innerHTML = cartRowContents
  cartItems.append(cartRow);
  cartRow.getElementsByClassName("btn-danger")[0].addEventListener('click', removeCartItem)
  cartRow.getElementsByClassName("cart-quantity-input")[0].addEventListener('change', quantityChanged) 
}

// update cart total 

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





