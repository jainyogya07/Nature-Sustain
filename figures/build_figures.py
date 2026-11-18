#!/usr/bin/env python3
"""Publication figures for the Delhi NCT plastic-waste manuscript.

Numbers are taken only from the validated Phase 7 files / manuscript tables.
Visual language follows the submitted mockups (Okabe–Ito, white ground).
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".mplconfig"))

import re
import textwrap

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd


def wrap(s, n):
    return "\n".join(textwrap.wrap(str(s), n, break_long_words=False))


def dms_to_dec(raw):
    s = str(raw).replace("’", "'").replace("”", '"').replace("′", "'").replace("″", '"')
    m = re.search(r"(\d+)\D+(\d+)\D+([\d.]+)\D*([NSEW])", s)
    if not m:
        return None
    d, mn, sec, hemi = m.groups()
    val = float(d) + float(mn) / 60.0 + float(sec) / 3600.0
    if hemi in "SW":
        val = -val
    return val

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

# Okabe–Ito
OI = dict(
    blue="#0072B2",
    orange="#E69F00",
    sky="#56B4E9",
    green="#009E73",
    yellow="#F0E442",
    vermillion="#D55E00",
    purple="#CC79A7",
    black="#000000",
    grey="#999999",
    navy="#003A5D",
    cream="#F4EFE6",
    ice="#E8F1F8",
    ice2="#D4E4F0",
)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 8.5,
    "axes.titlesize": 10,
    "axes.labelsize": 8.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

GREEN_SITES = ["Kamla Nehru Ridge", "Kashmere Gate ISBT", "CBD Karkardooma"]


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", pad_inches=0.12)
    fig.savefig(OUT / f"{name}.png", dpi=220, pad_inches=0.12)
    fig.savefig(OUT / f"{name}.svg", pad_inches=0.12)
    plt.close(fig)
    print("wrote", name)


def load():
    burden = pd.read_csv(ROOT / "phase7c_locality_plastic_burden_scores.csv")
    resin = pd.read_csv(ROOT / "phase7c_locality_full_resin_composition.csv")
    coords = pd.read_csv(ROOT / "pipeline_v2/audit/coordinate_registry.csv")
    lisa = pd.read_csv(ROOT / "pipeline_v2/advanced_analytics/8c_lisa_hotspots_elite.csv")
    robust = pd.read_csv(ROOT / "phase7d_robust_priorities.csv")
    comp = pd.read_csv(ROOT / "phase7d_locality_composite_scores_all_scenarios.csv")
    burden["burden_01"] = burden["plastic_burden_score"] / 100.0
    return burden, resin, coords, lisa, robust, comp


# ---------------------------------------------------------------------------
# Fig. 1
# ---------------------------------------------------------------------------
def fig1():
    stages = [
        ("1", "Localities (N=58)", "Quantify locality-scale plastic burden.", "Burden score + small-sample flag"),
        ("2", "Composition", "Characterise resin streams as prevalence.", "Resin profile; PVC scored"),
        ("3", "Spatial context", "Distinguish hotspots from isolated high burden.", "LISA class where p<0.05"),
        ("4", "City processing", "Place locality signals in the city ledger.", "76.81% rate; 259 TPD residual"),
        ("5", "Plant utilization", "Diagnose balance across four WTE plants.", "50.1 pp utilization spread"),
        ("6", "Robustness gate", "Test whether priorities survive method change.", "GREEN spending filter"),
        ("7", "Diversion feasibility", "State a constraint set, not a route.", "Permitted / blocked sinks"),
        ("8", "Licensed intervention", "Match action to evidence scale.", "Typed decision permissions"),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 7.4))
    ax.set_xlim(0, 16.6)
    ax.set_ylim(0, 12.4)
    ax.axis("off")

    ax.text(8.3, 12.05, "Evidence objects", ha="center", va="center",
            fontsize=11, fontweight="bold", color=OI["navy"])
    ax.text(8.3, 0.95, "Decision permissions", ha="center", va="center",
            fontsize=11, fontweight="bold", color=OI["navy"])

    strip = [("Measurements", 1.0), ("Diagnostic tests", 5.0),
             ("Robustness gate", 9.0), ("Licensed interventions", 13.0)]
    ax.add_patch(FancyBboxPatch((0.35, 10.55), 15.9, 0.85, boxstyle="round,pad=0.03,rounding_size=0.08",
                                facecolor=OI["cream"], edgecolor="#D9D0C2", linewidth=0.7))
    for i, (lab, x) in enumerate(strip):
        ax.text(x + 1.15, 10.97, lab, ha="center", va="center", fontsize=8.2,
                fontweight="bold", color=OI["blue"])
        if i < 3:
            ax.annotate("", xy=(x + 2.55, 10.97), xytext=(x + 2.15, 10.97),
                        arrowprops=dict(arrowstyle="-|>", color=OI["navy"], lw=0.9, mutation_scale=8))

    w, h_top, h_bot, gapx, gapy = 3.7, 1.45, 2.35, 0.28, 0.18
    for i, (n, title, purpose, output) in enumerate(stages):
        col, row = i % 4, i // 4
        x = 0.35 + col * (w + gapx)
        y_top = 8.85 - row * (h_top + h_bot + gapy + 0.45)
        face = OI["ice"] if i < 5 else OI["ice2"]
        ax.add_patch(FancyBboxPatch((x, y_top), w, h_top, boxstyle="round,pad=0.04,rounding_size=0.10",
                                    facecolor=face, edgecolor=OI["blue"], linewidth=1.0))
        ax.add_patch(Circle((x + 0.28, y_top + h_top - 0.28), 0.20, facecolor=OI["blue"], edgecolor="none"))
        ax.text(x + 0.28, y_top + h_top - 0.28, n, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(x + w / 2 + 0.08, y_top + h_top / 2 - 0.02, title, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=OI["navy"])
        ax.add_patch(FancyBboxPatch((x, y_top - h_bot - 0.08), w, h_bot, boxstyle="round,pad=0.04,rounding_size=0.10",
                                    facecolor=OI["cream"], edgecolor="#D9D0C2", linewidth=0.7))
        ax.text(x + 0.16, y_top - 0.28, "Purpose", ha="left", va="top", fontsize=7, fontweight="bold", color=OI["blue"])
        ax.text(x + 0.16, y_top - 0.50, wrap(purpose, 38), ha="left", va="top", fontsize=7.3, color="#333333", linespacing=1.3)
        ax.text(x + 0.16, y_top - 1.32, "Output", ha="left", va="top", fontsize=7, fontweight="bold", color=OI["blue"])
        ax.text(x + 0.16, y_top - 1.54, wrap(output, 38), ha="left", va="top", fontsize=7.3, color="#333333", linespacing=1.3)
        if col < 3:
            ax.annotate("", xy=(x + w + gapx - 0.04, y_top + h_top / 2),
                        xytext=(x + w + 0.04, y_top + h_top / 2),
                        arrowprops=dict(arrowstyle="-|>", color=OI["black"], lw=1.0, mutation_scale=9))

    ax.text(0.35, 4.85, "then", fontsize=8, color=OI["navy"], fontstyle="italic")
    ax.text(0.35, 0.28,
            "Do not transfer evidence beyond its measurement scale without validation. Delhi NCT is the demonstration; Delhi-NCR is the policy neighbourhood, not the sample.",
            fontsize=7.3, color="#555555", style="italic")
    save(fig, "fig1")


# ---------------------------------------------------------------------------
# Fig. 2
# ---------------------------------------------------------------------------
def fig2(burden, resin):
    top = burden.sort_values("plastic_burden_score", ascending=False).head(10).copy()
    names = top["location"].tolist()
    scores = (top["plastic_percent"] / 30.49).round(3).tolist()
    pcts = top["plastic_percent"].tolist()
    r = resin.set_index("location")
    cols = [
        ("pet_percent_of_plastic", "PET", OI["blue"]),
        ("pp_percent_of_plastic", "PP", OI["sky"]),
        ("hdpe_ldpe_percent_of_plastic", "HDPE/LDPE", OI["green"]),
        ("ps_percent_of_plastic", "PS", OI["orange"]),
        ("pvc_percent_of_plastic", "PVC", OI["purple"]),
        ("others_percent_of_plastic", "Others", OI["grey"]),
    ]
    fig = plt.figure(figsize=(11.2, 5.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 0.22, 1.50], wspace=0.06)
    ax = fig.add_subplot(gs[0])
    axp = fig.add_subplot(gs[1], sharey=ax)
    axb = fig.add_subplot(gs[2])

    y = np.arange(len(names))[::-1]
    ax.barh(y, scores, color=OI["blue"], height=0.62, zorder=2)
    for yi, s in zip(y, scores):
        ax.text(max(s - 0.03, 0.04), yi, f"{s:.3f}", va="center", ha="right",
                fontsize=7.6, color="white", fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Burden score (0–1)")
    ax.set_title("(a) Top localities by burden score (0–1)", loc="left", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    axp.set_xlim(0, 1)
    axp.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    for sp in axp.spines.values():
        sp.set_visible(False)
    axp.set_title("Plastic\nshare", loc="center", fontsize=7.4, color=OI["blue"], pad=8)
    for yi, p in zip(y, pcts):
        axp.text(1.0, yi, f"{p:.2f}%", va="center", ha="right", fontsize=7.6,
                 color=OI["blue"], fontweight="bold", clip_on=False)

    ax = axb
    yb = list(np.arange(len(names))[::-1]) + [-1.35]
    labels_b = names + ["All 58 localities (mean)"]
    rows = []
    for loc in names:
        rows.append([float(r.loc[loc, c]) for c, _, _ in cols])
    means = [23.60, 2.79, 53.24, 4.92, 1.65, 13.80]
    rows.append(means)
    left = np.zeros(len(rows))
    for j, (_, lab, col) in enumerate(cols):
        vals = np.array([row[j] for row in rows])
        ax.barh(yb, vals, left=left, color=col, height=0.62, label=lab, zorder=2)
        for yi, v, lf in zip(yb, vals, left):
            if v >= 7.5:
                ax.text(lf + v / 2, yi, f"{v:.1f}", ha="center", va="center", fontsize=6.2,
                        color="white" if j in (0, 2, 4) else "#222222")
        left = left + vals
    ax.set_yticks(yb)
    ax.set_yticklabels([""] * len(names) + ["All 58 localities (mean)"], fontsize=8)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of plastic by resin (%)")
    ax.set_title("(b) Plastic resin composition by locality (100% stacked)", loc="left", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    leg = ax.legend(ncol=6, loc="lower center", bbox_to_anchor=(0.5, -0.22), frameon=False, fontsize=7.2,
                    handlelength=1.1, columnspacing=0.9)
    for t in leg.get_texts():
        if t.get_text() == "Others":
            t.set_color("#777777")
            t.set_fontsize(6.6)

    fig.text(0.01, -0.02,
             "(a) Burden score = plastic % / 30.49; Kamla Nehru Ridge = 1.000. The right-hand column is plastic share of total waste.\n"
             "(b) 100% stacked resin shares. PVC is magenta because it is scored. N = 58. Ranking is by burden score (Layer A), not the composite ranks in the robustness registry.",
             fontsize=7, color="#444444")
    save(fig, "fig2")


# ---------------------------------------------------------------------------
# Fig. 3
# ---------------------------------------------------------------------------
def fig3(burden, coords, lisa):
    df = coords.merge(burden, left_on="location", right_on="location", how="left")
    df["lat_plot"] = df["lat_raw"].map(dms_to_dec).fillna(df["lat_decimal"])
    df["lon_plot"] = df["lon_raw"].map(dms_to_dec).fillna(df["lon_decimal"])
    lisa_map = lisa.set_index("location")["Cluster_Classification"].to_dict()
    lisa_p = lisa.set_index("location")["LISA_P_Value"].to_dict()

    def klass(name):
        lab = lisa_map.get(name, "")
        p = lisa_p.get(name, 1)
        if p > 0.05 or not lab:
            return "ns"
        if "High-High" in lab:
            return "hh"
        if "Low-Low" in lab:
            return "ll"
        if "Low-High" in lab:
            return "lh"
        if "High-Low" in lab:
            return "hl"
        return "ns"

    colors = {"hh": "#D55E00", "hl": "#E69F00", "ll": "#0072B2", "lh": "#56B4E9", "ns": "#B0B0B0"}
    nct = np.array([
        [76.84, 28.57], [76.83, 28.68], [76.92, 28.82], [77.02, 28.88],
        [77.17, 28.89], [77.28, 28.88], [77.35, 28.82], [77.348, 28.70],
        [77.34, 28.56], [77.32, 28.48], [77.22, 28.41], [77.10, 28.40],
        [76.95, 28.47], [76.84, 28.57],
    ])
    yamuna = np.array([
        [77.21, 28.88], [77.23, 28.80], [77.24, 28.72], [77.25, 28.64],
        [77.27, 28.56], [77.30, 28.48], [77.325, 28.42],
    ])

    fig = plt.figure(figsize=(10.2, 6.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[3.2, 1.15], wspace=0.08)
    ax = fig.add_subplot(gs[0])
    axl = fig.add_subplot(gs[1])
    axl.axis("off")
    ax.add_patch(Polygon(nct, closed=True, facecolor="#F7F4EE", edgecolor=OI["black"], lw=1.1, zorder=1))
    ax.plot(yamuna[:, 0], yamuna[:, 1], color=OI["sky"], lw=3.2, solid_capstyle="round", zorder=2, alpha=0.85)
    ax.text(77.31, 28.62, "Yamuna", color=OI["blue"], fontsize=7.5, style="italic")

    sizes = 28 + 220 * df["burden_01"].fillna(0).values
    cs = [colors[klass(n)] for n in df["location"]]
    ax.scatter(df["lon_plot"], df["lat_plot"], s=sizes, c=cs, edgecolors="white", linewidths=0.4, zorder=3)

    offsets = {
        "Kamla Nehru Ridge": (10, 12),
        "Kashmere Gate ISBT": (12, -16),
        "CBD Karkardooma": (10, 10),
        "DAV School": (16, -14),
        "Kamla Nagar Market": (-78, 10),
        "Tis Hazari Court": (-72, -14),
    }
    for name in GREEN_SITES + ["DAV School", "Kamla Nagar Market", "Tis Hazari Court"]:
        row = df[df["location"] == name]
        if row.empty:
            continue
        x, y = float(row["lon_plot"].iloc[0]), float(row["lat_plot"].iloc[0])
        if name in GREEN_SITES:
            ax.scatter([x], [y], s=260, facecolors="none", edgecolors=OI["green"], linewidths=1.7, zorder=4)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=offsets[name],
                    fontsize=6.6, color=OI["navy"], zorder=5,
                    arrowprops=dict(arrowstyle="-", color="#888888", lw=0.4))

    ax.set_xlim(76.78, 77.55)
    ax.set_ylim(28.36, 28.94)
    ax.set_aspect("equal")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, ls=":", lw=0.4, color="#CCCCCC")
    ax.annotate("N", xy=(76.92, 28.90), xytext=(76.92, 28.84),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1),
                ha="center", va="bottom", fontsize=9, fontweight="bold")
    # scale bar ~15 km ≈ 0.153 deg lon at 28.6N
    sb_x, sb_y = 76.88, 28.40
    ax.plot([sb_x, sb_x + 0.153], [sb_y, sb_y], color="black", lw=2.2)
    ax.text(sb_x + 0.076, sb_y - 0.018, "0        15 km", ha="center", fontsize=7)

    from matplotlib.lines import Line2D
    size_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#888", markersize=s, label=lab)
        for s, lab in [(4, "0.00–0.20"), (6.5, "0.20–0.40"), (8.5, "0.40–0.60"), (10.5, "0.60–0.80"), (13, "0.80–1.00")]
    ]
    class_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=colors[k], markersize=8, label=lab)
        for k, lab in [("hh", "High–High (cluster)"), ("hl", "High–Low (outlier)"),
                       ("ll", "Low–Low (cluster)"), ("lh", "Low–High (outlier)"), ("ns", "Not significant ($p>0.05$)")]
    ]
    green_h = Line2D([0], [0], marker="o", color="none", markerfacecolor="none",
                     markeredgecolor=OI["green"], markeredgewidth=1.6, markersize=10,
                     label="GREEN spending-filter sites")
    leg1 = axl.legend(handles=size_handles, title="Plastic burden score (0–1)", loc="upper left",
                      fontsize=7, title_fontsize=7.5, frameon=True, fancybox=False, edgecolor="#DDDDDD",
                      bbox_to_anchor=(0.0, 1.0))
    axl.add_artist(leg1)
    axl.legend(handles=class_handles + [green_h], title="Local Moran's I (LISA)", loc="upper left",
               fontsize=7, title_fontsize=7.5, frameon=True, fancybox=False, edgecolor="#DDDDDD",
               bbox_to_anchor=(0.0, 0.48))

    fig.text(0.08, 0.01,
             "Delhi NCT only. Point size = burden score; colour = LISA class where $p\\leq 0.05$. "
             "Ridge and Kashmere Gate ISBT are high-burden and not classified as hotspots.",
             fontsize=7.2, color="#444444")
    save(fig, "fig3")


# ---------------------------------------------------------------------------
# Fig. 4
# ---------------------------------------------------------------------------
def fig4():
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)
    ax.axis("off")

    # notes on TOP, not beside the bars
    ax.add_patch(FancyBboxPatch((0.25, 5.15), 4.55, 0.95, boxstyle="round,pad=0.04,rounding_size=0.06",
                                facecolor="#F7F7F7", edgecolor="#DDDDDD", linewidth=0.6))
    ax.text(2.52, 5.85, "Processing rate = 76.81%   (858 / 1,117)", ha="center", fontsize=8.2, color="#333333")
    ax.text(2.52, 5.42, "vs 85% reference  =  $-$8.19 pp", ha="center", fontsize=8.2,
            color=OI["vermillion"], fontweight="bold")

    ax.add_patch(FancyBboxPatch((5.05, 5.15), 4.70, 0.95, boxstyle="round,pad=0.04,rounding_size=0.06",
                                facecolor="#FAFAFA", edgecolor="#BBBBBB", linewidth=0.6, linestyle="--"))
    ax.text(7.40, 5.85, "Different denominator", ha="center", fontsize=8, fontweight="bold", color="#555555")
    ax.text(7.40, 5.42, "Total-MSW $\\approx$63% is not additive with these plastic figures.",
            ha="center", fontsize=7.2, color="#666666")

    bw = 2.85
    blocks = [
        (0.35, OI["blue"], "Generated", "1,117 TPD", "100%"),
        (3.55, "#2A9D8F", "Processed", "858 TPD", "76.81%"),
        (6.75, "#E8C07A", "Residual", "259 TPD", "23.19%"),
    ]
    for x, col, lab, val, pct in blocks:
        ax.add_patch(FancyBboxPatch((x, 1.85), bw, 2.45, boxstyle="round,pad=0.04,rounding_size=0.10",
                                    facecolor=col, edgecolor="none"))
        ax.text(x + bw / 2, 3.95, lab, ha="center", fontsize=9, fontweight="bold",
                color="white" if col != "#E8C07A" else "#4A3B16")
        ax.text(x + bw / 2, 3.25, val, ha="center", fontsize=14, fontweight="bold",
                color="white" if col != "#E8C07A" else "#4A3B16")
        ax.text(x + bw / 2, 2.55, pct, ha="center", fontsize=10,
                color="white" if col != "#E8C07A" else "#4A3B16")
    for x in (3.20, 6.40):
        ax.annotate("", xy=(x + 0.28, 3.05), xytext=(x - 0.08, 3.05),
                    arrowprops=dict(arrowstyle="-|>", color=OI["navy"], lw=1.4, mutation_scale=12))

    ax.text(5.0, 0.45,
            "$N=2$ city plastic ledger. Cross-sectional mass balance, not a trend and not a forecast.",
            ha="center", fontsize=7.5, color="#555555")
    save(fig, "fig4")


# ---------------------------------------------------------------------------
# Fig. 5
# ---------------------------------------------------------------------------
def fig5():
    plants = [
        ("Ghazipur\n(1,300 TPD)", 58.3, 347.7, OI["blue"], "Underutilized (< 85%)"),
        ("Tehkhand\n(2,000 TPD)", 68.0, 340.7, OI["blue"], "Underutilized (< 85%)"),
        ("Okhla\n(1,950 TPD)", 95.8, None, OI["orange"], "High Utilization (95–100%)"),
        ("Bawana\n(2,000 TPD)", 108.4, None, OI["vermillion"], "Over-Stressed (> 100%)"),
    ]
    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    y = np.arange(len(plants))[::-1]
    bar_height = 0.52

    # Draw bars
    for yi, (name, util, head, col, status) in zip(y, plants):
        # Main bar
        ax.barh(yi, util, color=col, height=bar_height, zorder=3, edgecolor="none")
        
        # White bold text inside bar
        ax.text(util - 2.2, yi, f"{util:.1f}%", va="center", ha="right",
                fontsize=9.2, fontweight="bold", color="white", zorder=5)
            
        # Headroom shaded band
        if head is not None:
            rect = Rectangle((util, yi - bar_height / 2), 85 - util, bar_height,
                             facecolor="#E8F4FA", edgecolor=OI["sky"],
                             linestyle="--", linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            ax.text((util + 85) / 2, yi, f"+{head:.1f} TPD\nHeadroom",
                    ha="center", va="center", color=OI["navy"],
                    fontsize=8.0, fontweight="bold", zorder=4)

    # 85% and 100% vertical lines
    ax.axvline(85, color="#2b6cb0", ls="--", lw=1.2, zorder=3)
    ax.axvline(100, color="#111111", ls="-", lw=1.3, zorder=3)

    # Benchmark labels above plot area with NO OVERLAP
    ax.text(84.0, 3.52, "85% Benchmark", ha="right", va="bottom", fontsize=8.0, fontweight="bold", color="#2b6cb0")
    ax.text(101.0, 3.52, "100% Design Capacity", ha="left", va="bottom", fontsize=8.0, fontweight="bold", color="#111111")

    # Annotations for Bawana over-stress
    ax.text(108.4 + 1.5, 0, "(+8.4% Over Design)", va="center", ha="left",
            fontsize=8.0, fontweight="bold", color=OI["vermillion"])

    ax.set_yticks(y)
    ax.set_yticklabels([p[0] for p in plants], fontsize=9, fontweight="medium")
    ax.set_xlim(0, 126)
    ax.set_ylim(-0.6, 3.8)
    ax.set_xlabel("Utilization of Licensed Design Capacity (%)", fontsize=9, fontweight="medium", labelpad=6)

    # Spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")

    # Legend at top
    legend_handles = [
        mpatches.Patch(facecolor=OI["blue"], label="Underutilized (< 85%)"),
        mpatches.Patch(facecolor=OI["orange"], label="High Utilization (95–100%)"),
        mpatches.Patch(facecolor=OI["vermillion"], label="Over-Stressed (> 100%)"),
        mpatches.Patch(facecolor="#E8F4FA", edgecolor=OI["sky"], linestyle="--", label="Operational Headroom to 85%"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", bbox_to_anchor=(0.0, 1.05),
              ncol=4, frameon=False, fontsize=7.6, handlelength=1.4, handleheight=0.9)

    # Subtitle / Header above legend
    fig.text(0.125, 0.965, "Operational Heterogeneity Across Delhi WTE Facilities: 50.1 pp Spread (58.3% to 108.4%)",
             fontsize=8.8, fontweight="bold", color=OI["navy"], va="top")

    # Footnote
    fig.text(0.125, 0.02,
             "Mixed-waste throughput headroom = (0.85 × design capacity) − actual throughput. Total headroom = 688.4 TPD.\nSource: DPCC Monthly Progress Report (March 2025, Annexure-5).",
             fontsize=7.2, color="#555555")

    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.18, right=0.96)
    save(fig, "fig5")


# ---------------------------------------------------------------------------
# Fig. 6
# ---------------------------------------------------------------------------
def fig6(comp, robust, burden):
    scen_cols = [
        ("composite_equal", "Baseline\n(equal)"),
        ("composite_plastic_dominant", "Burden $\\uparrow$"),
        ("composite_pvc_dominant", "PVC $\\uparrow$"),
        ("composite_perturb_plastic", "Perturb\nburden"),
        ("composite_perturb_pvc", "Perturb\nPVC"),
        ("composite_pca", "PCA"),
    ]
    ranks = pd.DataFrame({"locality": comp["locality"]})
    for col, _ in scen_cols:
        ranks[col] = comp[col].rank(ascending=False, method="min").astype(int)
    ranks["mean_rank"] = ranks[[c for c, _ in scen_cols]].mean(axis=1)
    ranks["borda"] = ranks[[c for c, _ in scen_cols]].sum(axis=1).rank(method="min").astype(int)
    ranks["top10"] = (ranks["composite_equal"] <= 10).astype(int)
    rob = robust.set_index("locality")
    bur = burden.set_index("location")["burden_01"]

    def klass(name):
        if name in GREEN_SITES:
            return "GREEN"
        hits = rob.loc[name, "appearance_rate_pct"] if name in rob.index else 0
        if name == "Ryan International School":
            return "RED"
        if hits >= 55:
            return "AMBER"
        return "RED"

    ranks["klass"] = ranks["locality"].map(klass)
    # display: GREEN first (emphasis), then AMBER by baseline rank, then a few RED
    green = ranks[ranks["klass"] == "GREEN"].copy()
    green["_ord"] = green["locality"].map({n: i for i, n in enumerate(GREEN_SITES)})
    green = green.sort_values("_ord")
    amber_names = ["DAV School", "National Museum", "Lajpat Nagar Central Market",
                   "Shakarpur", "Burari Sant Nagar", "Chanakyapuri"]
    amber = ranks[ranks["locality"].isin(amber_names)].copy()
    amber["_ord"] = amber["locality"].map({n: i for i, n in enumerate(amber_names)})
    amber = amber.sort_values("_ord")
    red = ranks[ranks["locality"].isin(["Ryan International School", "Ajmal Khan Road Market", "Okhla Mandi"])].copy()
    red["_ord"] = red["locality"].map({"Ryan International School": 0, "Ajmal Khan Road Market": 1, "Okhla Mandi": 2})
    red = red.sort_values("_ord")

    show = pd.concat([green, amber, red], ignore_index=True)
    n_g, n_a = len(green), len(amber)

    cmap = LinearSegmentedColormap.from_list("rank", [OI["blue"], "#DEEBF7", "white", "#F4C2B2", OI["vermillion"]])
    mat_cols = [c for c, _ in scen_cols] + ["borda", "mean_rank"]
    mat = show[mat_cols].values.astype(float)

    fig = plt.figure(figsize=(11.2, 6.8))
    gs = fig.add_gridspec(2, 1, height_ratios=[0.18, 1.0], hspace=0.08)
    axb = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])
    fig.suptitle("")

    axb.axis("off")
    boxes = [
        (0.04, "Weighting robustness", r"$\rho = 0.893$", "Mean Spearman correlation"),
        (0.36, "Top-10 overlap", "83.3%", "Across weighting/normalization rows"),
        (0.68, "Leave-one-out (LOO)", "0.55", "Mean rank displacement"),
    ]
    for x, h, v, s in boxes:
        axb.add_patch(FancyBboxPatch((x, 0.15), 0.28, 0.75, boxstyle="round,pad=0.02,rounding_size=0.04",
                                     facecolor=OI["ice"], edgecolor=OI["blue"], transform=axb.transAxes, linewidth=0.9))
        axb.text(x + 0.14, 0.78, h, ha="center", va="top", fontsize=7, color=OI["blue"], transform=axb.transAxes)
        axb.text(x + 0.14, 0.50, v, ha="center", va="center", fontsize=13, fontweight="bold",
                 color=OI["navy"], transform=axb.transAxes)
        axb.text(x + 0.14, 0.22, s, ha="center", va="bottom", fontsize=6.4, color="#555555", transform=axb.transAxes)

    im = ax.imshow(mat, cmap=cmap, vmin=1, vmax=58, aspect="auto")
    ax.set_yticks(range(len(show)))
    ax.set_yticklabels(show["locality"].tolist(), fontsize=8)
    headers = [h.replace("\n", " ") for _, h in scen_cols] + ["Borda", "Mean rank"]
    ax.set_xticks(range(len(headers)))
    ax.set_xticklabels(headers, rotation=25, ha="right", fontsize=7.4)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = int(round(mat[i, j]))
            ax.text(j, i, f"{val}", ha="center", va="center", fontsize=7,
                    color="white" if val <= 8 or val >= 45 else "#222222")
        # top10 chip
    # extra column for top-10 of baseline
    # draw class bands
    ax.axhline(n_g - 0.5, color=OI["green"], lw=1.2)
    ax.axhline(n_g + n_a - 0.5, color=OI["orange"], lw=1.2)
    for i in range(n_g):
        ax.get_yticklabels()[i].set_fontweight("bold")
        ax.get_yticklabels()[i].set_color("#1B5E20")
    ax.set_xlim(-0.5, mat.shape[1] - 0.5)

    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Rank (1 = highest priority)", fontsize=7)
    fig.text(0.01, -0.01,
             "Specification stability of candidate priorities. GREEN sites are displayed first for emphasis; they are not sorted above burden rank 1. "
             "Figure 2 ranks by plastic-burden score. This figure ranks a composite priority under alternative weights. "
             "DAV School is AMBER (LOO-influential) despite a 9/9 appearance rate. Mean Spearman rho = 0.893.",
             fontsize=7, color="#444444")
    save(fig, "fig6")


# ---------------------------------------------------------------------------
# Fig. 7
# ---------------------------------------------------------------------------
def fig7():
    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    steps = [
        (0.25, "1", "Origin", "GREEN high-burden sites\nRidge · Kashmere Gate · CBD\n$N=58$"),
        (3.15, "2", "Collection", "Segregated plastic stream\nto MRF / primary points"),
        (6.05, "3", "Facility check", "Design, utilization,\ncompliance, headroom"),
        (8.95, "4", "Utilization gate", "Prefer $<$85%  ·  85--100% conditional\nBlock $>$100%  (not slack)"),
    ]
    for x, n, title, body in steps:
        ax.add_patch(FancyBboxPatch((x, 5.55), 2.70, 2.25, boxstyle="round,pad=0.04,rounding_size=0.12",
                                    facecolor=OI["ice"], edgecolor=OI["blue"], linewidth=1.0))
        ax.add_patch(Circle((x + 0.32, 7.48), 0.22, facecolor=OI["blue"], edgecolor="none"))
        ax.text(x + 0.32, 7.48, n, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(x + 1.50, 7.48, title, ha="center", va="center", fontsize=9, fontweight="bold", color=OI["navy"])
        ax.text(x + 1.35, 6.55, body, ha="center", va="center", fontsize=7.4, color="#333333", linespacing=1.35)
    for x in (2.95, 5.85, 8.75):
        ax.annotate("", xy=(x + 0.18, 6.65), xytext=(x - 0.02, 6.65),
                    arrowprops=dict(arrowstyle="-|>", color=OI["navy"], lw=1.15, mutation_scale=11))

    ax.plot([10.30, 10.30], [5.52, 5.12], color=OI["navy"], lw=1.05)
    ax.plot([3.02, 8.97], [5.12, 5.12], color=OI["navy"], lw=1.05)
    ax.annotate("", xy=(3.02, 4.88), xytext=(3.02, 5.12),
                arrowprops=dict(arrowstyle="-|>", color=OI["navy"], lw=1.05, mutation_scale=10))
    ax.annotate("", xy=(8.97, 4.88), xytext=(8.97, 5.12),
                arrowprops=dict(arrowstyle="-|>", color=OI["navy"], lw=1.05, mutation_scale=10))

    ax.add_patch(FancyBboxPatch((0.25, 2.85), 5.55, 2.00, boxstyle="round,pad=0.04,rounding_size=0.10",
                                facecolor="#E6F4EA", edgecolor=OI["green"], linewidth=1.1))
    ax.text(3.02, 4.55, "Permitted sinks", ha="center", fontsize=8.5, fontweight="bold", color=OI["green"])
    ax.text(1.60, 3.85, "Ghazipur  58.3%", ha="center", fontsize=8.2, fontweight="bold", color=OI["navy"])
    ax.text(1.60, 3.35, "1,300 TPD  ·  headroom 347.7 TPD", ha="center", fontsize=7, color=OI["blue"])
    ax.text(4.45, 3.85, "Tehkhand  68.0%", ha="center", fontsize=8.2, fontweight="bold", color=OI["navy"])
    ax.text(4.45, 3.35, "2,000 TPD  ·  headroom 340.7 TPD", ha="center", fontsize=7, color=OI["blue"])

    ax.add_patch(FancyBboxPatch((6.20, 2.85), 5.55, 2.00, boxstyle="round,pad=0.04,rounding_size=0.10",
                                facecolor="#FDECEC", edgecolor=OI["vermillion"], linewidth=1.1))
    ax.text(8.97, 4.55, "Blocked / not treated as slack", ha="center", fontsize=8.5, fontweight="bold",
            color=OI["vermillion"])
    ax.text(8.97, 3.85, "Bawana  108.4%  ·  2,000 TPD  ·  load withheld",
            ha="center", fontsize=8, fontweight="bold", color=OI["navy"])
    ax.text(8.97, 3.35, "Okhla 95.8% is High Utilization, not spare capacity.",
            ha="center", fontsize=7.2, color="#555555")

    ax.text(0.25, 2.40, "Not solved here  —  later capacitated model", fontsize=8, fontweight="bold", color="#666666")
    for i, (t, b) in enumerate([
        ("Road network", "Topology, times, restrictions"),
        ("Fleet and routing", "Vehicle types and capacities"),
        ("Time windows", "Collection / delivery windows"),
    ]):
        x = 0.25 + i * 3.90
        ax.add_patch(FancyBboxPatch((x, 0.85), 3.70, 1.35, boxstyle="round,pad=0.03,rounding_size=0.08",
                                    facecolor="#FAFAFA", edgecolor="#D0D0D0", linewidth=0.7, linestyle="--"))
        ax.text(x + 1.85, 1.85, t, ha="center", fontsize=8, fontweight="bold", color="#555555")
        ax.text(x + 1.85, 1.35, b, ha="center", fontsize=7, color="#777777")

    ax.text(6.0, 0.28, "Constraint set, not an optimal route. N=58 origins; plant census from DPCC March 2025.",
            ha="center", fontsize=7.4, color="#555555")
    save(fig, "fig7")


# ---------------------------------------------------------------------------
# Fig. 8
# ---------------------------------------------------------------------------
def fig8():
    cards = [
        ("1  Locality burden", "ROBUST PRIORITY",
         "Ridge = 1.000; Kashmere Gate ISBT = 0.992; 58 localities scored 0–1.",
         "Prioritise collection at robust high-burden sites (Ridge, Kashmere Gate, CBD).",
         "Export of these ranks to other cities or years."),
        ("2  PVC", "INVESTIGATION",
         "PVC spikes at DAV School (15.43%); sample mean 1.65%.",
         "Site investigation; keep chlorinated resin off an over-stressed grate.",
         "Generalisation of one-site PVC to citywide feed."),
        ("3  PET / PP", "DESCRIPTIVE",
         "PET = 23.60%, PP = 2.79% (means; N=58).",
         "Assess MRF access where PET is prevalent; measure capture.",
         "Equating PET share with a recycling rate."),
        ("4  City processing", "TWO-RECORD LEDGER",
         "858 of 1,117 TPD processed (76.81%); -8.19 pp vs 85%.",
         "Record a plastic line in the municipal ledger; commission a fate study.",
         "Trend or forecast of processing from N=2."),
        ("5  WTE utilization", "CENSUS SNAPSHOT",
         "Ghazipur 58.3%; Tehkhand 68.0%; Okhla 95.8%; Bawana 108.4%; range 50.1 pp.",
         "Relieve Bawana; fill Ghazipur/Tehkhand up to mixed-waste headroom.",
         "Treatment of Okhla as slack, or of 688.4 TPD as spare."),
        ("6  Spatial clusters", "LISA-CONFIRMED",
         "High–high: Kamla Nagar Market, Tis Hazari. Ridge and Kashmere Gate not classified.",
         "Zone plans for confirmed clusters; site lifting at isolated generators.",
         "Treatment of a high-burden name as a hotspot name."),
    ]
    chip = {
        "ROBUST PRIORITY": OI["green"],
        "INVESTIGATION": "#5B4B8A",
        "DESCRIPTIVE": OI["grey"],
        "TWO-RECORD LEDGER": "#6B5B4F",
        "CENSUS SNAPSHOT": OI["navy"],
        "LISA-CONFIRMED": OI["blue"],
    }
    fig, ax = plt.subplots(figsize=(10.8, 8.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 13.5)
    ax.axis("off")

    rh, gap = 1.85, 0.12
    y0 = 11.95
    for i, (layer, rob, evid, yes, no) in enumerate(cards):
        y = y0 - i * (rh + gap)
        ax.add_patch(FancyBboxPatch((0.25, y), 11.50, rh, boxstyle="round,pad=0.03,rounding_size=0.10",
                                    facecolor="white", edgecolor="#D8DEE6", linewidth=0.9))
        ax.add_patch(Rectangle((0.25, y), 0.12, rh, facecolor=chip[rob], edgecolor="none"))
        ax.text(0.55, y + rh - 0.32, layer, ha="left", va="center", fontsize=8.6, fontweight="bold", color=OI["navy"])
        ax.add_patch(FancyBboxPatch((8.15, y + rh - 0.56), 3.35, 0.44,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=chip[rob], edgecolor="none"))
        ax.text(9.82, y + rh - 0.34, rob, ha="center", va="center", fontsize=5.7, color="white", fontweight="bold")
        ax.text(0.55, y + rh - 0.82, evid, ha="left", va="center", fontsize=7.4, color="#333333")
        ax.text(0.55, y + 0.42, "Licensed  ·  " + yes, ha="left", va="center", fontsize=7.2, color=OI["navy"])
        ax.text(0.55, y + 0.16, "Not licensed  ·  " + no, ha="left", va="center", fontsize=7.2, color="#6B2D3C")

    ax.text(0.25, 0.68,
            "GREEN/AMBER/RED are reserved for locality-priority robustness classes (Table 6).",
            fontsize=6.9, color="#555555")
    ax.text(0.25, 0.40,
            "Other status labels identify the evidence type and are not robustness grades.",
            fontsize=6.9, color="#555555")
    save(fig, "fig8")


# ---------------------------------------------------------------------------
# Fig. 9
# ---------------------------------------------------------------------------
def fig9():
    fig, ax = plt.subplots(figsize=(10.8, 7.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10.2)
    ax.axis("off")

    headers = [
        (0.25, OI["blue"], "MEASUREMENTS"),
        (4.20, "#666666", "OFFICIAL REPORTS  (context)"),
        (8.15, OI["green"], "INFERENCE"),
    ]
    for x, col, lab in headers:
        ax.text(x + 1.725, 9.65, lab, ha="center", fontsize=8.4, fontweight="bold", color=col)

    meas = [
        "1. Composition ($N=58$)\nPET 23.60%; PP 2.79%; PVC spike at DAV 15.43%.",
        "2. Burden ($N=58$)\nRidge = 1.000; Kashmere Gate ISBT = 0.992.",
        "3. City processing ($N=2$)\n858 / 1,117 TPD = 76.81%; $-$8.19 pp vs 85%.",
        "4. Plant utilization (census)\n58.3 / 68.0 / 95.8 / 108.4%; range 50.1 pp.",
        "5. Spatial context ($N=58$)\nHigh burden $\\neq$ hotspot. HH: Kamla Nagar, Tis Hazari.",
    ]
    grey = [
        "PIB / MoEFCC (EPR)\n20.7 Mt plastic packaging recycled nationally since 2022.",
        "—",
        "Delhi Economic Survey 2025–26\nTotal-MSW processing $\\approx$63% citywide.",
        "MCD / DPCC reports + CPCB affidavit\nOperations, downtime; Okhla meets monitored norms.",
        "—",
    ]
    infer = [
        "A. Material actions\nSegregate; MRF for PET; inspect DAV PVC.",
        "B. Place-based priorities\nGREEN sites as spending filter.",
        "C. Capacity / throughput\nPlastic ledger line; fate study for 259 TPD.",
        "D. Plant loading\nFill Ghazipur/Tehkhand; withhold load from Bawana.",
        "E. Spatial licence\nZone plans for clusters; site lifting for isolated generators.",
    ]
    w, h = 3.45, 1.42
    ys = [8.00, 6.42, 4.84, 3.26, 1.68]
    xs = [0.25, 4.20, 8.15]
    faces = ["#EAF3FA", "#F2F2F2", "#E7F6EC"]
    edges = [OI["blue"], "#888888", OI["green"]]
    for items, face, edge, x in zip([meas, grey, infer], faces, edges, xs):
        for txt, y in zip(items, ys):
            if txt == "—":
                continue
            ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        facecolor=face, edgecolor=edge, linewidth=0.9))
            ax.text(x + 0.14, y + h - 0.14, txt, ha="left", va="top", fontsize=6.7, color="#222222", linespacing=1.28)

    mid = lambda i: ys[i] + h / 2
    ax.annotate("", xy=(xs[1] - 0.04, mid(0)), xytext=(xs[0] + w + 0.04, mid(0)),
                arrowprops=dict(arrowstyle="-|>", color=OI["blue"], lw=1.1, mutation_scale=9))
    ax.annotate("", xy=(xs[2] - 0.04, mid(1)), xytext=(xs[0] + w + 0.04, mid(1)),
                arrowprops=dict(arrowstyle="-|>", color=OI["green"], lw=1.1, mutation_scale=9))
    ax.annotate("", xy=(xs[1] - 0.04, mid(2)), xytext=(xs[0] + w + 0.04, mid(2)),
                arrowprops=dict(arrowstyle="-|>", color=OI["grey"], lw=1.1, ls="--", mutation_scale=9))
    ax.annotate("", xy=(xs[2] - 0.04, mid(3)), xytext=(xs[1] + w + 0.04, mid(3)),
                arrowprops=dict(arrowstyle="-|>", color=OI["green"], lw=1.1, mutation_scale=9))
    ax.annotate("", xy=(xs[2] - 0.04, mid(4)), xytext=(xs[0] + w + 0.04, mid(4)),
                arrowprops=dict(arrowstyle="-|>", color=OI["green"], lw=1.1, mutation_scale=9))

    ax.plot([0.30, 0.95], [0.95, 0.95], color=OI["blue"], lw=1.6)
    ax.text(1.05, 0.95, "context", va="center", fontsize=7.4, color=OI["blue"])
    ax.plot([2.55, 3.20], [0.95, 0.95], color=OI["green"], lw=1.6)
    ax.text(3.30, 0.95, "converges", va="center", fontsize=7.4, color=OI["green"])
    ax.plot([5.10, 5.75], [0.95, 0.95], color=OI["grey"], lw=1.6, ls="--")
    ax.text(5.85, 0.95, "not comparable", va="center", fontsize=7.4, color="#666666")

    ax.add_patch(FancyBboxPatch((0.30, 0.12), 11.40, 0.55, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#FAFAFA", edgecolor="#DDDDDD", linewidth=0.6))
    ax.text(6.00, 0.40,
            "The $\\approx$63% total-MSW rate and 76.81% plastic rate may both be true without either confirming the other.",
            ha="center", va="center", fontsize=7.2, color="#333333")
    save(fig, "fig9")


def main():
    burden, resin, coords, lisa, robust, comp = load()
    fig1()
    fig2(burden, resin)
    fig3(burden, coords, lisa)
    fig4()
    fig5()
    fig6(comp, robust, burden)
    fig7()
    fig8()
    fig9()
    print("done", OUT)


if __name__ == "__main__":
    main()
