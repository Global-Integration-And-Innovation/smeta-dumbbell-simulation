## 📁 Repository Contents
# SMETA Dumbbell Simulation

A computational visualization of the **SMETA framework**  
(Space–Mass–Energy–Time–Ātman) using a dual-component particle model.

---

## 🧠 Conceptual Model

Each particle is represented as a **dual Ātman system**:

- 🔵 **Ātman A (Interactive / Pulse)**  
  - Drives interaction, motion, attraction–repulsion  
  - Represented as the **blue node**  
  - Dominant during dynamic and peripheral activity  

- 🟡 **Ātman B (Memory / Informational)**  
  - Stores accumulated interaction history  
  - Represented as the **yellow node**  
  - Regulates stabilization and re-formation  

These two components form a **dumbbell structure**, dynamically evolving over time.

---

## 🔄 Emergent Behaviour

The simulation demonstrates:

- Interaction-driven memory formation  
- Memory saturation and decay  
- Dissolution of the interactive component  
- Free-memory phase (yellow-only state)  
- Rebinding of interaction to memory  
- Coexistence of multiple phase states in a single field  

---

## 📊 Phase Structure

Each particle independently evolves through:

1. **ACTIVE** → Interaction-dominated phase  
2. **STEADY** → Memory-stabilized equilibrium  
3. **DISSOLVING** → Interaction fading  
4. **FREE-YELLOW** → Memory-only persistence  
5. **REBINDING** → Reformation of interaction  

Global system phase is defined by **dominant population state**.

---

## ⚙️ Model Features

- Nonlinear interaction field (attraction + repulsion)  
- Memory evolution with saturation:
  
  \[
  \frac{dB}{dt} = \alpha I (1 - \frac{B}{B_{\max}}) - \lambda B
  \]

- Feedback:
  
  Interaction → Memory → Future interaction

- Asynchronous phase cycles across particles  

---

## ▶️ How to Run

```bash
pip install numpy matplotlib
python smeta_dumbbell.py


- `smeta_dumbbell.py` → Main simulation code  
- `README.md` → Documentation  

---

## 👨‍⚕️ Author

**Dr. Rajatsubhra Mukhopadhyay**  
Pediatrician | Independent Researcher  
Director, Child Health Care Arambag  

ORCID: https://orcid.org/0000-0001-5658-8016  

---

## ⚠️ Usage Note

This work represents an original conceptual and computational framework.  
Reproduction, modification, or redistribution should be done with proper attribution.
## 🔗 Related Work (SMETA Framework)

This simulation is part of an ongoing research development of the SMETA framework.

### Foundational Works

1. **SMETA Framework — Version 1.0**  
   Published: 28 January 2026  
   DOI: https://doi.org/10.5281/zenodo.18396901  

2. **Integrated Axiomatic Consolidation (Version 1.1)**  
   Published: 4 February 2026  
   DOI: https://doi.org/10.5281/zenodo.18490160  

3. **SMETA Pamphlet**  
   DOI: https://doi.org/10.5281/zenodo.18979029  

---

These works establish the theoretical foundation of the SMETA model, while the present repository provides a computational realization of the dual Ātman dynamics.

---

## 🔬 Future Directions

- Quantitative validation of phase transitions  
- Analytical formulation of Ātman interaction fields  
- Experimental parameter mapping  
- Integration with SMETA master equation
