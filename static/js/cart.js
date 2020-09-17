/*var updateBtns = document.getElementsByClassName('update-cart')
for (i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
       var storeID = this.dataset.product
       var action = this.dataset.action
       console.Log('product__id:': pid, 'Action:',action)

       console.Log('USER:',user)
       if(user == 'AnonymousUser'){
         console.Log('Not logged in')
       }else{
          updateUserOrder(product__id, action)
       }
    })

}
function updateUserOrder(product__id, action){
    console.Log('User is logged in, sending data...')

    var url = '/updateItem/'
    fetch(url, {
       method: 'POST',
       headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
       },
       body:JSON.stringify({'product__id': pid, 'action':action})

    })
    .then((response)=>{
       return response.json();
    })
    .then((data)=>{
       location.reload()
    });
}
*/

//
//$("input[type='number']").change(function(event) {
//     var input = event.target;
//    if (isNaN(input.value) || input.value <= 0) {
//        input.value = 1;
//    }
//    updateCartTotal();
//});

if (document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}
function ready() {
    var removeCartItemButtons = document.getElementsByClassName('btn-danger');
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i];
        button.addEventListener('click', removeCartItem);
    }
    var quantityInputs = document.getElementsByClassName('cart-quantity-input');
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i];
        input.addEventListener('change', quantityChanged);
    }
    var addToCartButtons = document.getElementsByClassName('shop-item-button');
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i];
        button.addEventListener('click', addToCartClicked);
    }
   document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked);
}
function purchaseClicked() {
    //alert('Thank you for your purchase');
    var cartItems = document.getElementsByClassName('cart-items')[0];
    while (cartItems.hasChildNodes()) {
        cartItems.removeChild(cartItems.firstChild);
    }
    updateCartTotal();
}
function removeCartItem(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.parentElement.remove();
    var item_id = $(event.target.parentElement.parentElement.previousElementSibling).find("input")[0].id;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/remove_cart_item?id="+item_id, false);
    xhttp.send();
    window.location = "/cart"
//    updateCartTotal();
}

function quantityChanged(event) {
    var input = event.target;
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1;
    }
    updateCartTotal();
    var cid = event.target.id;
    var quant = event.target.value;
    var xhttp = new XMLHttpRequest();
    var url = "/change_quan?cid="+cid+"&quantity="+quant;
    xhttp.open("GET", url, false);
    xhttp.send();
}


function addToCartClicked(event) {
    var button = event.target;
    var shopItem = button.parentElement.parentElement;
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText;
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText;
    var imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src;
    addItemToCart(title, price, imageSrc);
    updateCartTotal();
}

function addItemToCart(title, price, imageSrc) {
    var cartRow = document.createElement('div');
    cartRow.classList.add('cart-row');
    var cartItems = document.getElementsByClassName('cart-items')[0];
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title');
    for (var i = 0; i < cartItemNames.length; i++) {
        if(cartItemNames[i].innerText == title){
            alert('This item is already added to the cart');
            return;
        }
    }
    var cartRowContents =`
        <div class="cart-item cart-column">
            <img class="cart-item-image" src="${imageSrc}" width="100" height="100">
            <span class="cart-item-title">${title}</span>
        </div>
        <span class="cart-price cart-column">${price}</span>
        <div class="cart-quantity cart-column">
            <input class="cart-quantity-input" type="number" value="1">
            <button class="btn btn-danger" type="button">REMOVE</button>
        </div>;
         <div class="cart-item cart-column">

				    <tr>
					  <td><span><img src="${imageSrc}" height="100" width="90" class="cart-item-image"></span></td>
					  <td><span style="color:black; margin-left:20px;" class="cart-item-title">${title}</span></td>
					  <td><span style="color:black; margin-left:20px;" class="cart_price cart-column">${price}</span></td>
					  <td style="margin:0px"><span style="color:black; margin-left:20px;">
						  <input type="number" value="{{store.quantity}}" style="width:40%" class="cart-quantity-input"></span></td>
					  <td><span><a href="" class="btn btn-primary purchase-button btn-danger" style="margin:0px; padding:4px">Remove</a></span></td>
				    </tr>
         </div>`;
    cartRow.innerHTML = cartRowContents;
    cartItems.append(cartRow);
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem);
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged);
}

function updateCartTotal() {
//    var cartItemContainer = document.getElementsByClassName('cart-items')[0];
//    var cartRows = cartItemContainer.getElementsByClassName('cart-row');
    var total = 0;
    var cartRows = document.querySelectorAll("tr");

    for (var i = 1; i < cartRows.length; i++) {
        var cartRow = cartRows[i];
        var value = parseInt($(cartRow).find("td span")[2].innerText);
        var quant = parseInt($(cartRow).find("td span input")[0].value);

        total += value*quant;

    }
    total = Math.round(total * 100)/100;
    document.querySelector(".cart-total span").innerText = 'RS.' + total;
}