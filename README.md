# CrustChain Simulation Toolkit
Python implementations of core CrustChain mechanisms for reproducibility and validation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
This repository contains simulation code for the CrustChain blockchain framework described in:
> Saha Reno and Koushik Roy. "CrustChain: Resolving the Blockchain Trilemma via Decentralized Storage and Proof-of-Capacity Consensus" (PLOS ONE, 2025)

## Scripts
| File | Description | Key Features |
|------|-------------|-------------|
| `adaptive_sharding.py` | MDP-optimized sharding | Q-learning, latency-aware grouping |
| `spost_challenge.py` | SPoSt proof generation | Arion-Poseidon hashing, sector audit |
| `hybrid_encoding.py` | Erasure-network coding | Reed-Solomon + Network coding |
| `fairswap.py` | Atomic cross-shard commits | Two-phase locking, bond slashing |
| `reputation_consensus.py` | Reputation system | Dynamic scoring, block probability |
| `simulation_runner.py` | Metrics simulator | Throughput, latency, chain quality |
| `bls_threshold.py` | BLS signatures | Threshold crypto, rotation |
| `data_retrieval.py` | Data retrieval | Time-lock puzzles, threshold decoding |
| `node_registration.py` | Node management | Staking, slashing, registry |

## Installation
```bash
git clone https://github.com/renosaha/crustchain-simulations
cd crustchain-simulations
pip install -r requirements.txt

```

## Running Simulations
Execute the main simulation with Byzantine node testing:
```bash
python simulation_runner.py --nodes 1024 --byzantine 0.4 --epochs 1000

```

Key parameters:
--nodes  :   Number of nodes (default: 1024);
--shards  :  Shard count (default: 64);
--byzantine :  Byzantine ratio (default: 0.3);
--epochs  :  Simulation epochs (default: 500)
