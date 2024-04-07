var mapElement = document.getElementById('map');
mapboxgl.accessToken = mapElement.dataset.mapboxApiKey;
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

const marker = new mapboxgl.Marker() // initialize a new marker
            .setLngLat([-122.25948, 37.87221]) // Marker [lng, lat] coordinates
            .addTo(map); // Add the marker to the map

const geocoder = new MapboxGeocoder({
    // Initialize the geocoder
    accessToken: mapboxgl.accessToken, // Set the access token
    mapboxgl: mapboxgl, // Set the mapbox-gl instance
    marker: false, // Do not use the default marker style
    placeholder: 'Search for places in Berkeley' // Set the placeholder text
});

// Add the geocoder to the map
map.addControl(geocoder);

// Listen for the `result` event on the geocoder
geocoder.on('result', function(e) {
    // Access the coordinates from the result object
    var coordinates = e.result.geometry.coordinates;

    // Access the context from the result object
    var context = e.result.context;

    // Iterate over the context array
    for (var i = 0; i < context.length; i++) {
        // Check if the text field exists
        if (context[i].text) {
            // Save the text to local storage
            localStorage.setItem('location_text', context[i].text);
            break;
        }
    }

    // Retrieve the data from local storage
    var savedLocation = localStorage.getItem('location_text');

    // Set the innerHTML of the displayArea to the retrieved data
    document.getElementById('displayArea').innerHTML = savedLocation;

    // Send the location data to the server
    fetch('/update_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            location_text: savedLocation,
            coordinates: coordinates,
        }),
    });
});


// Update the navbar location when the page loads
window.onload = function() {
    // Retrieve the data from local storage
    var savedLocation = localStorage.getItem('location_text');

    // Check if savedLocation is not null
    if (savedLocation) {
        // Set the innerHTML of the navbarLocation span to the retrieved data
        document.getElementById('navbarLocation').innerHTML = savedLocation;

        // Print a message to the console
        console.log('Navbar location updated successfully');
    }
};