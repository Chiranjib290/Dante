// file: fix-territory-toggle.js
;(function(){
  function initToggle() {
    var dialog = document.getElementById('lst-territory-selector');
    var btn    = document.querySelector('button[tabindex="6"]');
    if (!dialog || !btn) return false;

    // 1) give a stable ID
    if (!btn.id) btn.id = 'territory-selector-toggle';

    // 2) link the button to the dialog
    btn.setAttribute('aria-controls', dialog.id);

    // 3) capture your open/close labels
    var openLabel  = btn.getAttribute('aria-label').trim();
    var closeLabel = btn.dataset.closeAriaLabel
                     ? btn.dataset.closeAriaLabel.trim()
                     : openLabel.replace(/Find|Select/, 'Close');

    // 4) sync function based on actual visibility
    function syncState() {
      var isOpen = window.getComputedStyle(dialog).display !== 'none';
      btn.setAttribute('aria-expanded', String(isOpen));
      btn.setAttribute('aria-label', isOpen ? closeLabel : openLabel);
    }

    // initial sync
    syncState();

    // 5) watch for show/hide via class/style changes
    new MutationObserver(syncState)
      .observe(dialog, { attributes: true, attributeFilter: ['style','class'] });

    // 6) also sync right after the user clicks (UI may toggle it)
    btn.addEventListener('click', function() {
      setTimeout(syncState, 0);
    });

    return true;
  }

  // try immediately, else watch for DOM insertion
  if (!initToggle()) {
    new MutationObserver(function(m, obs) {
      if (initToggle()) obs.disconnect();
    }).observe(document.body, { childList: true, subtree: true });
  }
})();
