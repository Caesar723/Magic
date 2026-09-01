(() => {
  const dataElement = document.getElementById("card-fusion-points-data");
  const svg = document.getElementById("card-fusion-plot");
  if (!dataElement || !svg) return;

  const points = JSON.parse(dataElement.textContent || "[]");
  const tooltip = document.getElementById("card-fusion-tooltip");
  const typeFilter = document.getElementById("card-fusion-type-filter");
  const semanticFilter = document.getElementById("card-fusion-semantic-filter");
  const searchInput = document.getElementById("card-fusion-search");
  const legend = document.getElementById("card-fusion-legend");
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
    catalog_only: "Not observed in replay",
  };
  const semanticPalette = [
    "#e76f51", "#f4a261", "#e9c46a", "#90be6d", "#43aa8b", "#4d908e",
    "#577590", "#5773c8", "#7b68ee", "#9d4edd", "#c77dff", "#d65db1",
    "#ef476f", "#ff9f1c", "#8ac926", "#00b4d8", "#4895ef", "#b8c0ff",
  ];

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
  const changeLabel = (change) => changeLabels[change] || change || "Unknown";
  const humanizeSemantic = (value) => String(value || "UNSPECIFIED")
    .replaceAll("_", " ")
    .toLocaleLowerCase()
    .replace(/\b\w/g, (character) => character.toUpperCase());
  const hash = (text) => [...String(text)].reduce((value, character) => ((value * 31) + character.charCodeAt(0)) >>> 0, 7);
  const semanticLabel = (point) => point.semantic_label || point.dominant_change || "UNSPECIFIED";
  const pointColor = (point) => {
    const semantic = semanticLabel(point);
    return changeColors[semantic] || semanticPalette[hash(semantic) % semanticPalette.length];
  };
  const setText = (id, value) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value ?? "—";
  };

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

  const cardTypes = [...new Set(points.map((point) => point.type || "Unknown"))].sort();
  const semanticLabels = [...new Set(points.map(semanticLabel))].sort();
  cardTypes.forEach((type) => {
    const option = document.createElement("option");
    option.value = type;
    option.textContent = type;
    typeFilter?.appendChild(option);
  });
  semanticLabels.forEach((semantic) => {
    const option = document.createElement("option");
    option.value = semantic;
    option.textContent = humanizeSemantic(semantic);
    semanticFilter?.appendChild(option);
  });
  if (legend) {
    semanticLabels.forEach((semantic) => {
      const dot = document.createElement("i");
      dot.className = "legend-dot";
      dot.style.background = changeColors[semantic] || semanticPalette[hash(semantic) % semanticPalette.length];
      legend.append(dot, document.createTextNode(humanizeSemantic(semantic)));
    });
  }

  const pointLayer = document.createElementNS(namespace, "g");
  svg.appendChild(pointLayer);
  let circles = [];
  const circleByIndex = new Map();

  const selectPoint = (point) => {
    circles.forEach(({ circle, point: candidate }) => {
      circle.classList.toggle("is-selected", candidate.card_index === point.card_index);
    });
    setText("card-fusion-title", point.label || "Card");
    const cost = (point.mana_cost || []).join("/");
    const stats = point.has_state ? ` · ${point.attack}/${point.health}` : "";
    setText("card-fusion-attributes", [point.type, cost ? `cost ${cost}` : "", stats].filter(Boolean).join(" "));
    setText("card-fusion-samples", String(point.sample_count ?? "—"));
    setText("card-fusion-effects", (point.semantic_effects || []).map(humanizeSemantic).join(" · ") || "Unspecified");
    setText("card-fusion-change", changeLabel(point.dominant_change));
    setText("card-fusion-traits", (point.special_types || []).join(" · ") || "None");
    setText("card-fusion-description", point.description);

    const neighborList = document.getElementById("card-fusion-neighbor-list");
    if (!neighborList) return;
    neighborList.replaceChildren();
    (point.neighbors || []).forEach((neighbor) => {
      const card = points[neighbor.card_index];
      if (!card) return;
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.type = "button";
      const similarity = document.createElement("strong");
      similarity.textContent = `${Math.round(neighbor.similarity * 100)}%`;
      const label = document.createElement("span");
      label.textContent = card.label || "Card";
      button.append(similarity, label);
      button.title = card.description || card.label || "Card";
      button.addEventListener("click", () => {
        selectPoint(card);
        circleByIndex.get(card.card_index)?.focus();
      });
      item.appendChild(button);
      neighborList.appendChild(item);
    });
  };

  circles = points.map((point) => {
    const circle = document.createElementNS(namespace, "circle");
    circle.setAttribute("cx", scaleX(Number(point.x)));
    circle.setAttribute("cy", scaleY(Number(point.y)));
    circle.setAttribute("r", Math.min(10, 3.8 + Math.log2((point.sample_count || 0) + 1)));
    circle.setAttribute("tabindex", "0");
    circle.setAttribute("class", "card-fusion-point");
    circle.setAttribute("fill", pointColor(point));
    circle.style.fill = pointColor(point);
    const showTooltip = (event) => {
      tooltip.hidden = false;
      tooltip.textContent = `${point.label || "Card"} · ${humanizeSemantic(semanticLabel(point))} · ${point.sample_count || 0} uses`;
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
    circleByIndex.set(point.card_index, circle);
    return { circle, point };
  });

  const applyFilters = () => {
    const requiredType = typeFilter?.value || "";
    const requiredSemantic = semanticFilter?.value || "";
    const query = (searchInput?.value || "").trim().toLocaleLowerCase();
    circles.forEach(({ circle, point }) => {
      const text = `${point.label || ""} ${point.description || ""}`.toLocaleLowerCase();
      const visible = (!requiredType || point.type === requiredType)
        && (!requiredSemantic || semanticLabel(point) === requiredSemantic)
        && (!query || text.includes(query));
      circle.style.display = visible ? "" : "none";
    });
  };
  typeFilter?.addEventListener("change", applyFilters);
  semanticFilter?.addEventListener("change", applyFilters);
  searchInput?.addEventListener("input", applyFilters);
  applyFilters();
  if (points.length) selectPoint(points[0]);
})();
