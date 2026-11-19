(() => {
  const dropdowns = () => Array.from(document.querySelectorAll("details[data-dropdown]"));

  const closeAll = (except = null) => {
    for (const el of dropdowns()) {
      if (el !== except && el.open) {
        el.open = false;
      }
    }
  };

  const filterCategories = (input) => {
    const menu = input.closest(".feed-menu");
    if (!menu) {
      return;
    }
    const query = input.value.trim().toLocaleLowerCase("pl");
    const items = menu.querySelectorAll("[data-category-list] .feed-menu__item");
    let visibleCount = 0;
    for (const item of items) {
      const text = item.textContent.trim().toLocaleLowerCase("pl");
      const matches = !query || text.includes(query);
      item.hidden = !matches;
      if (matches) {
        visibleCount += 1;
      }
    }
    const empty = menu.querySelector("[data-category-empty]");
    if (empty instanceof HTMLElement) {
      empty.hidden = visibleCount > 0;
    }
  };

  document.addEventListener("toggle", (event) => {
    const target = event.target;
    if (target instanceof HTMLDetailsElement && target.matches("details[data-dropdown]") && target.open) {
      closeAll(target);
      const filterInput = target.querySelector("[data-category-filter]");
      if (filterInput instanceof HTMLInputElement) {
        filterInput.value = "";
        filterCategories(filterInput);
        filterInput.focus({ preventScroll: true });
      }
    }
  }, true);

  document.addEventListener("input", (event) => {
    const target = event.target;
    if (target instanceof HTMLInputElement && target.matches("[data-category-filter]")) {
      filterCategories(target);
    }
  });

  document.addEventListener("keydown", (event) => {
    const target = event.target;
    if (
      event.key === "Enter"
      && target instanceof HTMLInputElement
      && target.matches("[data-category-filter]")
    ) {
      const menu = target.closest(".feed-menu");
      const firstVisible = menu?.querySelector("[data-category-list] .feed-menu__item:not([hidden])");
      if (firstVisible instanceof HTMLAnchorElement) {
        event.preventDefault();
        firstVisible.click();
      }
    }
  });

  document.addEventListener("click", (event) => {
    for (const el of dropdowns()) {
      if (el.open && !el.contains(event.target)) {
        el.open = false;
      }
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    for (const el of dropdowns()) {
      if (el.open) {
        el.open = false;
        const summary = el.querySelector("summary");
        if (summary instanceof HTMLElement) {
          summary.focus();
        }
      }
    }
  });
})();
