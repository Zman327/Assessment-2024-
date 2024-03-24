document.addEventListener('DOMContentLoaded', function () {
    var video = document.getElementById('video-background');
    // Slow down the video playback speed to 0.5 (adjust as needed)
    video.playbackRate = 0.5;
});

document.addEventListener("DOMContentLoaded", function () {
    const matches = document.querySelectorAll('.game-slider_col_item');
    const cycleMatchBtn = document.getElementById('cycle-match-btn');
    let currentMatchIndex = 0;

    cycleMatchBtn.addEventListener('click', function () {
        // Hide the current match
        matches[currentMatchIndex].style.display = 'none';
        // Increment the index to show the next match
        currentMatchIndex = (currentMatchIndex + 1) % matches.length;
        // Show the next match
        matches[currentMatchIndex].style.display = 'block';
    });
});

document.addEventListener("DOMContentLoaded", function() {
    renderCalendar();
});

function renderCalendar() {
    const tableBody = document.querySelector("#calendar tbody");
    tableBody.innerHTML = ""; // Clear previous content

    // Example: Generating a calendar for March 2024
    const year = 2024;
    const month = 2; // JavaScript months are zero-indexed, so 2 represents March

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDayOfMonth = new Date(year, month, 1).getDay(); // 0 for Sunday, 1 for Monday, etc.

    let date = 1;
    for (let i = 0; i < 6; i++) { // Maximum 6 weeks in a month
        const row = tableBody.insertRow();
        for (let j = 0; j < 7; j++) {
            const cell = row.insertCell();
            if (i === 0 && j < firstDayOfMonth) {
                cell.textContent = ""; // Empty cells before the start of the month
            } else if (date > daysInMonth) {
                break;
            } else {
                cell.textContent = date;
                date++;
            }
        }
    }
}


// JavaScript to toggle navbar transparency on scroll
window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.navbar');
    if (window.scrollY > 0) {
        navbar.classList.add('opaque');
        navbar.classList.remove('transparent');
    } else {
        navbar.classList.remove('opaque');
        navbar.classList.add('transparent');
    }
});

// Function to toggle dropdown
function toggleDropdown(element) {
    element.parentElement.classList.toggle('active');
}

// Function to highlight selected navigation item and animate the line
function highlightNavItem(element) {
    // Remove active class from all nav items
    const navItems = document.querySelectorAll('.menu a');
    navItems.forEach(item => {
        item.classList.remove('active');
    });

    // Add active class to the selected item
    element.classList.add('active');

    // Get the position of the selected item
    const navRect = element.getBoundingClientRect();

    // Update the width and left position of the line
    const line = document.querySelector('.line');
    line.style.width = navRect.width + 'px';
    line.style.left = navRect.left + 'px';
}
