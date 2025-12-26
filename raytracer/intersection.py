from dataclasses import dataclass
import numpy as np


@dataclass
class Intersection:
    """
    Represents a ray-surface intersection point
    
    Attributes:
        hit_point: numpy array [x, y, z] - Point where ray hits surface
        normal: numpy array [x, y, z] - Surface normal at hit point (normalized)
        distance: float - Distance from ray origin to hit point
        surface: Surface object that was hit (optional, added by find_nearest_intersection)
    """
    hit_point: np.ndarray
    normal: np.ndarray
    distance: float
    surface: object = None
