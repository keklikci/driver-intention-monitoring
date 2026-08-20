# Migration notes

The research workspace mixed reusable DIM logic with local execution scripts,
environment-specific signal configuration, raw field data paths, generated reports, and
experiment outputs. This repository retains only a data-independent implementation in
a tested package:

| Original area | Repository replacement |
| --- | --- |
| geometry lookup and classification | `geometry.py` |
| DIM thresholding and event postprocessing | `monitor.py` |
| lane-event segmentation | `segmentation.py` |
| derived vehicle features | `features.py` |
| CWT and Fourier transforms | `transforms.py` |
| classifier initialization and voting | `modeling.py` |

The repository deliberately omits local data ingestion, vehicle/session enumeration,
employer-specific field names, output directories, model binaries, and plotting scripts.
Those components cannot be made reproducible or safely published without a permitted,
sanitized dataset and an explicit data-release decision.
