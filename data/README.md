# Data

Nothing is stored here. Every dataset used in this paper was published with
Liao et al., *Machine learning for practical quantum error mitigation*,
Nature Machine Intelligence **6**, 1478-1486 (2024), and lives in

> **https://github.com/qiskit-community/blackwater** (Apache-2.0)

Run `python data/fetch_data.py` to clone it and link it into place, or
`--check` to see what is already present.

## What is used

| Purpose | Upstream path | Size |
|---|---|---|
| 100-qubit hardware circuits (`ibm_brisbane`, 500 files, steps 1-10) | `docs/tutorials/data/ising_zne_hardware/100q_brisbane/` | 456 MB |
| Twirl-averaged noise-factor values at noise factors 1 and 3 | `docs/tutorials/zne_mitigated/twirl_100q_brisbane/step{01..10}.json` | 244 KB |
| The eleven simulator benchmark datasets | `docs/tutorials/data/{haoran_mbd,...}` | 5.2 GB |

The second row is what makes the 100-qubit results reproducible without
re-acquiring hardware data: those JSON files are the device measurements, and
everything downstream of them is computed here.

## What this repository adds

The ZNE reduction

    y = nf1 - (nf3 - nf1) / 2

applied to the twirl-averaged values, the stratified 100 train / 400 test
split (`docs/demos/qem_gnn/runs100q/split_100q.json`), and the circuit-to-graph
construction. All three are in `runs100q/build_100q.py`.
