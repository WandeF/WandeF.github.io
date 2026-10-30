# Source review · 2026-10-15

Reviewed read-only: [WandeF/hydro-cps-sim @ 2406aa649738c585e635b3661d1b9431db73edb8](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8).

- `install.sh`: Ubuntu 22.04/24.04 x86_64; normal user plus sudo; Conda Python 3.10; `--dry-run`, `--env`, `--parent`, `--jobs`. Builds OpenPLC CLI and ns-3; rewrites five top-level paths in every C-Town YAML; runs unit tests and an EPANET library-load smoke check.
- `requirements.txt`: pinned dependencies; EPANET wrapper installed separately from pinned DHALSIM-epynet checkout.
- `scripts/run_all.sh`: default C-Town YAML; configuration, iterations and timing options; output `reports/csv`; clears previous runtime/reports/generated PLC directories on each run. Document preserving results before another run.
- `examples/c_town/*.yaml`: baseline plus six attack presets. Current topology is PLC1–PLC8. Some filenames retain historical PLC9 naming. Do not infer targets from filenames.
- `src/attack/{launch,modbus_mitm,udp_dos,openplc_logic}.py`: implementations exist. No attack success claim or fabricated measurement is made.
- `src/io/export_results.py`: physics, actuator, observation, attack, timeout and timing CSV exports.
- Upstream `README_attack_mitm.md` refers to missing `config_mitm.yaml` and `scripts/compare_attack_results.py`. These stale commands are deliberately excluded. Use actual YAML names and the runner instead.
- Baseline defaults: 100 iterations; EPANET duration 86400 seconds, hydraulic step 300 seconds, `noise_scale: 0.0`; PLC4 consumes remote T5 and T7. Exact current fields remain defined by source.

Validation scope: website build, generated HTML/local links, bilingual search index and deployment configuration. No installation of simulator dependencies, privileged network setup, or full water-network simulation was performed for this documentation task. Repository source code was not changed. Runtime replication, figures, official citation metadata and licensing remain follow-up work.

## Manuscript documentation update

Architecture, workflow, C-Town dependencies and research-method descriptions were added from the author-provided manuscript on 2026-10-15. See `ASSET_SOURCES.md` for figure provenance and the distinction between manuscript scenarios and reviewed public presets. This does not extend the runtime validation scope above.

## UPSI and configuration update · 2026-10-29

Reviewed local project `/home/lzh/MASTER/CODE/hydro-cps-sim`, branch UPSI, commit d7fafbd. This section extends the earlier water-only source review.

- Reviewed base/types, registry/factory, session, normalization/config, signal_mapper/units, time_coordinator/quality, both native adapters, legacy policy, thermal plugin, PLC/SCADA transport, network generators and attack implementations.
- Added an explicit architecture boundary for UPSI, a standalone Chinese explanation in the author's output directory, paired English/Chinese extension tutorials and field dictionaries.
- Configuration distinguishes actual consumed options from descriptive/historical fields. In particular endpoint tap_mode drives ns-3 access; top-level taps/applications/attack_points are not substitutes for executable network and attack settings. noise_scale/log_level and ascii_trace are not implemented generic controls in the current path.
- Checked conceptual references against official FMI 3.0.2, mosaik API, YAML 1.2.2, PyYAML, Python package metadata and Modbus V1.1b3 documentation. UPSI is a project API; no FMU import, FMI conformance or simultaneous multi-backend coupling is claimed.
- Build: 32 bilingual content pages plus root redirect, 32 complete search records, internal links and heading anchors checked. Navigation/search/language switching and narrow-page presentation are checked in the local browser.
- Existing real-experiment evidence was read for examples; this documentation task does not rerun privileged simulations. The previous 90-test/full-loop validation belongs to the software integration work, not to a new test claim here.

The footer and badge now use neutral project documentation labels as part of the requested wording revision. Deployment workflow, repository remotes, manuscript originals and raw experiment results are unchanged. This update is locally built; no push or deployment is part of this documentation task.

## Wording and structure revision · 2026-10-29

The basic configuration pages now introduce the original C-Town fields and examples. UPSI schema, typed signals, units, time and quality settings are documented separately under Extensions. Chinese and English introductions use a tutorial style following CPSim's component-and-task organization. The architecture extends the original artwork rather than replacing its visual style; see ASSET_SOURCES.md for the rendering method. No simulator code or raw experiment results were changed.
