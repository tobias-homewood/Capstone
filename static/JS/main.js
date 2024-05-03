// Wait for the document to be ready
$(function () {
    // Function to convert inches to feet and inches
    function convertToFeetInches(inches) {
        if (isNaN(inches)) return "";
        var feet = Math.floor(inches / 12);
        var remainingInches = inches % 12;
        return (feet ? feet + "'" : "") + " " + remainingInches + '"';
    }

    // Function to convert a decimal number to inches with fraction
    function convertToInchesWithFraction(value) {
        if (isNaN(value)) return "";
        var wholeNumber = Math.floor(value);
        var fraction = value - wholeNumber;
        var fractionInSixteenths = Math.round(fraction * 16);

        if (fractionInSixteenths === 0) {
            return wholeNumber + '"';
        } else {
            return wholeNumber + " " + fractionInSixteenths + '/16"';
        }
    }

    // Initialize length slider
    var minLength = $("#length-slider").data("min-length");
    minLength =
        minLength === undefined || isNaN(minLength) || minLength === ""
            ? 0
            : minLength;
    var maxLength = $("#length-slider").data("max-length");
    maxLength =
        maxLength === undefined || isNaN(maxLength) || maxLength === ""
            ? 0
            : maxLength;

    $("#length-slider").slider({
        range: true,
        min: 0,
        max: 180,
        values: [minLength, maxLength],
        slide: function (event, ui) {
            $("#min-length").val(ui.values[0]);
            $("#max-length").val(ui.values[1]);
            $("#length-value").text(
                "Length: " +
                    convertToFeetInches(ui.values[0]) +
                    " - " +
                    convertToFeetInches(ui.values[1])
            );
        },
    });
    $("#length-value").text(
        "Length: " +
            convertToFeetInches(minLength) +
            " - " +
            convertToFeetInches(maxLength)
    );

    // Initialize price slider
    var minPrice = $("#price-slider").data("min-price");
    minPrice =
        minPrice === undefined || isNaN(minPrice) || minPrice === ""
            ? 0
            : minPrice;
    var maxPrice = $("#price-slider").data("max-price");
    maxPrice =
        maxPrice === undefined || isNaN(maxPrice) || maxPrice === ""
            ? 0
            : maxPrice;

    $("#price-slider").slider({
        range: true,
        min: 0,
        max: 2000,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            $("#min-price").val(ui.values[0]);
            $("#max-price").val(ui.values[1]);
            $("#price-value").text(
                "Price: €" + ui.values[0] + " - €" + ui.values[1]
            );
        },
    });
    $("#price-value").text("Price: €" + minPrice + " - €" + maxPrice);

    // Initialize width slider
    var minWidth = $("#width-slider").data("min-width");
    minWidth =
        minWidth === undefined || isNaN(minWidth) || minWidth === ""
            ? 0
            : Math.round(minWidth * 16);
    var maxWidth = $("#width-slider").data("max-width");
    maxWidth =
        maxWidth === undefined || isNaN(maxWidth) || maxWidth === ""
            ? 0
            : Math.round(maxWidth * 16);

    $("#width-slider").slider({
        range: true,
        min: 0 * 16,
        max: 30 * 16,
        step: 1,
        values: [minWidth, maxWidth],
        slide: function (event, ui) {
            var minValue = ui.values[0] / 16;
            var maxValue = ui.values[1] / 16;

            $("#min-width").val(minValue);
            $("#max-width").val(maxValue);
            $("#width-value").text(
                "Width: " +
                    convertToInchesWithFraction(minValue) +
                    " - " +
                    convertToInchesWithFraction(maxValue)
            );
        },
    });
    $("#width-value").text(
        "Width: " +
            convertToInchesWithFraction(minWidth / 16) +
            " - " +
            convertToInchesWithFraction(maxWidth / 16)
    );

    // Initialize depth slider
    var minDepth = $("#depth-slider").data("min-depth");
    minDepth =
        minDepth === undefined || isNaN(minDepth) || minDepth === ""
            ? 0
            : Math.round(minDepth * 16);
    var maxDepth = $("#depth-slider").data("max-depth");
    maxDepth =
        maxDepth === undefined || isNaN(maxDepth) || maxDepth === ""
            ? 0
            : Math.round(maxDepth * 16);

    $("#depth-slider").slider({
        range: true,
        min: 0 * 16,
        max: 5 * 16,
        step: 1,
        values: [minDepth, maxDepth],
        slide: function (event, ui) {
            var minValue = ui.values[0] / 16;
            var maxValue = ui.values[1] / 16;

            $("#min-depth").val(minValue);
            $("#max-depth").val(maxValue);
            $("#depth-value").text(
                "Depth: " +
                    convertToInchesWithFraction(minValue) +
                    " - " +
                    convertToInchesWithFraction(maxValue)
            );
        },
    });
    $("#depth-value").text(
        "Depth: " +
            convertToInchesWithFraction(minDepth / 16) +
            " - " +
            convertToInchesWithFraction(maxDepth / 16)
    );

    // Initialize volume slider
    var minVolume = $("#volume-slider").data("min-volume");
    minVolume =
        minVolume === undefined || isNaN(minVolume) || minVolume === ""
            ? 0
            : minVolume;
    var maxVolume = $("#volume-slider").data("max-volume");
    maxVolume =
        maxVolume === undefined || isNaN(maxVolume) || maxVolume === ""
            ? 0
            : maxVolume;

    $("#volume-slider").slider({
        range: true,
        min: 0,
        max: 100,
        values: [minVolume, maxVolume],
        slide: function (event, ui) {
            $("#min-volume").val(ui.values[0]);
            $("#max-volume").val(ui.values[1]);
            $("#volume-value").text(
                "Volume: " + ui.values[0] + " - " + ui.values[1]
            );
        },
    });
    $("#volume-value").text("Volume: " + minVolume + " - " + maxVolume);
});

