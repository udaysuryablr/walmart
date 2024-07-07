// scripts.js
window.addEventListener('load', () => {
    const oceanSound = document.getElementById('ocean-sound');
    const toggleButton = document.getElementById('toggle-music');

    oceanSound.play().catch(error => {
        console.log('Auto-play failed:', error);
    });

    toggleButton.addEventListener('click', () => {
        if (oceanSound.paused) {
            oceanSound.play();
            toggleButton.innerHTML = '<i class="fas fa-volume-up"></i> Pause Music';
        } else {
            oceanSound.pause();
            toggleButton.innerHTML = '<i class="fas fa-volume-mute"></i> Play Music';
        }
    });
});
