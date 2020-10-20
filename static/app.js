// Navigate product images 

const BigImage = document.getElementById('big-image');




// Navigate information 

const chooseInfo = document.getElementById('more-infos');
const choose = document.getElementsByClassName('choose');
const paragraph = document.getElementsByClassName('paragraph');


function styleItem (a,b,c) {
    a.style.cssText = 'color:black ; border-bottom: 2px solid black ; padding-bottom: 6px';
    b.style.cssText = 'color:gray ; border-bottom: none';
}

function displayPrph (e,f,g) {
        e.style.display = 'block';
        f.style.display = 'none';
}

chooseInfo.addEventListener('click', event => {
   
       if (event.target === choose[0]) {    
           
                 styleItem (choose[0],choose[1])
                 displayPrph (paragraph[0],paragraph[1])
        }  

       else {  

                 styleItem (choose[1],choose[0])
                 displayPrph (paragraph[1],paragraph[0])
        }  

});

// add items to the cart

const addToCart = document.getElementById('add-to-cart');
const itemsAdded = document.getElementById('items-added');
const counter = document.getElementById('counter');

addToCart.addEventListener('click',ev => itemsAdded.textContent = (counter.value));