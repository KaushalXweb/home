document.addEventListener("DOMContentLoaded", function() {
    showPage("loginPage");
});

// Function to show a specific page and hide others
function showPage(pageId) {
    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active"); // Remove active class from all pages
    });
    document.getElementById(pageId).classList.add("active"); // Add active class to the selected page
}

// Login function
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();
    const errorElement = document.getElementById("loginError"); // Add an element in your HTML to display errors

    if (username && password) {
        // In a real application, you would send this data to a server for authentication.
        // For this example, we'll just simulate a successful login.
        errorElement.textContent = ""; // Clear any previous errors
        showPage("resumePage");
    } else {
        errorElement.textContent = "Please enter a valid username or email and password.";
    }
});

// Resume Upload / Skills Submission
document.getElementById("skillsForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const skills = document.getElementById("skills").value;
    const resumeFile = document.getElementById("resume").files;
    const errorElement = document.getElementById("resumeError"); // Add an element in your HTML to display errors

    if (skills || resumeFile.length > 0) {
        errorElement.textContent = ""; // Clear any previous errors
        alert("Submission successful!");
        showPage("dashboardPage");
    } else {
        errorElement.textContent = "Please enter skills or upload a resume.";
    }
});
