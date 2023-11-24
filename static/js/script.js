document.addEventListener("DOMContentLoaded", function () {
    const toggleSidebar = document.querySelector('.toggle-sidebar');
    const settingsContainer = document.querySelector('.settings');
    const toggleSettings = document.querySelector('.toggle-settings');
    const voiceToggle = document.getElementById('voiceToggle');

    toggleSidebar.addEventListener('click', function () {
        settingsContainer.classList.toggle('show');
    });

    toggleSettings.addEventListener('click', function () {
        voiceToggle.checked = false; // Reset the toggle when settings are opened
        settingsContainer.classList.toggle('show-accessibility');
    });

    voiceToggle.addEventListener('change', function () {
        // Implement your logic for voice guidance here
        if (voiceToggle.checked) {
            // Voice guidance turned ON
            console.log('Voice Guidance ON');
        } else {
            // Voice guidance turned OFF
            console.log('Voice Guidance OFF');
        }
    });
});
