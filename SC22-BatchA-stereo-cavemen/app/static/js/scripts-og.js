/*!
* Start Bootstrap - Grayscale v7.0.5 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});


//Slideshow Gallery JS
let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides")[0];
  let dots = document.getElementsByClassName("demo");
  let captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}

// model script

var which_model = "sp"; //sets default model to shakespeare
const linkButton = document.getElementById('a-btn');
linkButton.addEventListener("click", aToSubmit());

function aToSubmit()
{
    document.getElementById("sub-form").submit();
}

function grModel()
{
    //models.setAttribute(model,"gr");
    which_model = "gr";
    sendModel();
}

function dtModel()
{
    //models.setAttribute(model,"dt");
    which_model = "dt";
    sendModel();
}

function nkModel()
{
    //models.setAttribute(model,"nk");
    which_model = "nk";
    sendModel();
}

function spModel()
{
    //models.setAttribute(model,"sp");
    which_model = "sp";
    sendModel();
}

function sendModel()
{
    console.log(which_model);
    /*const request = new XMLHttpRequest();
    request.open("POST", `/get_model/${JSON.stringify(model_to_use)}`);
    request.send();*/
}

const grButton = document.getElementById('ramsay');
const dtButton = document.getElementById('trump');
const nkButton = document.getElementById('minaj');
const spButton = document.getElementById('shakespeare');

grButton.addEventListener("click", grModel());
dtButton.addEventListener("click", dtModel());
nkButton.addEventListener("click", nkModel());
spButton.addEventListener("click", spModel());

$.ajax({
url: Flask.url_for('generate_text'),
type: 'POST',
headers: {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
},
data: JSON.stringify(which_model),   // converts js value to JSON string
})
.done(function(result){     // on success get the return object from server
    console.log(result)     // do whatever with it. In this case see it in console
})