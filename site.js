(function () {
  var progress = document.getElementById("scroll-progress-bar");
  if (progress) {
    var onScroll = function () {
      var doc = document.documentElement;
      var height = doc.scrollHeight - doc.clientHeight;
      var ratio = height > 0 ? (window.scrollY / height) * 100 : 0;
      progress.style.width = ratio + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest(".faq-trigger");
    if (!button) return;
    var item = button.closest(".faq-item");
    if (!item) return;
    var open = item.classList.toggle("open");
    button.setAttribute("aria-expanded", open ? "true" : "false");
  });

  var copyButtons = document.querySelectorAll("[data-copy-link]");
  copyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var done = function () {
        var original = button.getAttribute("title") || "Copy article link";
        button.setAttribute("title", "Link copied");
        button.style.color = "#804526";
        window.setTimeout(function () {
          button.setAttribute("title", original);
          button.style.color = "";
        }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(window.location.href).then(done).catch(function () {});
      }
    });
  });

  var grid = document.getElementById("blogGrid");
  if (!grid) return;

  var activePillar = "all";
  var buttons = document.querySelectorAll(".cat-btn");
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".blog-card"));
  var noResults = document.getElementById("noResults");
  var resultCount = document.getElementById("resultCount");
  var searchInput = document.getElementById("blogSearchInput");

  function applyFilter() {
    var query = (searchInput && searchInput.value ? searchInput.value : "").trim().toLowerCase();
    var visible = 0;
    cards.forEach(function (card) {
      var pillar = card.getAttribute("data-pillar") || card.getAttribute("data-section") || "";
      var haystack = card.getAttribute("data-search") || "";
      var matchesPillar = activePillar === "all" || pillar === activePillar;
      var matchesQuery = !query || haystack.indexOf(query) !== -1;
      var show = matchesPillar && matchesQuery;
      card.style.display = show ? "flex" : "none";
      if (show) visible += 1;
    });
    if (noResults) noResults.style.display = visible === 0 ? "block" : "none";
    if (resultCount) {
      var noun = visible === 1 ? "guide" : "guides";
      resultCount.textContent = "Showing " + visible + " " + noun;
    }
  }

  function setPillar(pillar, button) {
    activePillar = pillar;
    buttons.forEach(function (btn) {
      var on = btn === button;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    applyFilter();
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      if (button.tagName === "A" && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
        event.preventDefault();
      }
      var pillar = button.getAttribute("data-pillar") || button.getAttribute("data-section") || "all";
      setPillar(pillar, button);
      var next = pillar === "all" ? "" : "#" + pillar;
      if (history.replaceState) {
        history.replaceState(null, "", pillar === "all" ? location.pathname + location.search : next);
      } else if (pillar !== "all") {
        location.hash = next;
      }
    });
  });

  var initial = (location.hash || "").replace("#", "");
  if (initial) {
    var match = document.querySelector('.cat-btn[data-pillar="' + initial + '"], .cat-btn[data-section="' + initial + '"]');
    if (match) {
      setPillar(initial, match);
    } else {
      applyFilter();
    }
  } else {
    applyFilter();
  }

  var clearBtn = document.getElementById("searchClearBtn");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      if (clearBtn) clearBtn.hidden = !searchInput.value;
      applyFilter();
    });
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        searchInput.value = "";
        clearBtn.hidden = true;
        searchInput.focus();
        applyFilter();
      });
    }
  }
})();
