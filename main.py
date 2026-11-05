import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

from pathfinding import find_path
from rag import retrieve_rule, get_weights

st.set_page_config(page_title="Drone AI System", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#ff4b8b;'>🚁 Drone Path Suggestion System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:#00e6ff;'>AI + RAG + A* Path Planning</h4>",
    unsafe_allow_html=True
)

st.write("---")

mission = st.selectbox(
    "🎯 Select Mission Type:",
    ["normal", "low battery", "high risk"]
)

# ✅ UPDATED GRID (MULTIPLE PATHS NOW)
grid = [
    [0, 2, 2, 2, 0],
    [0, 0, 0, 2, 0],
    [0, 2, 0, 0, 0]
]

start = (0, 0)
goal = (2, 4)

if st.button("🚀 Generate Smart Path"):

    rule = retrieve_rule(mission)
    distance_weight, risk_weight = get_weights(mission)

    path = find_path(grid, start, goal, distance_weight, risk_weight)

    # ✅ SHOW PATH PROPERLY
    st.write("📍 Path Coordinates:")
    st.code(str(path))   # FIXED FORMAT

    if mission == "low battery":
        st.info("🔋 Low battery → Choosing shortest path")
    elif mission == "high risk":
        st.warning("⚠️ High risk → Avoiding risky zones")
    else:
        st.success("✅ Normal mission → Balanced path")

    st.write(f"**Rule Applied:** {rule}")

    placeholder = st.empty()

    for step in range(len(path)):
        fig, ax = plt.subplots()

        color_grid = np.zeros((len(grid), len(grid[0]), 3))

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 0:
                    color_grid[r][c] = [0.1, 0.8, 0.1]
                elif grid[r][c] == 1:
                    color_grid[r][c] = [0.9, 0.1, 0.1]
                elif grid[r][c] == 2:
                    color_grid[r][c] = [1, 1, 0.2]

        for i in range(step + 1):
            r, c = path[i]
            color_grid[r][c] = [0.1, 0.4, 1]

        ax.imshow(color_grid)

        ax.set_xticks(np.arange(-.5, len(grid[0]), 1))
        ax.set_yticks(np.arange(-.5, len(grid), 1))
        ax.grid(color='white')

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 1:
                    ax.text(c, r, "⛔", ha='center', va='center')
                elif grid[r][c] == 2:
                    ax.text(c, r, "⚠️", ha='center', va='center')

        drone_r, drone_c = path[step]
        ax.text(drone_c, drone_r, "🚁", ha='center', va='center', fontsize=14)

        ax.text(goal[1], goal[0], "🎯", ha='center', va='center')

        placeholder.pyplot(fig)
        time.sleep(0.4)

    st.success("✨ Path Generated Successfully!")