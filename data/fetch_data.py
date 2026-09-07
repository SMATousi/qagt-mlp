#!/usr/bin/env python3
"""Fetch the datasets this work is evaluated on.

Every circuit set and every label file used in the paper was published with

    H. Liao et al., "Machine learning for practical quantum error mitigation",
    Nature Machine Intelligence 6, 1478-1486 (2024)
    https://github.com/qiskit-community/blackwater   (Apache-2.0)

and none of it is redistributed here. This script clones that repository and
places its `docs/tutorials` tree where the notebooks and scripts expect it,
namely two levels above `docs/demos/qem_gnn/`, which is the same relative
position it occupies upstream.

    python data/fetch_data.py            # clone and link (~6 GB)
    python data/fetch_data.py --check    # report what is present, fetch nothing
"""
import argparse, os, subprocess, sys

REPO = "https://github.com/qiskit-community/blackwater"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTERNAL = os.path.join(ROOT, "external", "blackwater")
LINK = os.path.join(ROOT, "docs", "tutorials")

NEEDED = [
    "docs/tutorials/data/ising_zne_hardware/100q_brisbane",
    "docs/tutorials/zne_mitigated/twirl_100q_brisbane",
    "docs/tutorials/data/haoran_mbd",
    "docs/tutorials/data/haoran_mbd_coherent",
    "docs/tutorials/data/ising_dataset",
    "docs/tutorials/data/ising_dataset_random_init",
    "docs/tutorials/data/ising_init_0110",
    "docs/tutorials/data/ising_init_from_qasm",
    "docs/tutorials/data/ising_init_from_qasm_coherent",
    "docs/tutorials/data/ising_init_from_qasm_no_readout",
    "docs/tutorials/data/mbd_datasets2",
]


def check():
    missing = [p for p in NEEDED
               if not os.path.isdir(os.path.join(ROOT, p))]
    for p in NEEDED:
        print(("  ok      " if p not in missing else "  MISSING ") + p)
    print(f"\n{len(NEEDED) - len(missing)}/{len(NEEDED)} present")
    return not missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report what is present and exit")
    args = ap.parse_args()

    if args.check:
        sys.exit(0 if check() else 1)

    if not os.path.isdir(EXTERNAL):
        os.makedirs(os.path.dirname(EXTERNAL), exist_ok=True)
        print(f"cloning {REPO} -> external/blackwater (this is ~6 GB)")
        subprocess.check_call(["git", "clone", "--depth", "1", REPO, EXTERNAL])
    else:
        print("external/blackwater already present, not re-cloning")

    os.makedirs(os.path.dirname(LINK), exist_ok=True)
    if not os.path.exists(LINK):
        os.symlink(os.path.join(EXTERNAL, "docs", "tutorials"), LINK)
        print(f"linked docs/tutorials -> external/blackwater/docs/tutorials")

    print()
    if check():
        print("\nall datasets present; see README.md for what to run")
    else:
        print("\nsome paths are missing -- upstream layout may have changed")
        sys.exit(1)


if __name__ == "__main__":
    main()
