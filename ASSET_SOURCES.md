# Manuscript-derived documentation material

Added 2026-10-15 from the Hydro-CPS-Sim manuscript directory provided by the project author. Only selected explanatory material is included; the TeX sources, full PDF, author/affiliation details, raw experimental data and quantitative result plots are not copied into this repository.

| Website asset | Supplied manuscript asset |
| --- | --- |
| `assets/hydro_cps_sim_architecture.png` | `figures/png/hydro_cps_sim_architecture.png` |
| `assets/closed_loop_experiment_workflow.png` | `figures/png/closed_loop_experiment_workflow.png` |
| `assets/ctown_water_topology.png` | `figures/png/ctown_water_topology.png` |
| `assets/attack_cross_layer_propagation_paths.png` | `figures/png/attack_cross_layer_propagation_paths.png` |

Original PNG files are copied unchanged and shared between both languages. Captions identify the manuscript origin; C-Town is the underlying model for the topology illustration. Transparent diagrams are displayed on a white figure background with links to their full-resolution files.

Text adaptations use `01_introduction.tex`, `03_design.tex`, `04_implementation.tex`, `05_experiments.tex` and `07_discussion.tex`. The publication page reports only the working title and the draft status apparent from `main.tex`; no publication metadata is invented.

The research setup differs from the public source presets reviewed at `2406aa649738c585e635b3661d1b9431db73edb8`: manuscript attacks use iterations 15–55 in 80-iteration runs and a PLC7 DoS path; public DoS presets target PLC2 during iterations 5–90. Historical T7 acquisition identifiers also differ. The site explicitly separates these contexts and does not present manuscript settings as verified reproduction commands.

No raw-data audit or simulator execution was performed for this documentation update. Quantitative manuscript claims and performance figures remain unpublished here pending versioned reproduction evidence.
