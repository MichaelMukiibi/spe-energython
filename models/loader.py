"""Configuration loading: baselines.yaml + point-scenario overrides (deep merge)."""
from __future__ import annotations

import copy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base (override wins on scalars/list)."""
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def load_baseline(scenario: str | None = None, root: Path = ROOT) -> dict:
    """Load the canonical baseline, optionally overridden by a point scenario."""
    cfg = load_yaml(root / "scenarios" / "baselines.yaml")
    if scenario:
        path = root / "scenarios" / f"{scenario}.yaml"
        if path.exists():
            cfg = deep_merge(cfg, load_yaml(path))
        else:
            raise FileNotFoundError(f"Unknown scenario: {scenario}")
    return cfg