// Handle form submission for favourite form
$(document).ready(function () {
    $(document).on("submit", ".favourite-form", function (e) {
        e.preventDefault(); // prevent the form from being submitted
        var form = $(this);
        var url = form.attr("action");
        var heartIcon = form.find(".bi"); // moved this line up here

        // Check if user is logged in
        var userLoggedIn = $("body").attr("data-user-logged-in") === "True";
        if (!userLoggedIn) {
            var currentUrl = encodeURIComponent(window.location.href);
            window.location.href = "/login?next=" + currentUrl + "&message=You need to be logged in to favourite a board";
            return; // stop execution if user is not logged in
        }

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements
            success: function (data) {
                if (window.location.pathname.includes("/user/")) {
                    // If on user_profile page, remove the board
                    form.closest("li").remove();
                } else {
                    // If on search_boards page, toggle the heart color and fill
                    heartIcon.toggleClass("bi-heart bi-heart-fill text-red");
                }
            },
            statusCode: {
                302: function() {
                    // If the response is a redirect, redirect to login page
                    var currentUrl = encodeURIComponent(window.location.href);
                    window.location.href = "/login?next=" + currentUrl + "&message=You need to be logged in to favourite a board";
                    heartIcon.removeClass("bi-heart bi-heart-fill text-red"); // remove the classes that change the color
                }
            }
        });
    });
});
    // Handle the reset button click event
    $('#reset-button').click(function() {
        // Retrieve the board location from local storage
        var currentBoardLocation = localStorage.getItem("coordinates");
        // Reset the sliders
        $("#length-slider").slider("values", [0, 180]);
        $("#min-length").val(0);
        $("#max-length").val(180);

        $("#price-slider").slider("values", [0, 2000]);
        $("#min-price").val(0);
        $("#max-price").val(2000);

        $("#width-slider").slider("values", [0, 30 * 16]);
        $("#min-width").val(0);
        $("#max-width").val(30);

        $("#depth-slider").slider("values", [0, 5 * 16]);
        $("#min-depth").val(0);
        $("#max-depth").val(5);

        $("#volume-slider").slider("values", [0, 100]);
        $("#min-volume").val(0);
        $("#max-volume").val(100);

        // Reset the slider labels
        $("#length-value").text("Length: 0\" - 15' 0\"");
        $("#price-value").text("Price: €0 - €2000");
        $("#width-value").text("Width: 0\" - 30\"");
        $("#depth-value").text("Depth: 0\" - 5\"");
        $("#volume-value").text("Volume: 0 - 100");

        // Reset the other inputs
        $("#sell_or_rent").prop('selectedIndex', 0);
        $("#board_manufacturer").val('');
        $("#model").val('');
        $("#condition").prop('selectedIndex', 0);
        $("#delivery_options").prop('selectedIndex', 0);
        $("#min-price").val('');
        $("#max-price").val('');
    });
// This block of code is responsible for handling the click event on the filters element.
// When the filters element is clicked, the display style of the filter-form is toggled between 'none' and 'block'.
document.addEventListener("DOMContentLoaded", (event) => {
    var filtersElement = document.getElementById("filters");
    if (filtersElement) {
        filtersElement.addEventListener("click", function () {
            var form = document.getElementById("filter-form");
            if (form.style.display === "none") {
                form.style.display = "block";
            } else {
                form.style.display = "none";
            }
        });
    }
});

document.querySelectorAll('.board-image-container').forEach(function(element) {
    element.addEventListener('click', function() {
        var url = this.getAttribute('data-url');
        window.location.href = url;
    });
});

$(document).ready(function() {
    // Attach a click event handler to the heart icon
    $(".favourite-form button, #delete-board-temp button").on("click", function(e) {
        e.stopPropagation();  // Stop the event from propagating up to the board-image-container
    });
});