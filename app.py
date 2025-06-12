import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st
import pandas as pd
import time
import os

# Constants
N_NODES = 30
AREA_SIZE = 100
MAX_ENERGY = 1.0
BS_LOCATION = (50, 50)

# Node class
class Node:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.is_CH = False

def euclidean(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def create_fuzzy_controller():
    residual_energy = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'residual_energy')
    distance_to_bs = ctrl.Antecedent(np.arange(0, 150, 10), 'distance_to_bs')
    node_density = ctrl.Antecedent(np.arange(0, 20, 1), 'node_density')
    ch_probability = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'ch_probability')

    residual_energy.automf(3)
    distance_to_bs.automf(3)
    node_density.automf(3)

    ch_probability['low'] = fuzz.trimf(ch_probability.universe, [0, 0, 0.5])
    ch_probability['medium'] = fuzz.trimf(ch_probability.universe, [0.2, 0.5, 0.8])
    ch_probability['high'] = fuzz.trimf(ch_probability.universe, [0.5, 1.0, 1.0])

    rules = [
        ctrl.Rule(residual_energy['good'] & distance_to_bs['poor'] & node_density['poor'], ch_probability['high']),
        ctrl.Rule(residual_energy['average'] & distance_to_bs['average'], ch_probability['medium']),
        ctrl.Rule(residual_energy['poor'] | distance_to_bs['good'], ch_probability['low']),
        ctrl.Rule(node_density['good'] & residual_energy['good'], ch_probability['medium']),
    ]

    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)

def simulate():
    np.random.seed(int(time.time()))  # Make randomness dynamic each time

    nodes = []
    for _ in range(N_NODES):
        x, y = np.random.uniform(0, AREA_SIZE, 2)
        energy = np.random.uniform(0.3, MAX_ENERGY)
        nodes.append(Node(x, y, energy))

    fuzzy_ctrl = create_fuzzy_controller()
    ch_scores = []
    results = []

    for i, node in enumerate(nodes):
        dist_to_bs = euclidean((node.x, node.y), BS_LOCATION)
        density = sum(euclidean((node.x, node.y), (other.x, other.y)) < 20 for j, other in enumerate(nodes) if j != i)

        fuzzy_ctrl.input['residual_energy'] = node.energy
        fuzzy_ctrl.input['distance_to_bs'] = dist_to_bs
        fuzzy_ctrl.input['node_density'] = density
        fuzzy_ctrl.compute()

        ch_prob = fuzzy_ctrl.output['ch_probability']
        ch_scores.append((i, ch_prob))

        results.append({
            'Node ID': i,
            'X': round(node.x, 2),
            'Y': round(node.y, 2),
            'Energy': round(node.energy, 3),
            'Distance to BS': round(dist_to_bs, 2),
            'Density': density,
            'Fuzzy Score': round(ch_prob, 3),
            'Is Cluster Head': False
        })

    best_node_idx = max(ch_scores, key=lambda x: x[1])[0]
    nodes[best_node_idx].is_CH = True
    results[best_node_idx]['Is Cluster Head'] = True

    df = pd.DataFrame(results)
    st.subheader("📋 Simulation Data")
    st.dataframe(df)

    fig, ax = plt.subplots()
    for i, node in enumerate(nodes):
        color = 'red' if node.is_CH else 'blue'
        ax.scatter(node.x, node.y, c=color)
        ax.text(node.x + 1, node.y + 1, f"{i}", fontsize=8)

    ax.scatter(*BS_LOCATION, c='green', marker='X', s=100, label='Base Station')
    ax.set_title("WSN Node Deployment with Cluster Head")
    ax.grid(True)
    ax.legend()
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    st.pyplot(fig)

    st.success(f"✅ Cluster Head selected: Node #{best_node_idx}")

# --------- Streamlit UI ---------
st.set_page_config(page_title="Dynamic WSN Cluster Head Simulation", layout="centered")
st.title("📡 Cluster Head Selection in WSNs Using Fuzzy Logic")
st.markdown("This app automatically re-runs the simulation based on your selected interval. Click 'Stop Simulation' to halt.")


if 'running' not in st.session_state:
    st.session_state.running = False

if 'interval' not in st.session_state:
    st.session_state.interval = 10


st.session_state.interval = st.slider("⏱️ Select rerun interval (seconds):", 1, 20, st.session_state.interval)


col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Simulation"):
        st.session_state.running = True
        st.rerun()

with col2:
    if st.button("⏹️ Stop Simulation"):
        st.session_state.running = False


if st.session_state.running:
    simulate()
    st.warning(f"⏳ Re-running in {st.session_state.interval} seconds...")
    time.sleep(st.session_state.interval)
    st.rerun()
