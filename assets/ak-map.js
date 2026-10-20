(function () {
  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function loadLeaflet(root, done) {
    if (window.L) {
      done();
      return;
    }
    var css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = root + "assets/vendor/leaflet/leaflet.css";
    document.head.appendChild(css);
    var script = document.createElement("script");
    script.src = root + "assets/vendor/leaflet/leaflet.js";
    script.onload = done;
    document.body.appendChild(script);
  }

  var lineColor = {
    Purple: "#5c2d91",
    Green: "#0d7a3f",
    Yellow: "#a68400",
    Pink: "#b4235a",
    Blue: "#1d5fbf"
  };

  function strokeFor(feature) {
    var layer = feature.properties.layer;
    if (layer === "tank") return { color: "#1d4e6f", weight: 1, fillColor: "#3d7ea6", fillOpacity: 0.35 };
    if (layer === "tank-island") return { color: "#1d4e6f", weight: 1, fillColor: "#f7f4ee", fillOpacity: 0.9 };
    if (layer === "primary") return { color: "#0b3a66", weight: 2.4 };
    if (layer === "secondary") return { color: "#9a5b16", weight: 1.4 };
    if (layer === "primary-buffer") return { color: "#0b3a66", weight: 0, fillColor: "#0b3a66", fillOpacity: 0.16 };
    if (layer === "secondary-buffer") return { color: "#9a5b16", weight: 0, fillColor: "#c47b2b", fillOpacity: 0.14 };
    return { color: "#333", weight: 1 };
  }

  function markerFor(feature, latlng) {
    var props = feature.properties || {};
    var line = (props.line || "").split(",")[0].trim();
    var color = lineColor[line] || "#333";
    if (props.layer === "bbmp-lake") {
      return L.circleMarker(latlng, { radius: 5, color: "#145c38", weight: 1, fillColor: "#1f7a4d", fillOpacity: 0.95 });
    }
    if (props.layer === "uc") {
      return L.circleMarker(latlng, { radius: 6, color: color, weight: 2, fillColor: "#ffffff", fillOpacity: 1 });
    }
    return L.circleMarker(latlng, { radius: 6, color: "#ffffff", weight: 1, fillColor: color, fillOpacity: 0.95 });
  }

  function popupHtml(props) {
    var lines = [];
    if (props.name) lines.push("<strong>" + escapeHtml(props.name) + "</strong>");
    if (props.status) lines.push(escapeHtml(props.status));
    if (props.line) lines.push(escapeHtml(props.line));
    if (props.zone) lines.push("Zone: " + escapeHtml(props.zone));
    if (props.lulc) lines.push(escapeHtml(props.lulc));
    if (props.object_id) lines.push("Object " + escapeHtml(props.object_id));
    if (props.label) lines.push(escapeHtml(props.label));
    if (props.place_count != null && props.layer !== "bbmp-lake" && props.layer !== "tank") {
      lines.push(escapeHtml(props.place_count) + " OSM place nodes within 800 m. Names are in the table.");
    }
    return lines.join("<br>");
  }

  function draw(el) {
    var root = el.getAttribute("data-root") || "";
    var legendEl = document.getElementById(el.getAttribute("data-legend"));
    var legend = JSON.parse(legendEl.textContent);
    var map = L.map(el, { scrollWheelZoom: false });
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    fetch(el.getAttribute("data-geo"))
      .then(function (response) { return response.json(); })
      .then(function (collection) {
        var groups = {};
        legend.forEach(function (item) { groups[item.id] = L.layerGroup(); });
        var geo = L.geoJSON(collection, {
          style: strokeFor,
          pointToLayer: markerFor,
          onEachFeature: function (feature, layer) {
            var props = feature.properties || {};
            var html = popupHtml(props);
            if (html) layer.bindPopup(html);
            var group = groups[props.layer];
            if (group) group.addLayer(layer);
          }
        });
        var overlays = {};
        legend.forEach(function (item) {
          overlays[item.label] = groups[item.id];
          if (item.on !== false) groups[item.id].addTo(map);
        });
        L.control.layers(null, overlays, { collapsed: true }).addTo(map);
        if (geo.getBounds().isValid()) map.fitBounds(geo.getBounds(), { padding: [16, 16] });
      })
      .catch(function () {
        el.insertAdjacentHTML("afterend", "<p class=\"ak-map-note\">The map file did not load. The table on this page still lists the records.</p>");
      });
  }

  function boot(el) {
    var root = el.getAttribute("data-root") || "";
    var start = function () { loadLeaflet(root, function () { draw(el); }); };
    if (!("IntersectionObserver" in window)) {
      start();
      return;
    }
    var seen = false;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !seen) {
          seen = true;
          observer.disconnect();
          start();
        }
      });
    }, { rootMargin: "200px" });
    observer.observe(el);
  }

  document.querySelectorAll(".ak-map").forEach(boot);
})();
