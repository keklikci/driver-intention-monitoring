"""Signal names required by the DIM implementation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalColumns:
    """Map the DIM inputs to columns in a drive dataframe."""

    timestamp: str = "timestamp"
    velocity_kmph: str = "velocity_kmph"
    acceleration: str = "acceleration_mps2"
    steering_moment: str = "steering_moment_nm"
    steering_angle_deg: str = "steering_angle_deg"
    lane_departure_warning: str = "lane_departure_warning"
    lane_departure_option: str = "lane_departure_option"
    assisted_driving_mode: str = "assisted_driving_mode"
    curvature_left: str = "curvature_left_radpm"
    curvature_right: str = "curvature_right_radpm"
    lane_y_left: str = "lane_y_left_m"
    lane_y_right: str = "lane_y_right_m"
    geometry: str = "geometry_class"
    steering_angle_velocity: str = "steering_angle_velocity_radps"
    output: str = "dim"
