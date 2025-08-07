# 📡 Fuzzy Logic-Based Cluster Head Selection in Wireless Sensor Networks

This project introduces a dynamic, intelligent simulation for *cluster head selection* in Wireless Sensor Networks (WSNs) using *Fuzzy Logic*. The system optimizes energy efficiency and network lifetime by evaluating node characteristics and simulating CH selection through a visual, Streamlit-based interface.

---

## 👨‍💻 Team

- [Tushar Gupta](https://github.com/gtushar8055) — Dataset, Graphs, Data Analysis  
- [Nitish Kumar Choubey](https://github.com/NitishChoubey) — Model Coding, Documentation  
- [Harshit Singhal](https://github.com/harshitsinghal226) — Tables, Flowcharts, Paper content 
- [Nikhil Nagar](https://github.com/Nikhil-X-codes) — Research Paper Analysis, Tables  
- [Devansh Bansal](https://github.com/devanshbansal16) — Documentation Content  
- *Institute:* IIIT Sonepat, Haryana, India

---

## 📌 Project Objective

To enhance Wireless Sensor Network performance by:
- Dynamically selecting optimal *Cluster Heads (CHs)*
- Reducing overall *energy consumption*
- *Prolonging network lifetime* using fuzzy logic-based inference

---

## 🧠 Core Technologies

- *Frameworks & Tools:*  
  - *Streamlit:* Interactive UI and simulation control  
  - *Pandas:* DataFrame handling for node metrics  
  - *Matplotlib:* Visualization of node deployment and CHs  
  - *NumPy:* Mathematical operations and coordinate generation  

- *Logic System:*  
  - Fuzzy rules with 3 linguistic inputs  
  - Output: ch_probability (Low, Medium, High)  
  - Decision made by max probability across all nodes


---

## ⚙ Key Features

- *Fuzzy-Based CH Selection:*  
  Calculates selection probability using fuzzy rules based on:
  - Residual energy  
  - Distance to base station  
  - Node density  

- *Visual WSN Deployment:*  
  Plots 30 random nodes on a 100x100 field with color-coded CH

- *Dynamic Simulation:*  
  User can select time interval and trigger simulations through UI

- *Automatic Decision Logic:*  
  Selects the most eligible node as CH using fuzzy evaluation

- *Base Station Support:*  
  Fixed BS at center coordinates (50, 50) for distance calculation

---
