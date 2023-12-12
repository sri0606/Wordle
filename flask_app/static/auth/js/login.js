let count = 0;

function checkCredentials() {
    // Get user input from form fields
    var email = $('#email').val();
    var password = $('#password').val();

    // Package data in a JSON object
    var data_d = {'email': email, 'password': password};

    // Send data to the server via jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success: function (returned_data) {
            returned_data = JSON.parse(returned_data);
            if (returned_data.success === 1) {
                // Authentication successful, redirect to home page
                window.location.href = "/home";
            } else {
                // Authentication failed, update failure message
                count++;
                $('#failureMessage').html('Authentication failed. Attempts: ' + count);
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}