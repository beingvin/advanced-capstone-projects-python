console.log('connected to stripe_checkout.js')
document.getElementsByClassName("btn-purchase")[0].addEventListener('click', create_checkout_session )

// click puchase button 

function create_checkout_session() {

    // var x = cartItems()  
  
    fetch("/cart/stripe_pay", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: cartItems()
      }),
    })
    .then((res) => {
      if (res.ok) return res.json();
      return res.json().then((json) => Promise.reject(json));
    })
    .then(({ url }) => {
      // console.log(url);
      window.location = url;
    })
    .catch((e) => {
      console.error(e.error);
    });
}


function cartItems(){
    var cartItemsContainer = document.getElementsByClassName("cart-items")[0];
    var cartRows = cartItemsContainer.getElementsByClassName("cart-row");
    var cartItems= []
    for (var i = 0; i < cartRows.length; i++) {
      var cartRow = cartRows[i];
      var idElement = cartRow.getElementsByClassName("cart-item-id")[0].value
      var titleElement = cartRow.getElementsByClassName("cart-item-title")[0].innerHTML
      var priceElement = cartRow.getElementsByClassName("cart-price")[0].innerHTML;
      var quantityElement = cartRow.getElementsByClassName("cart-quantity-input")[0].value;

      console.log(quantityElement)
    //   var items = {
    //     // title: titleElement,
    //     // price: priceElement,
    //     quantity: quantity
    //   }
      cartItems.push({id:idElement, quantity: parseInt(quantityElement)})
 
  
    }
    return cartItems

  } 