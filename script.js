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

function filterRankings() {
  const selectedWeapons = Array.from(document.querySelectorAll('#weaponSelector input:checked')).map(checkbox => checkbox.value);
  const selectedGenders = Array.from(document.querySelectorAll('#genderSelector input:checked')).map(checkbox => checkbox.value);
  const rows = document.querySelectorAll('#rankingsTable tbody tr');

  rows.forEach(row => {
      const rowWeapon = row.getAttribute('data-weapon');
      const rowGender = row.getAttribute('data-gender');
      const weaponMatch = selectedWeapons.length === 0 || selectedWeapons.includes(rowWeapon);
      const genderMatch = selectedGenders.length === 0 || selectedGenders.includes(rowGender);

      if (weaponMatch && genderMatch) {
          row.style.display = '';
      } else {
          row.style.display = 'none';
      }
  });
}

document.addEventListener("DOMContentLoaded", function() {
  renderCalendar();

  const monthSelector = document.getElementById("month");
  const yearSelector = document.getElementById("year");

  monthSelector.addEventListener("change", renderCalendar);
  yearSelector.addEventListener("change", renderCalendar);
});

function renderCalendar() {
  const tableBody = document.querySelector("#calendar tbody");
  tableBody.innerHTML = "";

  const month = parseInt(document.getElementById("month").value);
  const year = parseInt(document.getElementById("year").value);

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const firstDayOfMonth = new Date(year, month, 1).getDay();

  let date = 1;
  for (let i = 0; i < 6; i++) {
      const row = tableBody.insertRow();
      for (let j = 0; j < 7; j++) {
          const cell = row.insertCell();
          if (i === 0 && j < firstDayOfMonth) {
              cell.textContent = "";
          } else if (date > daysInMonth) {
              cell.textContent = "";
          } else {
              cell.textContent = date;
              date++;
          }
      }
  }
}
