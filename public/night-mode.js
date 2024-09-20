const toggleModeButton = document.getElementById('toggleModeButton');
const body = document.body;

toggleModeButton.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
});