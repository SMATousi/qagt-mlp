# QAGT-MLP

Reference implementation for *QAGT-MLP: An Attention-Based Graph Transformer
for Small and Large-Scale Quantum Error Mitigation*.

QAGT-MLP predicts error-mitigated expectation values from a noisy circuit
execution. It encodes the circuit as a graph over gate instances and, for each
measured qubit, pools a local context over that observable's causal lightcone
with a query conditioned on the qubit and on its noisy value, alongside a
graph-wide global context. The model has 292,610 parameters and is linear in
the number of operations in the circuit.

## Layout

The code lives at `docs/demos/qem_gnn/`, mirroring its position in the
upstream repository it builds on, so that every relative data path resolves
unchanged. See NOTICE and THIRD_PARTY.md.

```
docs/demos/qem_gnn/
  circuits_to_graph.py   DAG -> PyG graph; 20-dim node features; both masks
  lightcone.py           causal lightcone and wire masks
  model.py               QAGT-MLP
  qem_ext.py             configurable variant used by every ablation
  qem_train.py           TrainConfig, train_qem, train_ensemble, metrics
  qem_levels.py          discrete-target detection and decoders
  qem_descriptors.py     165-dim circuit descriptors (the RF feature set)
  mlp.py                 Random Forest baseline (upstream; see THIRD_PARTY.md)
  sim_*.ipynb            the eleven benchmark datasets, outputs retained
  02_GNN_Transformer.ipynb   the 100-qubit pipeline
  runs100q/              100-qubit build, training and analysis
  runs_ablation/         descriptor and conditioning ablations
  runs_locality/         generator for circuits of controlled causal coverage
results/                 every JSON the paper's numbers are read from
figures/                 the figures as they appear in the paper
```

## Setup

```bash
pip install -r requirements.txt
python data/fetch_data.py          # datasets from Liao et al.; ~6 GB
python data/fetch_data.py --check  # verify without fetching
```

No dataset is redistributed here. `data/README.md` says what is fetched and
what this repository computes from it.

## Reproducing the paper

Run from `docs/demos/qem_gnn/`. The 100-qubit graphs must be built once
(~25 min); everything else reads them.

```bash
python runs100q/build_100q.py
```

| Paper object | Command |
|---|---|
| Table 1, mask locality | `python runs100q/locality_100q.py` |
| Table 2, 100-qubit results | `python runs100q/train_100q.py` |
| Table 3, eleven-dataset benchmark | the `sim_*.ipynb` notebooks (outputs stored) |
| Table 4, per-qubit conditioning | `python runs_ablation/run_conditioning.py` |
| Table 5, graph vs. descriptors | `python runs_ablation/run_ablation.py` |
| Fig., per-step normalised error | `runs100q/analysis/b1_per_step.py`, then `b1_figure.py` |
| Fig., held-out-step extrapolation | `runs100q/analysis/b2_heldout_step.py`, then `b2_figure.py` |
| Fig., 2^4 factorial ablation | `runs100q/analysis/b4_factorial.py`, then `b4_figure.py` |
| Fig., conditioning ablation | `runs_ablation/run_conditioning.py`, `measure_collapse.py`, then `conditioning_figure.py` |

Each script writes a JSON next to itself; the same files are mirrored in
`results/` so the paper's numbers can be checked without running anything.

Trained checkpoints for the 100-qubit model (five seeds) and for the
held-out-step model are in `runs100q/`.

## Reproducibility note

The graph attention operator uses non-deterministic scatter reductions on GPU,
so a fixed seed does not give bit-identical runs. All headline numbers are
ensembles over five seeds; ablations report three seeds with their spread.
Small differences in the last reported digit are expected.

## Licence

MIT (LICENSE). Portions derive from `qiskit-community/blackwater` under
Apache-2.0 — see NOTICE, LICENSE-APACHE-2.0 and THIRD_PARTY.md. All datasets
are that project's, and are fetched rather than redistributed.
