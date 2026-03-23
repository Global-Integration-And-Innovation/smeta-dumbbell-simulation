# SMETA Dumbbell Simulation

Author
Dr. Rajatsubhra Mukhopadhyay
Pediatrician | Independent Researcher
Director, Child Health Care Arambag
ORCID: https://orcid.org/0000-0001-5658-8016⁠�

## Abstract

This repository presents a computational implementation of the SMETA framework  
(Space–Mass–Energy–Time–Ātman) using a dual-component particle model.  
Each particle is represented as a coupled system consisting of an interactive component and a memory component. The model demonstrates how interaction-driven dynamics generate memory, and how accumulated memory subsequently regulates future interaction, resulting in emergent phase behaviour.

---

## Conceptual Model

Each particle is defined as a dual-component system:

- **Ātman A (Interactive Component)**  
  Governs instantaneous interaction, motion, and attraction–repulsion dynamics.

- **Ātman B (Memory Component)**  
  Stores accumulated interaction history and modulates future evolution.

The system can be interpreted as a coupled interaction–memory framework:

\[
\mathcal{A} = (\mathcal{A}_A, \mathcal{A}_B)
\]

where interaction generates memory and memory feeds back into interaction.

---

## Mathematical Formulation

### Memory Evolution

\[
\frac{dB}{dt} = \alpha I(t)\left(1 - \frac{B}{B_{\max}}\right) - \lambda B
\]

where:

- \( B \) : memory state  
- \( I(t) \) : interaction input  
- \( \alpha \) : memory formation coefficient  
- \( \lambda \) : decay constant  
- \( B_{\max} \) : saturation limit  

### Interaction–Memory Feedback

\[
I(t) = I_0(t) + \beta B
\]

This defines a closed feedback system:

\[
\text{Interaction} \rightarrow \text{Memory} \rightarrow \text{Modified Interaction}
\]

---

## Computational Implementation

The model is implemented using a particle-based simulation with:

- Nonlinear interaction field (attraction–repulsion balance)
- Memory accumulation with saturation and decay
- Time-dependent feedback from memory to interaction
- Asynchronous evolution across particles

Each particle evolves independently while interacting within a shared field.

---

## Emergent Behaviour

The simulation exhibits the following phenomena:

- Interaction-driven memory formation  
- Memory saturation and gradual decay  
- Reduction of interaction intensity  
- Persistence of memory-dominated states  
- Re-emergence of interaction from stored memory  
- Coexistence of multiple dynamical phases  

---

## Phase Structure

Each particle transitions through the following states:

1. **ACTIVE** — interaction-dominated regime  
2. **STEADY** — stabilized memory–interaction balance  
3. **DISSOLVING** — decreasing interaction influence  
4. **MEMORY-DOMINANT** — persistence of memory without active interaction  
5. **REBINDING** — reactivation of interaction from memory  

The global system phase is determined by the dominant population state.

---

## Related Work

This repository is part of the SMETA framework development.
SMETA Framework — Version 1.0
DOI: https://doi.org/10.5281/zenodo.18396901⁠�
Integrated Axiomatic Consolidation (Version 1.1)
DOI: https://doi.org/10.5281/zenodo.18490160⁠�
SMETA Pamphlet
DOI: https://doi.org/10.5281/zenodo.18979029⁠�

These works establish the theoretical foundation of the model.
Scope and Limitations
This work represents a conceptual and computational framework.
The model is not yet experimentally validated.
Parameters are phenomenological and require calibration against measurable systems.

##Future Work

Analytical derivation of interaction fields
Quantitative phase transition analysis
Parameter estimation from physical or biological systems
Integration with the SMETA master equation
Development of experimentally testable predictions

## Citation

If this work is used or referenced, please cite the associated SMETA publications listed above.

## License

All rights reserved by the author.
Reuse is permitted only with proper attribution.

## Repository Contents

- `smeta_dumbbell.py` — simulation code  
- `README.md` — documentation  

---

## Usage

Install required dependencies:

```bash
pip install numpy matplotlib

python smeta_dumbbell.py

