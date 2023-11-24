function toggleSettings() {
    var modal = document.getElementById("settingsModal");
    modal.style.display = modal.style.display === "none" ? "block" : "none";
}

function toggleVoiceGuidance() {
    // Toggle the state of voice guidance
    var voiceGuidanceToggle = document.getElementById("voiceGuidanceToggle");
    // Use this value to enable or disable voice guidance in your JavaScript logic
    var enableVoiceGuidance = voiceGuidanceToggle.checked;
    // You may want to save this setting in local storage or send it to the server

    // Close the settings modal
    toggleSettings();
}