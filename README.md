# OIF Systems Intelligence

**Offline host inventory normalization and software change detection.**

This repository helps an operator compare two explicitly supplied system inventory snapshots. It focuses on the system layer: operating system, hardware profile, installed software, and observed changes over time. It does not perform network discovery, remote administration, or background telemetry collection.

## Implemented

- Inventory structure validation for host identity, observation time, OS, hardware, and software.
- Duplicate package detection using case-insensitive names.
- Deterministic comparison of software additions, removals, and version changes.
- Command-line JSON report.
- Unit tests and fictional before/after fixtures.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
oif-system-diff examples/before.json examples/after.json
```

The example fixtures intentionally describe a fictional workstation.

## Input shape

Each inventory contains:
- `host_id`: stable local identifier chosen by the operator.
- `observed_at`: timestamp of the snapshot.
- `operating_system`: OS name and version.
- `hardware`: declared CPU, memory, and other attributes.
- `software`: array of package names and versions.

## Operational boundaries

Inventory files can expose hostnames, usernames, software versions, and infrastructure details. Collect only from systems you own or are authorized to assess. Redact sensitive values before sharing. A package inventory is not a vulnerability scan and does not establish whether a host is secure.

## Ecosystem boundary

This project owns offline system-state comparison. Model memory estimates are handled by [OIF Model Intelligence](https://github.com/HuffmanMainNode/OIF-Model-Intelligence); distributed resource assignment is handled by [OI Swarm Intelligence](https://github.com/HuffmanMainNode/OI-Swarm-Intelligence).
