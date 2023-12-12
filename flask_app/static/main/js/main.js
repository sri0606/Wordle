 function toggle_visibility() {
    var e = document.getElementById('feedback-main');
    if(e.style.display == 'block')
       e.style.display = 'none';
    else
       e.style.display = 'block';
 }

 function howToPlayClick() {
   // Update the display of the instructionsPopup div to be visible
   var instructionsPopup = document.getElementById('instructionsPopup');
   if (instructionsPopup) {
       instructionsPopup.style.display = 'flex';
   }
}

function closeInstructionsPopup() {
   // Update the display of the instructionsPopup div to be hidden
   var instructionsPopup = document.getElementById('instructionsPopup');
   if (instructionsPopup) {
       instructionsPopup.style.display = 'none';
   }
}

function playWordle(){
   window.location.href = "/login";
}

function signUp(){
   window.location.href = "/signup";
}

// Check if the instructions parameter is present that needs need be loaded once user signs up first time
const params = new URLSearchParams(window.location.search);
if (params.get('instructions') === 'true') {
   howToPlayClick();
}
