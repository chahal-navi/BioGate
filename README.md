# BioGate

**Mechanistic Interpretability for Upstream Biosecurity Guardrails**

![Hackathon](https://img.shields.io/badge/Hackathon-Submission-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)

## Overview
The Sentinel Pipeline is an upstream biosecurity guardrail designed to intercept malicious pathogenic intent directly within the latent space of generative biology models (like ProteinMPNN). By applying mechanistic interpretability techniques to the structural translation bottleneck, this architecture isolates biological threat geometry before it can be synthesized into physical DNA.

### Key Capabilities:
* **Latent Interception:** Operates on the final decoder layer, catching threats before sequence generation.
* **Polysemantic Disentanglement:** Uses $L_1$-regularized linear probing ($C=0.5$) to prove that generative structural AI defaults to physical heuristics (sequence length), and mathematically isolates true biological intent from these shortcuts.
* **Zero-Shot Generalization:** Successfully intercepts novel, out-of-distribution biological weapons (Ricin, Anthrax, Botulinum) without relying on historical sequence homology (e.g., BLAST).

## Architecture

<img width="1041" height="899" alt="Screenshot 2026-04-25 at 12 22 43 PM" src="https://github.com/user-attachments/assets/232e6aad-2519-461c-82a8-10b3623783e7" />


