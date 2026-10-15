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
