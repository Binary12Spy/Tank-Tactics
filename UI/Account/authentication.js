function authenticate() {
    // Get the form input values
    var username = $("#typeUsernameX").val();
    var password = $("#typePasswordX").val();

    // Create the JSON payload
    var payload = {
        username: username,
        password: password
    };

    $.ajax({
        url: '/authenticate',
        method: 'POST',
        data: JSON.stringify(payload), // Convert payload to JSON string
        contentType: 'application/json', // Set content type to JSON
        success: function (response) {
            
        },
        error: function (error) {
            $('#errorToast').toast("show");
        }
    });
}