// Get the CSRF token from the meta tag
var csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Get the map element from the DOM
var mapElement = document.getElementById("map");

// Set the Mapbox access token from the data attribute of the map element
mapboxgl.accessToken = mapElement.dataset.mapboxApiKey;

// Retrieve the coordinates from local storage
var savedCoordinates = localStorage.getItem("coordinates");

// Parse the coordinates or use default values if they are not available
var coordinates = savedCoordinates ? JSON.parse(savedCoordinates) : [-74.5, 40];

var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v12",
    center: coordinates, // Use the coordinates from local storage
    zoom: 9,
});

// Add an event listener for the 'moveend' event on the map
map.on('moveend', function() {
    // Get the new center of the map after it has been moved
    var newCenter = map.getCenter();

    // Format the coordinates of the new center as an array
    var formattedCoordinates = [newCenter.lng, newCenter.lat];

    // Update the 'board_location_coordinates' form field with the new coordinates
    var boardLocationElement = document.getElementById('board_location_coordinates');
    if(boardLocationElement) {
        boardLocationElement.value = JSON.stringify(formattedCoordinates);
    }
});

// Initialize a new marker and add it to the map
const marker = new mapboxgl.Marker() // initialize a new marker
    .setLngLat([-122.25948, 37.87221]) // Set the position of the marker [lng, lat]
    .addTo(map); // Add the marker to the map

// Initialize a new Mapbox geocoder
const geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken, // Set the access token for the geocoder
    mapboxgl: mapboxgl, // Set the mapbox-gl instance for the geocoder
    marker: false, // Do not use the default marker style
    placeholder: "Search for boards in...", // Set the placeholder text for the geocoder input
});

// Add the geocoder control to the map
map.addControl(geocoder);

// Add an event listener for the 'result' event on the geocoder
geocoder.on("result", function (e) {
    // Get the coordinates from the result object
    var coordinates = e.result.geometry.coordinates;

    // Get the text from the result object
    var context = e.result.text;

    // If the text field exists, save it to local storage
    if (context) {
        localStorage.setItem("location_text", context);
    }

    // Save the coordinates to local storage
    localStorage.setItem("coordinates", JSON.stringify(coordinates));

    // Retrieve the saved location and coordinates from local storage
    var savedLocation = localStorage.getItem("location_text");
    var savedCoordinates = localStorage.getItem("coordinates");

    // Update the 'navbarLocation' element with the saved location
    document.getElementById("navbarLocation").innerHTML = savedLocation;

    // Send a POST request to the '/update_location' endpoint with the saved location and coordinates
    $.ajax({
        url: '/update_location',
        method: 'POST',
        contentType: 'application/json',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: JSON.stringify({
            location_text: savedLocation,
            coordinates: JSON.parse(savedCoordinates),
        }),
        dataType: 'json',
        success: function(data) {
            console.log('Success:', data);
        },
        error: function(error) {
            console.error('Error:', error);
        },
    });
});

window.onload = function () {
    var savedLocation = localStorage.getItem("location_text");
    var savedCoordinates = localStorage.getItem("coordinates");

    if (savedLocation && savedCoordinates) {
        var navbarLocation = document.getElementById("navbarLocation");
        var boardLocation = document.getElementById('board_location_coordinates');

        if (navbarLocation) {
            navbarLocation.innerHTML = savedLocation;
        }

        if (boardLocation) {
            boardLocation.value = savedCoordinates;
        }

        $.ajax({
            url: '/update_location',
            method: 'POST',
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": csrf_token
            },
            data: JSON.stringify({
                location_text: savedLocation,
                coordinates: JSON.parse(savedCoordinates),
            }),
            dataType: 'json',
            success: function(data) {
                console.log('Success:', data);
            },
            error: function(error) {
                console.error('Error:', error);
            },
        });
    }
};

$(document).ready(function () {
    // Determine if the current page is the homepage
    var isHomepage = $('h5').is('#homepage-instructions');

    // Get the saved location text from local storage
    var locationText = localStorage.getItem("location_text");

    // If on the homepage, make the map visible
    if (isHomepage) {
        $("#mapWrapper").css({"max-height": "300px", "opacity": "1"});
        
        // If a location is saved, display it
        if (locationText) {
            $("#locationText").text("Your location is currently set to " + locationText + ". Please choose an option below.");
        } 
        // If no location is saved, display a default message
        else {
            $("#locationText").text("Start by entering your location above and then choose an option below.");
        }
    }

    // Add event listeners for the 'hide.bs.collapse' and 'show.bs.collapse' events on the 'mapContainer' element
    $("#mapContainer").on({
        "hide.bs.collapse": function () {
            // When the 'mapContainer' element is collapsed, hide the 'mapWrapper' element
            $("#mapWrapper").css({"max-height": "0", "opacity": "0"});
        },
        "show.bs.collapse": function () {
            // When the 'mapContainer' element is expanded, show the 'mapWrapper' element
            $("#mapWrapper").css({"max-height": "300px", "opacity": "1"});
        },
    });
});