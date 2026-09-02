(() => {
  const data = document.getElementById("transition-plan-points-data"), svg = document.getElementById("transition-plan-plot");
  if (!data || !svg) return;
  const points = JSON.parse(data.textContent || "[]"), tooltip = document.getElementById("transition-plan-tooltip"), legend = document.getElementById("transition-plan-legend");
  const namespace = "http://www.w3.org/2000/svg", width = 1000, height = 640, padding = 42;
  const colors = { opponent_damage: "#e48279", self_damage: "#b98cff", life_gain: "#6fcf97", summon: "#76a9fa", remove: "#f2c94c", draw: "#56ccf2", discard: "#f2994a", graveyard_change: "#bb6bd9", library_change: "#8fb3a6", mana_change: "#a9d6a3", no_major_change: "#81938e" };
  const labels = { opponent_damage: "Opponent damage", self_damage: "Self damage", life_gain: "Life gain", summon: "Summon", remove: "Remove", draw: "Draw", discard: "Discard", graveyard_change: "Graveyard", library_change: "Library", mana_change: "Mana", no_major_change: "No major change" };
  // Return non-degenerate limits for either PCA axis.
  const extent = (key) => { const values = points.map((point) => Number(point[key]) || 0), low = Math.min(...values), high = Math.max(...values); return low === high ? [low - 1, high + 1] : [low, high]; };
  const [xMin, xMax] = extent("x"), [yMin, yMax] = extent("y");
  // Map PCA coordinates into the fixed SVG viewbox.
  const scaleX = (value) => padding + ((value - xMin) / (xMax - xMin)) * (width - padding * 2), scaleY = (value) => height - padding - ((value - yMin) / (yMax - yMin)) * (height - padding * 2);
  // Return the shared transition-space class and its exact display color.
  const change = (point) => point.state_delta?.change_type || "no_major_change", color = (point) => colors[change(point)] || colors.no_major_change;
  // Replace one inspector field without altering its markup.
  const setText = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value ?? "—"; };
  const grid = document.createElementNS(namespace, "g"); grid.setAttribute("class", "plot-grid");
  for (let index = 1; index < 5; index += 1) {
    const x = padding + ((width - padding * 2) * index) / 5, y = padding + ((height - padding * 2) * index) / 5;
    [[x, x, padding, height - padding], [padding, width - padding, y, y]].forEach(([x1, x2, y1, y2]) => { const line = document.createElementNS(namespace, "line"); line.setAttribute("x1", x1); line.setAttribute("x2", x2); line.setAttribute("y1", y1); line.setAttribute("y2", y2); grid.appendChild(line); });
  }
  svg.appendChild(grid); const layer = document.createElementNS(namespace, "g"); svg.appendChild(layer);
  if (legend) [...new Set(points.map(change))].sort().forEach((type) => { const dot = document.createElement("i"); dot.className = "legend-dot"; dot.style.background = colors[type] || colors.no_major_change; legend.append(dot, document.createTextNode(labels[type] || type)); });
  // Mark a point and expose the same sample metadata as Transition space.
  const select = (point, circle) => {
    svg.querySelectorAll(".transition-point").forEach((item) => item.classList.remove("is-highlighted")); circle.classList.add("is-highlighted");
    setText("transition-plan-title", `Plan ${point.vector_index}`); setText("transition-plan-index", String(point.source_index ?? point.vector_index)); setText("transition-plan-action", point.action?.label); setText("transition-plan-change", labels[change(point)] || change(point)); setText("transition-plan-card", point.card_used?.description); setText("transition-plan-coordinate", `PC1 ${Number(point.x).toFixed(3)} · PC2 ${Number(point.y).toFixed(3)}`);
    const link = document.getElementById("transition-plan-reconstruction-link"); if (link) { link.hidden = !point.reconstruction_url; link.href = point.reconstruction_url || "#"; }
  };
  points.forEach((point) => {
    const circle = document.createElementNS(namespace, "circle"); circle.setAttribute("cx", scaleX(Number(point.x))); circle.setAttribute("cy", scaleY(Number(point.y))); circle.setAttribute("r", point.is_highlighted ? "6.5" : "3.2"); circle.setAttribute("tabindex", "0"); circle.setAttribute("class", `transition-point${point.is_highlighted ? " is-highlighted" : ""}`); circle.style.fill = color(point);
    // Position a small label beside the hovered plan point.
    const showTooltip = (event) => { tooltip.hidden = false; tooltip.textContent = `${labels[change(point)] || change(point)} · ${point.action?.label || "Unknown action"}`; const bounds = svg.parentElement.getBoundingClientRect(); tooltip.style.left = `${event.clientX - bounds.left + 12}px`; tooltip.style.top = `${event.clientY - bounds.top + 12}px`; };
    circle.addEventListener("mouseenter", showTooltip); circle.addEventListener("mousemove", showTooltip); circle.addEventListener("mouseleave", () => { tooltip.hidden = true; }); circle.addEventListener("focus", () => select(point, circle)); circle.addEventListener("click", () => select(point, circle)); layer.appendChild(circle);
  });
})();
