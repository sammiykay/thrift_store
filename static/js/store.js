function tog(){
    let x = document.querySelector('.link2');
    let y = document.querySelector('.burg1');
    let b = document.querySelector('.burg2');
    let a = document.querySelector('.burg3');
    x.classList.toggle('toggle');
    y.classList.toggle('tog');
    a.classList.toggle('tog');
    b.classList.toggle('tog');
}

var updateBtns = document.getElementsByClassName('update-cart');
for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if (user == 'AnonymousUser'){
            alert('You need to login to use this feature');
            console.log('User is not authenticated');
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data..');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        if (data == 'Out of stock') {
            showAlert();
        } else {
            // Update the cart quantity displayed on the page
            const itemQuantity = document.querySelector('#item_quantity');
            const cartTotal = document.querySelector('#cart-badge');
            const cartTotalElements = document.getElementsByClassName('cart_total');
            
            

            // Optionally, update the number of items in the cart badge
            cartTotal.innerText = data.cart_total;
            const cartBadge = document.querySelector('#cart-badge');
            cartBadge.innerText = data.cart_items_count;
            itemQuantity.innerText = data.item_quantity;
            showAlert2();
            // Show a success alert when an item is added/removed
            // if (action == 'add') {
            //     showAlert('Item added to cart!', 'success');
            // } else if (action == 'remove') {
            //     showAlert('Item removed from cart!', 'warning');
            // }
        }
    });
}
function showAlert() {
    console.log('dd')
    document.getElementById('alert').style.display = 'block';
    // Automatically remove the alert after 3 seconds
    setTimeout(() => {
        
        setTimeout(() => document.getElementById('alert').style.display = 'none', 500); // Wait for fade-out transition
    }, 3000);
}


function showAlert2() {
    console.log('dd')
    document.getElementById('alert2').style.display = 'block';
    // Automatically remove the alert after 3 seconds
    setTimeout(() => {
        
        setTimeout(() => document.getElementById('alert2').style.display = 'none', 500); // Wait for fade-out transition
    }, 3000);
}
