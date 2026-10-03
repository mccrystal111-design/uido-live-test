(() => {
  'use strict';

  // Behaviour layer: no presentation styles are set here.
  const root = document.querySelector('[data-wind-gauge]');
  if (!root) return;

  const strengths = ['1/2', '1', '2', '3'];
  const strengthButton = root.querySelector('[data-action="cycle-strength"]');
  const strengthValue = root.querySelector('[data-strength-value]');
  const status = root.querySelector('[data-status]');
  const directionButtons = [...root.querySelectorAll('[data-direction]')];

  const state = { direction: null, strength: strengths[0] };

  function publish() {
    strengthValue.textContent = state.strength;
    strengthButton.setAttribute(
      'aria-label',
      'Change wind strength. Current strength ' + state.strength + ' club' + (state.strength === '1/2' ? '' : 's')
    );

    const detail = { direction: state.direction, strength: state.strength };
    root.dispatchEvent(new CustomEvent('uido:wind-change', { bubbles: true, detail }));
    window.parent?.postMessage({ type: 'uido:wind-change', ...detail }, window.location.origin);
  }

  function cycleStrength() {
    const currentIndex = strengths.indexOf(state.strength);
    state.strength = strengths[(currentIndex + 1) % strengths.length];
    publish();
    status.textContent = 'Wind strength ' + state.strength + ' club' + (state.strength === '1/2' ? '' : 's');
  }

  function chooseDirection(button) {
    state.direction = button.dataset.direction;
    directionButtons.forEach(item => {
      const selected = item === button;
      item.setAttribute('aria-pressed', String(selected));
    });
    publish();
    status.textContent = 'Wind direction ' + state.direction + ', strength ' + state.strength + ' club' + (state.strength === '1/2' ? '' : 's');
  }

  // Native button click supports touch, mouse, keyboard, and assistive input.
  strengthButton.addEventListener('click', cycleStrength);
  directionButtons.forEach(button => button.addEventListener('click', () => chooseDirection(button)));

  root.querySelector('[data-action="yardages"]').addEventListener('click', () => {
    root.dispatchEvent(new CustomEvent('uido:wind-back', { bubbles: true }));
    window.parent?.postMessage({ type: 'uido:wind-back' }, window.location.origin);
  });

  publish();
})();