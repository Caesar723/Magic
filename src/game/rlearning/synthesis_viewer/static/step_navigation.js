(() => {
  const navigators = [...document.querySelectorAll("[data-step-navigation]")];
  if (!navigators.length) return;

  const navigate = (url) => {
    if (url) window.location.assign(url);
  };

  navigators.forEach((navigator) => {
    const form = navigator.querySelector("[data-step-select-form]");
    const select = navigator.querySelector("[data-step-select]");
    if (!form || !select) return;

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      navigate(select.value);
    });
    select.addEventListener("change", () => navigate(select.value));
  });

  document.addEventListener("keydown", (event) => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    const target = event.target;
    if (
      target instanceof HTMLElement
      && (target.isContentEditable || /^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(target.tagName))
    ) {
      return;
    }

    const navigator = navigators[0];
    if (event.key === "[") {
      event.preventDefault();
      navigate(navigator.dataset.olderUrl);
    } else if (event.key === "]") {
      event.preventDefault();
      navigate(navigator.dataset.newerUrl);
    }
  });
})();
