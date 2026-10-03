const options = Array.from(document.querySelectorAll('.option'));
let completed = false;
options.forEach((button) => {
  button.addEventListener('click', () => {
    if (completed) return;
    completed = true;
    const value = button.dataset.value;
    window.dispatchEvent(new CustomEvent('uido:trajectory-selected', { detail: { value: value } }));
    if (window.parent !== window) {
      window.parent.postMessage({ type: 'uido:trajectory-selected', value: value }, window.location.origin);
    } else {
      document.querySelector('header p').textContent = value + ' selected';
      completed = false;
    }
  });
});