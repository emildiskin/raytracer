import numpy as np
from intersection import Intersection


class Cube:
    def __init__(self, position, scale, material_index):
        self.position = np.array(position, dtype=float)
        self.scale = scale
        self.material_index = material_index
    
    def intersect(self, ray):
        """
        Find intersection of ray with this cube using slabs method
        
        Args:
            ray: Ray object with origin and direction
            
        Returns:
            Intersection object or None if no intersection
        """

        half_size = self.scale / 2
        min_bound = self.position - half_size
        max_bound = self.position + half_size

        t_min = -np.inf
        t_max = np.inf
        hit_normal = np.array([0.0, 0.0, 0.0], dtype=float)

        for i in range(3):  # For X, Y, Z axes
            if abs(ray.direction[i]) < 1e-6:
                # Ray is parallel to slab
                if ray.origin[i] < min_bound[i] or ray.origin[i] > max_bound[i]:
                    return None  # No intersection
            else:
                t1 = (min_bound[i] - ray.origin[i]) / ray.direction[i]
                t2 = (max_bound[i] - ray.origin[i]) / ray.direction[i]
                if t1 > t2:
                    t1, t2 = t2, t1  # Swap

                if t1 > t_min:
                    t_min = t1
                    hit_normal = np.array([0.0, 0.0, 0.0], dtype=float)
                    hit_normal[i] = -1.0 if ray.direction[i] > 0 else 1.0

                if t2 < t_max:
                    t_max = t2

                if t_min > t_max:
                    return None  # No intersection
                
        if t_min < 0.0001:
            if t_max < 0.0001:
                return None  # Both intersections behind ray
            else:
                t_min = t_max  # Use t_max if t_min is behind
        
        hit_point = ray.point_at(t_min)

        return Intersection(hit_point=hit_point, normal=hit_normal, distance=t_min)
    
    def get_normal(self, point):
        """
        Calculate surface normal at a given point on the cube
        
        Args:
            point: numpy array [x, y, z] - Point on cube surface
            
        Returns:
            numpy array - Normalized surface normal pointing outward
        """
        for i in range(3):
            half_size = self.scale / 2
            if abs(point[i] - (self.position[i] + half_size)) < 1e-6:
                normal = np.array([0.0, 0.0, 0.0], dtype=float)
                normal[i] = 1.0
                return normal
            elif abs(point[i] - (self.position[i] - half_size)) < 1e-6:
                normal = np.array([0.0, 0.0, 0.0], dtype=float)
                normal[i] = -1.0
                return normal
