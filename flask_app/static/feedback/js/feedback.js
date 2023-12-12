document.addEventListener("DOMContentLoaded", function () {
    const feedbackForm = document.getElementById("feedback-form");
    const feedbackToggle = document.getElementById("feedback-toggle");

    // Initially, hide the feedback form
    feedbackForm.style.display = "none";

    // Toggle the feedback form when the button is clicked
    feedbackToggle.addEventListener("click", function () {
        if (feedbackForm.style.display === "none") {
            feedbackForm.style.display = "block";
        } else {
            feedbackForm.style.display = "none";
        }
    });
});
