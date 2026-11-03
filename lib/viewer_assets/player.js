/* Graph player - renders recorded traces (lib/trace.py) as SVG and lets the
 * viewer step through them. Part of lib/viewer.py (embedded into every HTML
 * file). No external libraries.
 *
 * Data (JSON in <script id="graph-data">):
 *   {title, scenes: [{title, description, directed, showWeights, vertices, edges,
 *                     pseudocode, styles, palette, legend, frames}]}
 * Frame keys: m = message, l = pseudocode line, vf / ef = flags of vertices /
 * edges (by index), vl / el = labels, vc = colour class, vars = [[name, value]].
 */
(function () {
  "use strict";

  const DATA = JSON.parse(document.getElementById("graph-data").textContent);
  const NS = "http://www.w3.org/2000/svg";
  const VERTEX_BASE = { fill: "#f1f5f9", color: "#334155", width: 1.5, text: "#0f172a", halo: null, dash: false, fade: false };
  const EDGE_BASE = { color: "#94a3b8", width: 2.2, halo: null, dash: false, fade: false };
  const BASE_DELAY = 1100; // milliseconds per step at speed 1x
  // The longer side of the layout in SVG units: grows with the number of
  // vertices, so that vertex boxes keep a sensible size relative to the graph.
  function canvasSize(n) {
    return Math.max(380, Math.min(1500, 210 * Math.sqrt(n)));
  }
  let CANVAS = 1000;

  const $ = (id) => document.getElementById(id);
  const svg = $("stage");
  const tooltip = $("tooltip");

  const state = {
    scene: 0,
    frame: 0,
    playing: false,
    timer: null,
    nodes: [], // per vertex: {g, box, halo, name, sub, x, y, w, h}
    edges: [], // per edge: {g, line, halo, arrow, label}
    view: null, // current viewBox {x, y, w, h}
    hover: null,
  };

  // ------------------------------------------------------------------
  // Helpers
  // ------------------------------------------------------------------
  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs || {})) node.setAttribute(key, value);
    if (parent) parent.appendChild(node);
    return node;
  }

  function scene() {
    return DATA.scenes[state.scene];
  }

  function frame() {
    return scene().frames[state.frame];
  }

  function priority(name) {
    const style = scene().styles[name];
    return style && style.priority !== undefined ? style.priority : 50;
  }

  /* Combine the base style and all flags (by priority). A colour class always
   * decides the fill, so that a colouring stays visible; the flags then show
   * through border, halo, dashes and fading. */
  function resolve(base, flags, colorClass) {
    const result = Object.assign({}, base);
    const sorted = (flags || []).slice().sort((a, b) => priority(a) - priority(b));
    for (const flag of sorted) {
      const style = scene().styles[flag] || {};
      for (const [key, value] of Object.entries(style)) {
        if (key !== "priority" && key !== "description" && value !== null) result[key] = value;
      }
    }
    if (colorClass !== undefined) result.fill = scene().palette[colorClass % scene().palette.length];
    return result;
  }

  // ------------------------------------------------------------------
  // Building a scene
  // ------------------------------------------------------------------
  function buildScene() {
    const sc = scene();
    svg.innerHTML = "";
    // No colour transitions while the new scene appears (they would start from black).
    svg.classList.add("no-transition");
    requestAnimationFrame(() => requestAnimationFrame(() => svg.classList.remove("no-transition")));
    state.nodes = [];
    state.edges = [];
    $("scene-title").textContent = DATA.scenes.length > 1 || sc.title !== DATA.title ? sc.title : "";

    const n = sc.vertices.length;
    CANVAS = canvasSize(n);
    const font = 16;
    const edgeLayer = el("g", { class: "edges" }, svg);
    const labelLayer = el("g", { class: "edge-labels" }, svg);
    const nodeLayer = el("g", { class: "nodes" }, svg);

    for (const v of sc.vertices) {
      const g = el("g", { class: "node" }, nodeLayer);
      const halo = el("rect", { class: "halo", fill: "none", rx: 12 }, g);
      const box = el("rect", { class: "box", rx: 9 }, g);
      const name = el("text", { class: "name", "text-anchor": "middle", "dominant-baseline": "central", "font-size": font }, g);
      name.textContent = v.text;
      const sub = el("text", { class: "sub", "text-anchor": "middle", "font-size": font * 0.78, fill: "#475569" }, g);
      const width = Math.max(name.getComputedTextLength() + font * 1.3, font * 2.1);
      const node = { g, box, halo, name, sub, x: v.x * CANVAS, y: (1 - v.y) * CANVAS, w: width, h: font * 1.95, font };
      state.nodes.push(node);
      attachNodeEvents(node, state.nodes.length - 1);
    }

    for (const e of sc.edges) {
      const g = el("g", { class: "edge" }, edgeLayer);
      const halo = el("path", { class: "halo", fill: "none", "stroke-linecap": "round" }, g);
      const line = el("path", { class: "line", fill: "none", "stroke-linecap": "round" }, g);
      const arrow = sc.directed ? el("path", { class: "arrow" }, g) : null;
      const label = el("text", { class: "elabel", "text-anchor": "middle", "dominant-baseline": "central", "font-size": font * 0.8 }, labelLayer);
      state.edges.push({ g, halo, line, arrow, label, data: e });
    }

    buildPanels();
    const steps = sc.frames.length;
    $("controls").style.display = steps > 1 ? "" : "none";
    $("slider").max = Math.max(steps - 1, 0);
    fit();
  }

  // ------------------------------------------------------------------
  // Drawing a frame
  // ------------------------------------------------------------------
  function exitPoint(node, dx, dy) {
    const length = Math.hypot(dx, dy) || 1;
    dx /= length;
    dy /= length;
    const hw = node.w / 2 + 3;
    const hh = node.h / 2 + 3;
    const tx = Math.abs(dx) > 1e-9 ? hw / Math.abs(dx) : Infinity;
    const ty = Math.abs(dy) > 1e-9 ? hh / Math.abs(dy) : Infinity;
    const t = Math.min(tx, ty);
    return { x: node.x + dx * t, y: node.y + dy * t };
  }

  function render() {
    const sc = scene();
    const fr = frame();

    sc.vertices.forEach((v, i) => {
      const node = state.nodes[i];
      const st = resolve(VERTEX_BASE, fr.vf[i], fr.vc[i]);
      const x = node.x - node.w / 2;
      const y = node.y - node.h / 2;
      for (const rect of [node.box, node.halo]) {
        rect.setAttribute("x", x);
        rect.setAttribute("y", y);
        rect.setAttribute("width", node.w);
        rect.setAttribute("height", node.h);
      }
      node.box.setAttribute("fill", st.fill);
      node.box.setAttribute("stroke", st.color);
      node.box.setAttribute("stroke-width", st.width);
      node.box.setAttribute("stroke-dasharray", st.dash ? "6 4" : "none");
      node.halo.setAttribute("stroke", st.halo || "none");
      node.halo.setAttribute("stroke-width", st.halo ? 12 : 0);
      node.halo.setAttribute("opacity", st.halo ? 0.55 : 0);
      node.name.setAttribute("x", node.x);
      node.name.setAttribute("y", node.y);
      node.name.setAttribute("fill", st.text);
      node.sub.setAttribute("x", node.x);
      node.sub.setAttribute("y", node.y + node.h / 2 + node.font * 0.95);
      node.sub.textContent = fr.vl[i] !== undefined ? fr.vl[i] : "";
      node.g.setAttribute("opacity", st.fade ? 0.35 : 1);
    });

    sc.edges.forEach((e, i) => {
      const edge = state.edges[i];
      const st = resolve(EDGE_BASE, fr.ef[i]);
      const a = state.nodes[e.u];
      const b = state.nodes[e.v];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const rad = e.curved ? 0.18 : 0;
      const control = { x: (a.x + b.x) / 2 + rad * dy, y: (a.y + b.y) / 2 - rad * dx };
      const start = e.curved ? exitPoint(a, control.x - a.x, control.y - a.y) : exitPoint(a, dx, dy);
      let end = e.curved ? exitPoint(b, control.x - b.x, control.y - b.y) : exitPoint(b, -dx, -dy);

      if (edge.arrow) {
        const from = e.curved ? control : start;
        const ux = end.x - from.x;
        const uy = end.y - from.y;
        const len = Math.hypot(ux, uy) || 1;
        const nx = ux / len;
        const ny = uy / len;
        const size = 10 + st.width * 1.6;
        const half = 4.5 + st.width * 0.9;
        const base = { x: end.x - nx * size, y: end.y - ny * size };
        edge.arrow.setAttribute(
          "d",
          `M${end.x},${end.y} L${base.x - ny * half},${base.y + nx * half} L${base.x + ny * half},${base.y - nx * half} Z`
        );
        edge.arrow.setAttribute("fill", st.color);
        end = { x: end.x - nx * size * 0.8, y: end.y - ny * size * 0.8 };
      }
      const d = e.curved
        ? `M${start.x},${start.y} Q${control.x},${control.y} ${end.x},${end.y}`
        : `M${start.x},${start.y} L${end.x},${end.y}`;
      for (const path of [edge.line, edge.halo]) path.setAttribute("d", d);
      edge.line.setAttribute("stroke", st.color);
      edge.line.setAttribute("stroke-width", st.width);
      edge.line.setAttribute("stroke-dasharray", st.dash ? "9 6" : "none");
      edge.halo.setAttribute("stroke", st.halo || "none");
      edge.halo.setAttribute("stroke-width", st.halo ? st.width + 10 : 0);
      edge.halo.setAttribute("opacity", st.halo ? 0.45 : 0);
      edge.g.setAttribute("opacity", st.fade ? 0.3 : 1);

      // Label at 45 % of the edge (slightly off the middle, so that the
      // labels of two crossing diagonals do not overlap).
      const t = 0.45;
      const lx = (1 - t) * (1 - t) * a.x + 2 * (1 - t) * t * (e.curved ? control.x : (a.x + b.x) / 2) + t * t * b.x;
      const ly = (1 - t) * (1 - t) * a.y + 2 * (1 - t) * t * (e.curved ? control.y : (a.y + b.y) / 2) + t * t * b.y;
      const text = fr.el[i] !== undefined ? fr.el[i] : sc.showWeights ? e.w : "";
      edge.label.textContent = text;
      edge.label.setAttribute("x", lx);
      edge.label.setAttribute("y", ly);
      edge.label.setAttribute("fill", fr.ef[i] && fr.ef[i].length ? st.color : "#475569");
      edge.label.setAttribute("opacity", st.fade ? 0.4 : 1);
    });

    renderPanels();
    if (state.hover !== null) showTooltip(state.hover);
  }

  // ------------------------------------------------------------------
  // Side panels
  // ------------------------------------------------------------------
  function buildPanels() {
    const sc = scene();
    $("description").textContent = sc.description || "";
    $("description-panel").style.display = sc.description ? "" : "none";

    const code = $("code");
    code.innerHTML = "";
    $("code-panel").style.display = sc.pseudocode.length ? "" : "none";
    if (sc.pseudocode.length) {
      const list = document.createElement("ol");
      for (const line of sc.pseudocode) {
        const item = document.createElement("li");
        item.textContent = line;
        list.appendChild(item);
      }
      code.appendChild(list);
    }

    const legend = $("legend");
    legend.innerHTML = "";
    $("legend-panel").style.display = sc.legend.length ? "" : "none";
    const list = document.createElement("ul");
    for (const entry of sc.legend) {
      const item = document.createElement("li");
      const icon = el("svg", { width: 34, height: 20, viewBox: "0 0 34 20" }, item);
      if (entry.kind === "edge") {
        const st = resolve(EDGE_BASE, [entry.flag]);
        el("line", { x1: 2, y1: 10, x2: 32, y2: 10, stroke: st.color, "stroke-width": Math.min(st.width, 5),
          "stroke-dasharray": st.dash ? "6 4" : "none", opacity: st.fade ? 0.4 : 1 }, icon);
      } else {
        const st = entry.kind === "color" ? Object.assign({}, VERTEX_BASE, { fill: entry.fill }) : resolve(VERTEX_BASE, [entry.flag]);
        el("rect", { x: 3, y: 3, width: 28, height: 14, rx: 4, fill: st.fill, stroke: st.color,
          "stroke-width": Math.min(st.width, 3), "stroke-dasharray": st.dash ? "4 3" : "none", opacity: st.fade ? 0.4 : 1 }, icon);
      }
      const text = document.createElement("span");
      text.textContent = entry.text;
      item.appendChild(text);
      list.appendChild(item);
    }
    legend.appendChild(list);
  }

  function renderPanels() {
    const sc = scene();
    const fr = frame();
    $("message").textContent = fr.m || "";
    $("counter").textContent = `Step ${state.frame + 1} / ${sc.frames.length}`;
    $("slider").value = state.frame;
    $("first").disabled = $("prev").disabled = state.frame === 0;
    $("next").disabled = $("last").disabled = state.frame === sc.frames.length - 1;
    $("play").textContent = state.playing ? "❚❚" : "▶";
    $("play").title = state.playing ? "Pause (Space)" : "Play (Space)";

    const previous = state.frame > 0 ? Object.fromEntries(sc.frames[state.frame - 1].vars) : {};
    const table = document.createElement("table");
    for (const [name, value] of fr.vars) {
      const row = table.insertRow();
      row.insertCell().textContent = name;
      row.insertCell().textContent = value;
      if (state.frame > 0 && previous[name] !== value) row.className = "changed";
    }
    $("variables").innerHTML = "";
    $("variables").appendChild(table);
    $("variables-panel").style.display = fr.vars.length ? "" : "none";

    const items = $("code").querySelectorAll("li");
    items.forEach((item, i) => item.classList.toggle("active", fr.l === i + 1));
    if (fr.l && items[fr.l - 1]) {
      const list = items[fr.l - 1].parentElement;
      const item = items[fr.l - 1];
      if (item.offsetTop < list.scrollTop || item.offsetTop > list.scrollTop + list.clientHeight - 24) {
        list.scrollTop = item.offsetTop - list.clientHeight / 2;
      }
    }
    updateHash();
  }

  // ------------------------------------------------------------------
  // Navigation and playback
  // ------------------------------------------------------------------
  function goto(index) {
    const count = scene().frames.length;
    state.frame = Math.max(0, Math.min(count - 1, index));
    render();
  }

  function setScene(index, frameIndex) {
    stop();
    state.scene = Math.max(0, Math.min(DATA.scenes.length - 1, index));
    state.frame = 0;
    document.querySelectorAll("#tabs button").forEach((b, i) => b.classList.toggle("active", i === state.scene));
    buildScene();
    goto(frameIndex || 0);
  }

  function delay() {
    return BASE_DELAY / parseFloat($("speed").value);
  }

  function tick() {
    if (state.frame >= scene().frames.length - 1) {
      stop();
      return;
    }
    goto(state.frame + 1);
    state.timer = setTimeout(tick, delay());
  }

  function play() {
    if (scene().frames.length < 2) return;
    if (state.frame >= scene().frames.length - 1) goto(0);
    state.playing = true;
    state.timer = setTimeout(tick, delay());
    renderPanels();
  }

  function stop() {
    state.playing = false;
    clearTimeout(state.timer);
    if (scene()) renderPanels();
  }

  function toggle() {
    state.playing ? stop() : play();
  }

  function updateHash() {
    const hash = `#scene=${state.scene + 1}&step=${state.frame + 1}`;
    if (location.hash !== hash) history.replaceState(null, "", hash);
  }

  function readHash() {
    const params = new URLSearchParams(location.hash.slice(1));
    return { scene: (parseInt(params.get("scene"), 10) || 1) - 1, step: (parseInt(params.get("step"), 10) || 1) - 1 };
  }

  // ------------------------------------------------------------------
  // Zoom, pan, drag, tooltip
  // ------------------------------------------------------------------
  function setView(view) {
    state.view = view;
    svg.setAttribute("viewBox", `${view.x} ${view.y} ${view.w} ${view.h}`);
  }

  function fit() {
    if (!state.nodes.length) {
      setView({ x: 0, y: 0, w: CANVAS, h: CANVAS * 0.6 });
      return;
    }
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const node of state.nodes) {
      minX = Math.min(minX, node.x - node.w / 2);
      maxX = Math.max(maxX, node.x + node.w / 2);
      minY = Math.min(minY, node.y - node.h / 2);
      maxY = Math.max(maxY, node.y + node.h / 2 + node.font * 1.6);
    }
    const margin = 50;
    const top = 40; // room for the scene title
    setView({ x: minX - margin, y: minY - margin - top, w: maxX - minX + 2 * margin, h: maxY - minY + 2 * margin + top });
  }

  function toSvg(event) {
    const point = svg.createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    return point.matrixTransform(svg.getScreenCTM().inverse());
  }

  function attachNodeEvents(node, index) {
    node.g.addEventListener("pointerdown", (event) => {
      event.stopPropagation();
      node.g.setPointerCapture(event.pointerId);
      const start = toSvg(event);
      const origin = { x: node.x, y: node.y };
      const move = (ev) => {
        const p = toSvg(ev);
        node.x = origin.x + p.x - start.x;
        node.y = origin.y + p.y - start.y;
        render();
      };
      const up = () => {
        node.g.removeEventListener("pointermove", move);
        node.g.removeEventListener("pointerup", up);
      };
      node.g.addEventListener("pointermove", move);
      node.g.addEventListener("pointerup", up);
    });
    node.g.addEventListener("pointerenter", () => {
      state.hover = index;
      showTooltip(index);
    });
    node.g.addEventListener("pointerleave", () => {
      state.hover = null;
      tooltip.style.display = "none";
    });
  }

  function showTooltip(index) {
    const v = scene().vertices[index];
    const fr = frame();
    const lines = [v.text];
    if (fr.vf[index] && fr.vf[index].length) lines.push("flags: " + fr.vf[index].join(", "));
    if (fr.vl[index] !== undefined) lines.push("label: " + fr.vl[index]);
    if (fr.vc[index] !== undefined) lines.push("colour: " + scene().colorNames[fr.vc[index]]);
    if (v.info) lines.push(v.info);
    lines.push("degree: " + v.degree);
    tooltip.textContent = lines.join("\n");
    tooltip.style.display = "block";
  }

  svg.addEventListener("pointermove", (event) => {
    tooltip.style.left = event.clientX + 14 + "px";
    tooltip.style.top = event.clientY + 14 + "px";
  });

  svg.addEventListener("pointerdown", (event) => {
    svg.setPointerCapture(event.pointerId);
    svg.classList.add("panning");
    const start = { x: event.clientX, y: event.clientY, view: Object.assign({}, state.view) };
    const scale = state.view.w / svg.clientWidth;
    const move = (ev) => {
      setView(Object.assign({}, start.view, {
        x: start.view.x - (ev.clientX - start.x) * scale,
        y: start.view.y - (ev.clientY - start.y) * scale,
      }));
    };
    const up = () => {
      svg.classList.remove("panning");
      svg.removeEventListener("pointermove", move);
      svg.removeEventListener("pointerup", up);
    };
    svg.addEventListener("pointermove", move);
    svg.addEventListener("pointerup", up);
  });

  svg.addEventListener("wheel", (event) => {
    event.preventDefault();
    const factor = Math.exp(event.deltaY * 0.0015);
    const p = toSvg(event);
    const v = state.view;
    setView({ x: p.x - (p.x - v.x) * factor, y: p.y - (p.y - v.y) * factor, w: v.w * factor, h: v.h * factor });
  }, { passive: false });

  // ------------------------------------------------------------------
  // Export
  // ------------------------------------------------------------------
  function exportSvg() {
    const copy = svg.cloneNode(true);
    copy.setAttribute("xmlns", NS);
    copy.setAttribute("width", Math.round(state.view.w));
    copy.setAttribute("height", Math.round(state.view.h));
    copy.setAttribute("font-family", "Segoe UI, Roboto, Helvetica, Arial, sans-serif");
    const background = el("rect", { x: state.view.x, y: state.view.y, width: state.view.w, height: state.view.h, fill: "white" });
    copy.insertBefore(background, copy.firstChild);
    copy.querySelectorAll("text.sub, text.elabel").forEach((t) => {
      t.setAttribute("paint-order", "stroke");
      t.setAttribute("stroke", "white");
      t.setAttribute("stroke-width", "4");
    });
    const title = el("text", { x: state.view.x + 16, y: state.view.y + 30, "font-size": 20, "font-weight": 700, fill: "#0f172a" });
    title.textContent = scene().title;
    copy.appendChild(title);
    return new XMLSerializer().serializeToString(copy);
  }

  function fileName(extension) {
    const base = (scene().title || DATA.title || "graph").replace(/[^\w\-]+/g, "_").replace(/^_+|_+$/g, "") || "graph";
    return `${base}_step${state.frame + 1}.${extension}`;
  }

  function download(blob, name) {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = name;
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
      URL.revokeObjectURL(link.href);
      link.remove();
    }, 1000);
  }

  function savePng() {
    const image = new Image();
    const url = URL.createObjectURL(new Blob([exportSvg()], { type: "image/svg+xml" }));
    image.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = Math.round(state.view.w * 2);
      canvas.height = Math.round(state.view.h * 2);
      const context = canvas.getContext("2d");
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(url);
      canvas.toBlob((blob) => download(blob, fileName("png")));
    };
    image.src = url;
  }

  // ------------------------------------------------------------------
  // Start
  // ------------------------------------------------------------------
  function init() {
    document.title = DATA.title;
    $("title").textContent = DATA.title;
    const tabs = $("tabs");
    if (DATA.scenes.length > 1) {
      DATA.scenes.forEach((sc, i) => {
        const button = document.createElement("button");
        button.textContent = sc.title || `Scene ${i + 1}`;
        button.addEventListener("click", () => setScene(i));
        tabs.appendChild(button);
      });
    }
    $("first").addEventListener("click", () => { stop(); goto(0); });
    $("prev").addEventListener("click", () => { stop(); goto(state.frame - 1); });
    $("play").addEventListener("click", toggle);
    $("next").addEventListener("click", () => { stop(); goto(state.frame + 1); });
    $("last").addEventListener("click", () => { stop(); goto(scene().frames.length - 1); });
    $("slider").addEventListener("input", (event) => {
      const index = parseInt(event.target.value, 10); // read it before stop() redraws the slider
      stop();
      goto(index);
    });
    $("speed").addEventListener("change", () => {
      if (state.playing) {
        clearTimeout(state.timer);
        state.timer = setTimeout(tick, delay());
      }
    });
    $("fit").addEventListener("click", fit);
    $("save-svg").addEventListener("click", () => download(new Blob([exportSvg()], { type: "image/svg+xml" }), fileName("svg")));
    $("save-png").addEventListener("click", savePng);
    document.addEventListener("keydown", (event) => {
      if (event.target.tagName === "INPUT" && event.target.type !== "range") return;
      const actions = {
        ArrowRight: () => { stop(); goto(state.frame + 1); },
        ArrowLeft: () => { stop(); goto(state.frame - 1); },
        " ": toggle,
        Home: () => { stop(); goto(0); },
        End: () => { stop(); goto(scene().frames.length - 1); },
        PageDown: () => setScene(state.scene + 1),
        PageUp: () => setScene(state.scene - 1),
        f: fit,
      };
      if (actions[event.key]) {
        event.preventDefault();
        actions[event.key]();
      }
    });
    const start = readHash();
    setScene(start.scene, start.step);
  }

  init();
})();
