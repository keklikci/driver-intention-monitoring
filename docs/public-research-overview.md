# Public research overview

This repository provides a standalone, data-independent research implementation of a
driver-intention-monitoring workflow. It accepts a caller-defined dataframe schema,
derives lightweight signal features, classifies road geometry, and produces an
event-level research decision.

The implementation is intended for method inspection, testing, and educational use.
It does not include a dataset, a trained deployment artifact, or a validated vehicle
control strategy.

## Configuring an experiment

Road geometry and monitoring thresholds are required from the caller. The following
small configuration is synthetic and is suitable only for examples and tests:

```python
from driver_intention_monitoring import GeometryThresholds, MonitorThresholds

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
```

For privacy reasons, the values are conceptually set and do not match the actual
parameters used in the implementation.

See the [data contract](data-contract.md) and [method overview](method.md) for the
required inputs and processing stages.
