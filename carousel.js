  // Get the carousel element
  var carousel = document.getElementById('carouselExampleIndicators');
  // Get the carousel inner element where the images will be added
  var carouselInner = carousel.querySelector('.carousel-inner');

  // Get the carousel indicators element where the bullets will be added
  var carouselIndicators = carousel.querySelector('.carousel-indicators');

    // Set the folder path where the images are stored
    var currentUrl = window.location.href;
    var folderPath = currentUrl.substring(0, currentUrl.lastIndexOf('/'));

    // Create an array to store the image paths
    var imagesArray = [];

    // Fetch the image files from the folder
    fetch(folderPath)
    .then((response) => {
        return response.text();
    })
    .then((data) => {
        // Create a new HTML document to parse the folder contents
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(data, "text/html");

        // Find all the <a> elements in the HTML document
        const links = htmlDoc.querySelectorAll("a");

        // Loop through each link and check if it is an image file
        for (let i = 0; i < links.length; i++) {
        const link = links[i];

        // Check if the link is an image file
        if (/\.(jpe?g|png|gif)$/i.test(link.href)) {
            // Add the image path to the imagesArray
            imagesArray.push(link.href);
        }
        }

        // Log the imagesArray to the console to verify
        console.log(imagesArray);
        addImageSlides(imagesArray);
    })
    .catch((error) => {
        console.error("Error fetching folder contents:", error);
    });

    function addImageSlides(images) {
        // Get the carousel element
        var carousel = document.getElementById('carouselExampleIndicators');
    
        // Get the carousel inner element where the images will be added
        var carouselInner = carousel.querySelector('.carousel-inner');
    
        // Loop through each image path and create a new slide
        for (var i = 0; i < images.length; i++) {
            // Create a new slide element
            var slide = document.createElement('div');
            slide.classList.add('carousel-item');
    
            // Create a new image element and set its attributes
            var image = document.createElement('img');
            image.classList.add('d-block');
            image.src = images[i];
            image.style.maxWidth = "500px";
            image.style.maxHeight = "500px";
    
            // Add the image to the slide and the slide to the carousel
            slide.appendChild(image);
            carouselInner.appendChild(slide);
        }
    
        // Set the first slide as active
        if(carouselInner.firstElementChild == null) return;
        carouselInner.firstElementChild.classList.add('active');
    }