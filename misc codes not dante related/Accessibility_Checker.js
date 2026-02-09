// file: accessibility-fixes.js
document.addEventListener('DOMContentLoaded', function() {
  //
  // 1) SLIM HAMBURGER FIX
  //
  var ham = document.getElementById('slim-hamburger');
  if (ham) {
    ham.setAttribute('role', 'button');
    ham.setAttribute('tabindex', '0');

    var openLabel  = (ham.dataset.openAriaLabel  || '').trim();
    var closeLabel = (ham.dataset.closeAriaLabel || '').trim();

    ham.setAttribute('aria-expanded', 'false');
    ham.setAttribute('aria-label', openLabel);

    function toggleHamburger() {
      var expanded = ham.getAttribute('aria-expanded') === 'true';
      ham.setAttribute('aria-expanded', String(!expanded));
      ham.setAttribute('aria-label', expanded ? openLabel : closeLabel);
    }

    ham.addEventListener('click', toggleHamburger);
    ham.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        toggleHamburger();
      }
    });
  }

  //
  // 2) SEARCH FIELD LABEL FIX
  //
  var label = document.querySelector('label.sr-only[for="searchField"]');
  var input = document.getElementById('countrySearch');
  if (label && input) {
    label.setAttribute('for', input.id);
  }


  var submitBtn = document.querySelector('input.submit-search[type="submit"]');
  if (!submitBtn) return;

  // only set if it’s blank
  if (!submitBtn.value.trim()) {
    submitBtn.value = 'Search';
  }

  // if you’re using an icon-only button, also add an aria-label:
  if (!submitBtn.hasAttribute('aria-label')) {
    submitBtn.setAttribute('aria-label', 'Search our site');
  }
  


});
