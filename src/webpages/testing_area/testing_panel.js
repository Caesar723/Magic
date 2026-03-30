(function () {
  const TYPE_FOLDER = {
    Creature: "creature",
    Instant: "Instant",
    Land: "land",
    Sorcery: "sorcery",
  };

  const KEYWORDS = [
    { id: "flying", label: "Flying" },
    { id: "reach", label: "Reach" },
    { id: "trample", label: "Trample" },
    { id: "haste", label: "Haste" },
    { id: "lifelink", label: "Lifelink" },
    { id: "vigilance", label: "Vigilance" },
    { id: "flash", label: "Flash" },
  ];

  class TestingLabPanel {
    constructor(client) {
      this.client = client;
      this.socket = client.socket_main;
      this.playerName = window.dataFromBackend.self;
      this.side = "self";
      this.cardDest = "hand";
      this.cardDataByType = {};

      this.drawer = document.getElementById("labDrawer");
      this.railBtn = document.getElementById("labRailBtn");

      this._bindDrawer();
      this._buildKeywords();
      this._bindSideSeg();
      this._bindDestSeg();
      this._bindSpawn();
      this._bindGlobal();
      this._loadCardNames();
    }

    _bindDrawer() {
      if (!this.railBtn || !this.drawer) return;
      this.railBtn.addEventListener("click", () => {
        const open = this.drawer.getAttribute("data-open") === "true";
        const next = !open;
        this.drawer.setAttribute("data-open", next ? "true" : "false");
        this.railBtn.setAttribute("aria-expanded", next ? "true" : "false");
      });
    }

    _buildKeywords() {
      const wrap = document.getElementById("labKeywords");
      if (!wrap) return;
      KEYWORDS.forEach((kw) => {
        const label = document.createElement("label");
        label.className = "lab-chip";
        const inp = document.createElement("input");
        inp.type = "checkbox";
        inp.value = kw.id;
        inp.id = `kw-${kw.id}`;
        const span = document.createElement("span");
        span.textContent = kw.label;
        label.appendChild(inp);
        label.appendChild(span);
        wrap.appendChild(label);
      });
    }

    _bindSideSeg() {
      const seg = document.querySelector(".lab-seg:not(.lab-seg-three)");
      if (!seg) return;
      seg.querySelectorAll("button[data-side]").forEach((btn) => {
        btn.addEventListener("click", () => {
          this.side = btn.getAttribute("data-side");
          seg.querySelectorAll("button[data-side]").forEach((b) => {
            b.setAttribute("data-active", b === btn ? "true" : "false");
          });
        });
      });
    }

    _bindDestSeg() {
      const seg = document.querySelector(".lab-seg-three");
      if (!seg) return;
      seg.querySelectorAll(".lab-dest-btn[data-dest]").forEach((btn) => {
        btn.addEventListener("click", () => {
          this.cardDest = btn.getAttribute("data-dest");
          seg.querySelectorAll(".lab-dest-btn[data-dest]").forEach((b) => {
            b.setAttribute("data-active", b === btn ? "true" : "false");
          });
        });
      });
    }

    _selectedKeywordIds() {
      return Array.from(
        document.querySelectorAll("#labKeywords input:checked")
      ).map((el) => el.value);
    }

    _bindSpawn() {
      const btn = document.getElementById("labSpawnBtn");
      if (!btn) return;
      btn.addEventListener("click", () => {
        const p = parseInt(document.getElementById("labPower").value, 10) || 0;
        const t = parseInt(document.getElementById("labTough").value, 10) || 1;
        const kws = this._selectedKeywordIds().join(",");
        const content = [this.side, String(p), String(t), kws].join(";");
        this._send("test_spawn", content);
      });
    }

    _bindGlobal() {
      const clearHand = document.getElementById("labClearHandBtn");
      if (clearHand) clearHand.addEventListener("click", () => this._send("test_clear_hand", ""));

      const resetLand = document.getElementById("labResetLandCapBtn");
      if (resetLand) resetLand.addEventListener("click", () => this._send("test_reset_land_cap", ""));

      const untapAll = document.getElementById("labUntapAllBtn");
      if (untapAll) untapAll.addEventListener("click", () => this._send("test_untap_all", ""));

      const wipe = document.getElementById("labWipeBtn");
      if (wipe) wipe.addEventListener("click", () => this._send("test_board_wipe", ""));

      const mSelf = document.getElementById("labManaSelfBtn");
      if (mSelf) mSelf.addEventListener("click", () => this._send("test_restore_mana", "self"));

      const mAll = document.getElementById("labManaAllBtn");
      if (mAll) mAll.addEventListener("click", () => this._send("test_restore_mana", "all"));
    }

    _send(type, content) {
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
      const msg = [this.playerName, type, content].join("|");
      this.socket.send(msg);
    }

    async addCard(type, name) {
      const content = `${name}+${type}+1+${this.cardDest}`;
      const values = [this.playerName, "add_card", content];
      this.socket.send(values.join("|"));
    }

    async _loadCardNames() {
      const strip = document.getElementById("labTypeStrip");
      const grid = document.getElementById("labCardGrid");
      if (!strip || !grid) return;

      try {
        const res = await fetch("/get_all_cards_name", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
        const data = await res.json();
        const names = data.card_names || {};
        this.cardDataByType = names;

        const types = Object.keys(names);
        let activeType = types[0] || null;

        const renderGrid = (t) => {
          grid.innerHTML = "";
          const folder = TYPE_FOLDER[t];
          (names[t] || []).forEach((name) => {
            const tile = document.createElement("button");
            tile.type = "button";
            tile.className = "lab-card-tile";
            const imgPath = `cards/${folder}/${name}/compress_img.jpg`;
            const thumb = document.createElement("span");
            thumb.className = "lab-card-thumb";
            const img = document.createElement("img");
            img.src = imgPath;
            img.alt = "";
            img.loading = "lazy";
            thumb.appendChild(img);
            const cap = document.createElement("span");
            cap.className = "lab-card-name";
            cap.textContent = name;
            tile.appendChild(thumb);
            tile.appendChild(cap);
            tile.addEventListener("click", () => this.addCard(t, name));
            grid.appendChild(tile);
          });
        };

        types.forEach((t) => {
          const pill = document.createElement("button");
          pill.type = "button";
          pill.className = "lab-type-pill";
          pill.textContent = t;
          pill.setAttribute("data-type", t);
          if (t === activeType) pill.setAttribute("data-active", "true");
          pill.addEventListener("click", () => {
            activeType = t;
            strip.querySelectorAll(".lab-type-pill").forEach((p) => {
              p.setAttribute("data-active", p.getAttribute("data-type") === t ? "true" : "false");
            });
            renderGrid(t);
          });
          strip.appendChild(pill);
        });

        if (activeType) renderGrid(activeType);
      } catch (e) {
        console.warn("TestingLab: could not load card names", e);
      }
    }
  }

  window.TestingLabPanel = TestingLabPanel;
})();
