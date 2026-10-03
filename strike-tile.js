const buttons = Array.from(document.querySelectorAll('.option'));
const confirmButton = document.getElementById('confirm');
const status = document.getElementById('selectionStatus');
const chosen = { vertical: '', horizontal: '' };
buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const axis = button.dataset.axis;
    chosen[axis] = button.dataset.value;
    buttons.filter((item) => item.dataset.axis === axis).forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    confirmButton.disabled = !(chosen.vertical && chosen.horizontal);
    status.textContent = confirmButton.disabled ? 'Choose both contact points' : chosen.vertical + ' ' + chosen.horizontal.toLowerCase() + ' selected';
  });
});
confirmButton.addEventListener('click', () => {
  if (!chosen.vertical || !chosen.horizontal) return;
  status.textContent = 'Strike confirmed';
});