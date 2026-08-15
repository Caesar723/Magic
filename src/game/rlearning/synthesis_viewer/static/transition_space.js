(() => {
  const dataElement = document.getElementById("transition-points-data");
  const svg = document.getElementById("transition-plot");
  if (!dataElement || !svg) return;

  const points = JSON.parse(dataElement.textContent || "[]");
  const tooltip = document.getElementById("transition-tooltip");
  const highlightToggle = document.getElementById("highlight-toggle");
  const highlightsOnlyToggle = document.getElementById("highlights-only-toggle");
  const namespace = "http://www.w3.org/2000/svg";
  const width = 1000;
  const height = 640;
  const padding = 42;
  const changeColors = {
    opponent_damage: "#e48279",
    self_damage: "#b98cff",
    life_gain: "#6fcf97",
    summon: "#76a9fa",
    remove: "#f2c94c",
    draw: "#56ccf2",
    discard: "#f2994a",
    graveyard_change: "#bb6bd9",
    library_change: "#8fb3a6",
    mana_change: "#a9d6a3",
    no_major_change: "#81938e",
  };
  const changeLabels = {
    opponent_damage: "Opponent damage",
    self_damage: "Self damage",
    life_gain: "Life gain",
    summon: "Summon",
    remove: "Remove",
    draw: "Draw",
    discard: "Discard",
    graveyard_change: "Graveyard",
    library_change: "Library",
    mana_change: "Mana",
    no_major_change: "No major change",
  };
  const pointChange = (point) => point.state_delta?.change_type || "no_major_change";
  const pointColor = (point) => changeColors[pointChange(point)] || changeColors.no_major_change;

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

  const grid = document.createElementNS(namespace, "g");
  grid.setAttribute("class", "plot-grid");
  for (let index = 1; index < 5; index += 1) {
    const x = padding + ((width - padding * 2) * index) / 5;
    const y = padding + ((height - padding * 2) * index) / 5;
    const vertical = document.createElementNS(namespace, "line");
    vertical.setAttribute("x1", x);
    vertical.setAttribute("x2", x);
    vertical.setAttribute("y1", padding);
    vertical.setAttribute("y2", height - padding);
    grid.appendChild(vertical);
    const horizontal = document.createElementNS(namespace, "line");
    horizontal.setAttribute("x1", padding);
    horizontal.setAttribute("x2", width - padding);
    horizontal.setAttribute("y1", y);
    horizontal.setAttribute("y2", y);
    grid.appendChild(horizontal);
  }
  svg.appendChild(grid);

  const pointLayer = document.createElementNS(namespace, "g");
  pointLayer.setAttribute("class", "point-layer");
  svg.appendChild(pointLayer);

  const legend = document.getElementById("state-change-legend");
  if (legend) {
    [...new Set(points.map(pointChange))].sort().forEach((change) => {
      const dot = document.createElement("i");
      dot.className = "legend-dot";
      dot.style.background = changeColors[change] || changeColors.no_major_change;
      legend.append(dot, document.createTextNode(changeLabels[change] || change));
    });
  }

  const setText = (id, value) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value ?? "—";
  };

  const selectPoint = (point) => {
    setText("point-title", `Vector ${point.vector_index}`);
    setText("point-action", point.action?.label);
    setText("point-card-type", point.card_used?.type);
    setText("point-card-text", point.card_used?.description);
    setText("point-change", changeLabels[pointChange(point)] || pointChange(point));
    setText("point-source-index", String(point.source_index));
    setText("point-score", point.reconstruction_score ?? "—");
    const link = document.getElementById("reconstruction-link");
    if (link && point.reconstruction_url) {
      link.href = point.reconstruction_url;
      link.hidden = false;
    } else if (link) {
      link.hidden = true;
    }
  };

  const circles = points.map((point) => {
    const circle = document.createElementNS(namespace, "circle");
    circle.setAttribute("cx", scaleX(Number(point.x)));
    circle.setAttribute("cy", scaleY(Number(point.y)));
    circle.setAttribute("r", point.is_highlighted ? 7 : 3.2);
    circle.setAttribute("tabindex", "0");
    circle.style.fill = pointColor(point);
    circle.setAttribute(
      "class",
      `transition-point${point.is_highlighted ? " is-highlighted" : ""}`,
    );

    const showTooltip = (event) => {
      tooltip.hidden = false;
      tooltip.textContent = `${changeLabels[pointChange(point)] || pointChange(point)} · ${point.action?.label || "Unknown action"}`;
      const bounds = svg.parentElement.getBoundingClientRect();
      tooltip.style.left = `${event.clientX - bounds.left + 12}px`;
      tooltip.style.top = `${event.clientY - bounds.top + 12}px`;
    };
    circle.addEventListener("mouseenter", showTooltip);
    circle.addEventListener("mousemove", showTooltip);
    circle.addEventListener("mouseleave", () => { tooltip.hidden = true; });
    circle.addEventListener("focus", () => selectPoint(point));
    circle.addEventListener("click", () => {
      selectPoint(point);
      if (point.reconstruction_url) window.location.href = point.reconstruction_url;
    });
    pointLayer.appendChild(circle);
    return { circle, point };
  });

  const applyFilters = () => {
    const highlightsOnly = Boolean(highlightsOnlyToggle?.checked);
    const emphasizeHighlights = Boolean(highlightToggle?.checked);
    svg.classList.toggle("highlights-disabled", !emphasizeHighlights);
    circles.forEach(({ circle, point }) => {
      circle.style.display = highlightsOnly && !point.is_highlighted ? "none" : "";
      circle.setAttribute("r", point.is_highlighted && emphasizeHighlights ? 7 : 3.2);
      circle.style.stroke = point.is_highlighted && emphasizeHighlights ? "#fff0c9" : "";
      circle.style.strokeWidth = point.is_highlighted && emphasizeHighlights ? "2.2" : "";
    });
  };
  highlightToggle?.addEventListener("change", applyFilters);
  highlightsOnlyToggle?.addEventListener("change", applyFilters);
  applyFilters();
})();
