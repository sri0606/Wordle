//handler for menu button click
function OnClick() {
  const dropdown = document.getElementById("myDropdown");
  dropdown.classList.toggle("show");

  // If the dropdown is shown, and the window width becomes greater than 650px,
  // hide the dropdown again.
  if (window.innerWidth > 650 && dropdown.classList.contains("show")) {
    dropdown.classList.remove("show");
  }
}

//if screen is resized to width greater than 650px
document.addEventListener("DOMContentLoaded", function() {
  window.addEventListener("resize", function() {
    if (window.innerWidth > 650) {
      document.getElementById("myDropdown").classList.remove("show");
    }
  });
});

