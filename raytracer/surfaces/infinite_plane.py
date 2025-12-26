import numpy as np
from intersection import Intersection
from mathutils import normalize


class InfinitePlane:
    def __init__(self, normal, offset, material_index):
        self.normal = np.array(normal, dtype=float)
        self.offset = offset
        self.material_index = material_index
    
    def intersect(self, ray):
        """
        Find intersection of ray with this plane
        
        Args:
            ray: Ray object with origin and direction
            
        Returns:
            Intersection object or None if no intersection
        """
        epsilon = 1e-6

        normalized_normal = normalize(self.normal)
        denom = np.dot(ray.direction, normalized_normal)
        if abs(denom) < epsilon:
            return None  # Ray is parallel to the plane
        
        t = (self.offset - np.dot(ray.origin, normalized_normal)) / denom
        if t < 0.0001:
            return None  # Intersection is behind the ray origin
        
        hit_point = ray.point_at(t)
        normal = self.get_normal(hit_point)
        return Intersection(hit_point=hit_point, normal=normal, distance=t)

    
    def get_normal(self, point):
        """
        Calculate surface normal at a given point on the plane
        
        Args:
            point: numpy array [x, y, z] - Point on plane surface (unused for planes)
            
        Returns:
            numpy array - Normalized surface normal (constant for planes)
        """

        # For infinite planes, the normal is constant everywhere
        return normalize(self.normal)
