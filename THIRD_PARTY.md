# Third-party code and data

## Data — all of it

Every circuit set and every label file used in this paper comes from the
public release accompanying Liao et al., *Machine learning for practical
quantum error mitigation*, Nature Machine Intelligence **6**, 1478-1486 (2024):

> https://github.com/qiskit-community/blackwater  (Apache-2.0)

Nothing is redistributed here. `data/fetch_data.py` retrieves it. This covers:

| What | Upstream path |
|---|---|
| 100-qubit Brisbane circuits, 500 files, steps 1-10 | `docs/tutorials/data/ising_zne_hardware/100q_brisbane/` |
| Twirl-averaged noise-factor values (the ZNE inputs) | `docs/tutorials/zne_mitigated/twirl_100q_brisbane/step{01..10}.json` |
| The eleven simulator benchmark datasets | `docs/tutorials/data/{haoran_mbd,haoran_mbd_coherent,ising_dataset,ising_dataset_random_init,ising_init_0110,ising_init_from_qasm,ising_init_from_qasm_coherent,ising_init_from_qasm_no_readout,mbd_datasets2}/` |

What this work adds to that data is the reduction, not the measurements: the
ZNE estimate `y = nf1 - (nf3 - nf1)/2` applied to the twirl-averaged values,
the stratified 100/400 split, and the graph construction. Those are in
`runs100q/build_100q.py` and `runs100q/split_100q.json`, and are MIT-licensed
along with the rest of this repository.

## Code

| File | Relationship to upstream |
|---|---|
| `mlp.py` | **Derived** from `blackwater/library/learning/mlp.py`. Retains the upstream feature encoders, including `encode_data_v2_ecr`, which defines the Random Forest baseline this paper compares against. Modified to expose the encoder separately so the same features can be fed to the graph model (see `qem_descriptors.py`). |
| `model.py`, `train_loop.py`, `dataset.py`, `featurizers.py`, `schemas.py`, `data_utils.py`, `sim_data_utils.py`, `utils.py` | Written for this work within a fork of the upstream repository, following its conventions and data formats. Where fragments originate upstream they are covered by the Apache-2.0 notice above. |
| `circuits_to_graph.py`, `lightcone.py`, `qem_ext.py`, `qem_train.py`, `qem_levels.py`, `qem_descriptors.py`, everything under `runs100q/`, `runs_ablation/`, `runs_locality/` | New in this work. |

The Random Forest baseline reported in the paper is upstream's own model, run
unmodified on the same circuits and splits as QAGT-MLP.
