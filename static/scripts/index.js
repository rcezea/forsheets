/**
 * Speech Recognition and Formula Conversion Script
 *
 * This script handles speech recognition and the conversion of text to formulas.
 * It utilizes Web Speech API for speech recognition and makes AJAX requests to the server
 * for converting and explaining formulas.
 *
 * Functions:
 * - `runSpeechRecog()`: Initiates speech recognition and updates the displayed text.
 * - Event Listener for the Enter Key with the text entry to generate formula.
 * - Event listener for the Microphone Button: Calls `runSpeechRecog()` when the button is clicked.
 * - Event listener for the Convert Button: Sends an AJAX request to convert the entered text to a formula.
 * - Event listener for the Explain Button: Sends an AJAX request to explain the generated formula.
 * - Event listener for the Copy Button: Copies the formula to the clipboard.
 *
 * Dependencies:
 * - jQuery is assumed to be available.
 *
 * Note:
 * - This script assumes the presence of HTML elements with IDs: entry, microphone-button, convert-button,
 *   explain-button, copy-button, result, home.
 */

//Action upon enter being pressed
const input = document.getElementById("entry");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("convert-button").click();
    }
});

// Define the runSpeechRecog function in the global scope
const runSpeechRecog = () => {
    $('entry').val('Loading text...');
    const output = document.getElementById('entry');
    const recognition = new webkitSpeechRecognition();
    recognition.onstart = () => {
        output.innerHTML = 'Listening...';
    };
    recognition.onresult = (e) => {
        output.innerHTML = e.results[0][0].transcript;
    };
    recognition.start();
};

// Event Listener for Microphone Button
$('#microphone-button').on('click', function () {
    // Call the global runSpeechRecog function
    runSpeechRecog();
});

// Conversion of text to formula
$("#convert-button").on("click", function (e) {

    $.ajax({
        url: "/user",
        type: "GET",
        success: function (data) {
            console.log("Session data:", data);
            if (data.session === false) {
                console.log("Redirecting to /home");
                window.location.href = "/home";
            }
        },
    });

    let input = $("#entry").val();
    if (input === '') {
        $("#result").val("Please enter text");
        return;
    }else {
        $("#result").val("Loading...");
    }

    let url = `/formula?user_input=${encodeURIComponent(input)}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            $("#result").val(data);
            $("#explain-button").show();
            $("#copy-button").show();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    e.preventDefault();
});

// Explaining the formula
$("#explain-button").on("click", function (e) {

    $.ajax({
        url: "/user",
        type: "GET",
        success: function (data) {
            console.log("Session data:", data);
            if (data.session === false) {
                console.log("Redirecting to /home");
                window.location.href = "/home";
            }
        },
    });

    let input = $("#result").val();
    if (input === "Please enter text") {
        $("#result").val("Last warning");
        return;
    }
    if (input === "Last warning") {
        alert("You've been suspended. Visit Registry in 15mins");
        return;
    }
    let url = `/explain?user_input=${(input)}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            let output = input + '\n\n' + data;
            $("#explain-button").hide();
            $("#copy-button").hide();
            $("#result").val(output);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    e.preventDefault();
});

// copy function
$("#copy-button").on("click", function () {
    let formula = $("#result").val();
    navigator.clipboard.writeText(formula).then(() => {
        alert('Content copied to clipboard');
    });
});
