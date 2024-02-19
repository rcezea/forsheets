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
        url: "/user", type: "GET", success: function (data) {
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
        url: "/user", type: "GET", success: function (data) {
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
})
