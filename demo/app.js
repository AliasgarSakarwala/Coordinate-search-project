// Wires up DEMO_DATA (from trajectories.js) to the two Plotly panels.
// No build step, no framework - just enough JS to make the sliders and
// tabs behave.

const PALETTE = {
  Complete: "#1f77b4",
  Ordered: "#ff7f0e",
  Opportunistic: "#2ca02c",
  MADS: "#d62728",
};

const ALGO_NAMES = Object.keys(PALETTE);

let currentFunction = "Rastrigin";
let playing = false;
let playTimer = null;

function isAlgoEnabled(name) {
  return document.getElementById("chk-" + name).checked;
}

function contourTrace(name) {
  const d = DEMO_DATA.functions[name];
  return {
    x: d.x,
    y: d.y,
    z: d.z,
    type: "contour",
    colorscale: "Viridis",
    showscale: false,
    opacity: 0.85,
    contours: { coloring: "heatmap" },
    hoverinfo: "skip",
  };
}

function pathTraces(name, evalLimit) {
  const d = DEMO_DATA.functions[name];
  const traces = [];
  for (const algo of ALGO_NAMES) {
    if (!isAlgoEnabled(algo)) continue;
    const pts = d.trajectories[algo].filter((p) => p.evals <= evalLimit);
    if (pts.length === 0) continue;
    traces.push({
      x: pts.map((p) => p.x[0]),
      y: pts.map((p) => p.x[1]),
      mode: "lines+markers",
      name: algo,
      line: { color: PALETTE[algo], width: 2 },
      marker: { color: PALETTE[algo], size: 7 },
    });
  }
  return traces;
}

function updateSliderRange() {
  const d = DEMO_DATA.functions[currentFunction];
  let maxEvals = 1;
  for (const algo of ALGO_NAMES) {
    const pts = d.trajectories[algo];
    if (pts.length) maxEvals = Math.max(maxEvals, pts[pts.length - 1].evals);
  }
  const slider = document.getElementById("evalSlider");
  slider.max = maxEvals;
  slider.value = maxEvals;
}

function renderLandscape() {
  const evalLimit = Number(document.getElementById("evalSlider").value);
  document.getElementById("evalLabel").textContent = evalLimit + " evaluations";

  const traces = [contourTrace(currentFunction), ...pathTraces(currentFunction, evalLimit)];
  Plotly.react(
    "landscape-plot",
    traces,
    {
      title: currentFunction + " - incumbent point over time",
      xaxis: { range: [-1, 1], title: "x1 (normalized)" },
      yaxis: { range: [-1, 1], title: "x2 (normalized)" },
      margin: { t: 40 },
      paper_bgcolor: "#171a23",
      plot_bgcolor: "#171a23",
      font: { color: "#e7e9ee" },
      legend: { orientation: "h", y: -0.15 },
    },
    { displayModeBar: false, responsive: true }
  );
}

function renderPortfolio() {
  const traces = ALGO_NAMES.map((algo) => {
    const pts = DEMO_DATA.portfolio[algo];
    return {
      x: pts.map((p) => p[0]),
      y: pts.map((p) => p[1]),
      mode: "lines",
      name: algo,
      line: { color: PALETTE[algo], width: 2.5 },
    };
  });
  Plotly.newPlot(
    "portfolio-plot",
    traces,
    {
      title: "-Sharpe + cost + risk penalty vs. evaluations (lower is better)",
      xaxis: { title: "Function evaluations" },
      yaxis: { title: "Objective value" },
      margin: { t: 40 },
      paper_bgcolor: "#171a23",
      plot_bgcolor: "#171a23",
      font: { color: "#e7e9ee" },
      legend: { orientation: "h", y: -0.2 },
    },
    { displayModeBar: false, responsive: true }
  );
}

function togglePlay() {
  playing = !playing;
  document.getElementById("playBtn").textContent = playing ? "Pause" : "Play";
  if (playing) {
    playTimer = setInterval(() => {
      const slider = document.getElementById("evalSlider");
      let next = Number(slider.value) + Math.max(1, Number(slider.max) / 60);
      if (next > Number(slider.max)) next = 0;
      slider.value = next;
      renderLandscape();
    }, 90);
  } else {
    clearInterval(playTimer);
  }
}

function setupTabs() {
  const buttons = document.querySelectorAll(".tab-btn");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".panel").forEach((p) => p.classList.add("hidden"));
      document.getElementById(btn.dataset.tab).classList.remove("hidden");
      if (btn.dataset.tab === "portfolio") renderPortfolio();
    });
  });
}

function setup() {
  setupTabs();

  document.getElementById("functionSelect").addEventListener("change", (e) => {
    currentFunction = e.target.value;
    updateSliderRange();
    renderLandscape();
  });

  ALGO_NAMES.forEach((algo) => {
    document.getElementById("chk-" + algo).addEventListener("change", renderLandscape);
  });

  document.getElementById("evalSlider").addEventListener("input", renderLandscape);
  document.getElementById("playBtn").addEventListener("click", togglePlay);

  updateSliderRange();
  renderLandscape();
}

document.addEventListener("DOMContentLoaded", setup);
