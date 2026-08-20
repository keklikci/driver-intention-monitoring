# Driver Intention Monitoring

This repository provides a standalone, data-independent research implementation of a
driver-intention-monitoring workflow.

It accompanies the master's thesis *Field Effectiveness Evaluation of Driver Intention
Monitoring in Lane Keeping Assist*. The package classifies road geometry and produces a
research decision for each intervention event.

## Publication and privacy boundary

I have included the [published master's
thesis](docs/kaan-gueney-keklikci-masters-thesis.pdf) here. It remains all rights
reserved; see the [thesis rights notice](docs/thesis-rights.md).

This public repository excludes raw field data, vehicle identifiers,
employer-specific signal names, calibrated parameters, empirical metrics, and
deployment logic. Read the [public research overview](docs/public-research-overview.md)
and [publication boundary](docs/publication-boundary.md) before using the code.

## Install

This project uses [uv](https://docs.astral.sh/uv/) for environments, dependency
resolution, and commands.

```sh
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Use

```python
import pandas as pd

from driver_intention_monitoring import (
    DimMonitor,
    GeometryThresholds,
    MonitorThresholds,
    SignalColumns,
    classify_geometry,
)

columns = SignalColumns()
geometry_thresholds = GeometryThresholds(
    speeds_kmph=(10.0, 20.0),
    curvatures_radpm=(0.02, 0.01),
)
monitor_thresholds = MonitorThresholds(
    speeds_mps=(5.0, 10.0),
    steering_moment_nm=(0.5, 0.4),
    acceleration_mps2=(0.3, 0.2),
    deceleration_mps2=(0.4, 0.3),
    steering_velocity_radps=(0.6, 0.5),
)
drive = pd.read_parquet("drive.parquet")
drive = classify_geometry(drive, columns, geometry_thresholds)
result = DimMonitor(monitor_thresholds, columns).run(drive)
```

For privacy reasons, the values are conceptually set and do not match the actual
parameters used in the implementation.

See the [documentation index](docs/README.md), [data contract](docs/data-contract.md),
[method overview](docs/method.md), and [thesis record](docs/thesis.md).

## Development

Run the full local quality gate before opening a pull request.

```sh
uv run ruff format .
uv run ruff check --fix .
uv run pytest
```

The package uses caller-supplied threshold configurations. Legacy scripts that depend
on local paths, credentials, data, and generated outputs are not included.
