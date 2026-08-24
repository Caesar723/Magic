(() => {
  const dataElement = document.getElementById("text-embedding-points-data");
  const svg = document.getElementById("text-embedding-plot");
  if (!dataElement || !svg) return;

  const points = JSON.parse(dataElement.textContent || "[]");
  const tooltip = document.getElementById("text-embedding-tooltip");
  const showQueriesToggle = document.getElementById("text-query-toggle");
  const filterElement = document.getElementById("binding-effect-filter");
  const legend = document.getElementById("binding-legend");
  const namespace = "http://www.w3.org/2000/svg";
  const width = 1000;
  const height = 640;
  const padding = 42;
  const selectedEffects = new Set();

  const values = (key) => points.map((point) => Number(point[key]) || 0);
  const extent = (items) => {
    const minimum = Math.min(...items);
    const maximum = Math.max(...items);
    return minimum === maximum ? [minimum - 1, maximum + 1] : [minimum, maximum];
  };
  const [xMin, xMax] = extent(values("x"));
  const [yMin, yMax] = extent(values("y"));
  const scaleX = (value) => padding + ((value - xMin) / (xMax - xMin)) * (width - padding * 2);
  const scaleY = (value) => height - padding - ((value - yMin) / (yMax - yMin)) * (height - padding * 2);
  const hash = (text) => [...String(text)].reduce((value, character) => ((value * 31) + character.charCodeAt(0)) >>> 0, 7);
  const bindingPalette = [
    "#e76f51", "#f4a261", "#e9c46a", "#90be6d", "#43aa8b", "#4d908e",
    "#577590", "#5773c8", "#7b68ee", "#9d4edd", "#c77dff", "#d65db1",
    "#ef476f", "#ff9f1c", "#8ac926", "#00b4d8", "#4895ef", "#b8c0ff",
  ];
  const bindingColor = (effect) => bindingPalette[hash(effect) % bindingPalette.length];
  const bindingEffects = (point) => {
    const effects = (point.bindings || []).map((binding) => binding.effect || "UNSPECIFIED");
    return [...new Set(effects.length ? effects : ["UNSPECIFIED"])];
  };
  const effectNames = [...new Set(
    points.filter((point) => point.kind === "card").flatMap(bindingEffects),
  )].sort();
  const activeEffect = (point) => {
    const effects = bindingEffects(point);
    return effects.find((effect) => selectedEffects.has(effect)) || effects[0];
  };
  const pointColor = (point) => point.kind === "query" ? "#f2c94c" : bindingColor(activeEffect(point));

  const grid = document.createElementNS(namespace, "g");
  grid.setAttribute("class", "plot-grid");
  for (let index = 1; index < 5; index += 1) {
    const x = padding + ((width - padding * 2) * index) / 5;
    const y = padding + ((height - padding * 2) * index) / 5;
    for (const [x1, x2, y1, y2] of [[x, x, padding, height - padding], [padding, width - padding, y, y]]) {
      const line = document.createElementNS(namespace, "line");
      line.setAttribute("x1", x1);
      line.setAttribute("x2", x2);
      line.setAttribute("y1", y1);
      line.setAttribute("y2", y2);
      grid.appendChild(line);
    }
  }
  svg.appendChild(grid);

  const pointLayer = document.createElementNS(namespace, "g");
  svg.appendChild(pointLayer);
  const setText = (id, value) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value ?? "—";
  };
  const selectPoint = (point) => {
    const isQuery = point.kind === "query";
    setText("text-point-title", isQuery ? `Query ${point.sample_id || point.query_index}` : point.name || "Card");
    setText("text-point-kind", isQuery ? "Synthesis query" : "Parsed card");
    setText("text-point-name", isQuery ? `${point.dataset || "dataset"} · ${point.sample_id || "—"}` : point.name);
    setText("text-point-type", isQuery ? "—" : [point.type, point.cost].filter(Boolean).join(" · "));
    setText("text-point-bindings", point.binding_label);
    setText("text-point-card-id", isQuery ? "—" : point.card_id);
    setText("text-point-text", point.text);
  };

  const circles = points.map((point) => {
    const isQuery = point.kind === "query";
    const circle = document.createElementNS(namespace, "circle");
    circle.setAttribute("cx", scaleX(Number(point.x)));
    circle.setAttribute("cy", scaleY(Number(point.y)));
    circle.setAttribute("r", isQuery ? 6.5 : 3.6);
    circle.setAttribute("tabindex", "0");
    circle.setAttribute("class", `text-point${isQuery ? " is-query" : ""}`);
    const showTooltip = (event) => {
      tooltip.hidden = false;
      tooltip.textContent = isQuery
        ? `Query · ${point.sample_id || "sample"}`
        : `${point.name || "Card"} · ${point.binding_label || "UNSPECIFIED"}`;
      const bounds = svg.parentElement.getBoundingClientRect();
      tooltip.style.left = `${event.clientX - bounds.left + 12}px`;
      tooltip.style.top = `${event.clientY - bounds.top + 12}px`;
    };
    circle.addEventListener("mouseenter", showTooltip);
    circle.addEventListener("mousemove", showTooltip);
    circle.addEventListener("mouseleave", () => { tooltip.hidden = true; });
    circle.addEventListener("focus", () => selectPoint(point));
    circle.addEventListener("click", () => selectPoint(point));
    pointLayer.appendChild(circle);
    return { circle, point };
  });

  const renderLegend = () => {
    if (!legend) return;
    legend.replaceChildren();
    const effects = selectedEffects.size ? [...selectedEffects].sort() : effectNames;
    effects.forEach((effect) => {
      const dot = document.createElement("i");
      dot.className = "legend-dot";
      dot.style.background = bindingColor(effect);
      legend.append(dot, document.createTextNode(effect));
    });
  };

  const applyFilters = () => {
    const showQueries = Boolean(showQueriesToggle?.checked);
    circles.forEach(({ circle, point }) => {
      const visible = point.kind === "query"
        ? showQueries
        : selectedEffects.size === 0 || bindingEffects(point).some((effect) => selectedEffects.has(effect));
      circle.style.display = visible ? "" : "none";
      const color = pointColor(point);
      circle.setAttribute("fill", color);
      circle.style.fill = color;
    });
    renderLegend();
  };

  if (filterElement) {
    effectNames.forEach((effect) => {
      const label = document.createElement("label");
      label.className = "binding-effect-option";
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.value = effect;
      checkbox.addEventListener("change", () => {
        if (checkbox.checked) selectedEffects.add(effect);
        else selectedEffects.delete(effect);
        applyFilters();
      });
      const dot = document.createElement("i");
      dot.className = "legend-dot";
      dot.style.background = bindingColor(effect);
      label.append(checkbox, dot, document.createTextNode(effect));
      filterElement.appendChild(label);
    });
  }

  document.getElementById("binding-select-all")?.addEventListener("click", () => {
    effectNames.forEach((effect) => selectedEffects.add(effect));
    filterElement?.querySelectorAll("input").forEach((checkbox) => { checkbox.checked = true; });
    applyFilters();
  });
  document.getElementById("binding-clear-all")?.addEventListener("click", () => {
    selectedEffects.clear();
    filterElement?.querySelectorAll("input").forEach((checkbox) => { checkbox.checked = false; });
    applyFilters();
  });
  showQueriesToggle?.addEventListener("change", applyFilters);
  applyFilters();
})();
