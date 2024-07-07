// scripts.js
window.addEventListener('load', () => {
    const oceanSound = document.getElementById('ocean-sound');
    oceanSound.play().catch(error => {
        console.log('Auto-play failed:', error);
    });
});
