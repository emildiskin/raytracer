import numpy as np


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
            Dictionary with 'hit_point', 'normal', 'distance' or None if no intersection
        """
        # TODO: Implement cube intersection using slabs method
        # 1. Calculate cube bounds:
        #    half_size = self.scale / 2
        #    min_bound = self.position - half_size
        #    max_bound = self.position + half_size
        # 2. Initialize: t_min = -inf, t_max = inf, hit_normal = [0,0,0]
        # 3. For each axis i in [0, 1, 2] (X, Y, Z):
        #    a. If |ray.direction[i]| < 1e-6 (ray parallel to slab):
        #       - If ray.origin[i] outside bounds: return None
        #    b. Else:
        #       - Calculate t1 = (min_bound[i] - ray.origin[i]) / ray.direction[i]
        #       - Calculate t2 = (max_bound[i] - ray.origin[i]) / ray.direction[i]
        #       - Ensure t1 <= t2 (swap if needed)
        #       - If t1 > t_min: update t_min = t1 and set hit_normal for this axis
        #       - If t2 < t_max: update t_max = t2
        #       - If t_min > t_max: return None (slabs don't overlap)
        # 4. If t_min < 0.0001: check t_max, or return None
        # 5. Calculate hit_point = ray.point_at(t_min)
        # 6. Normal is already calculated and stored in hit_normal during slab testing
        # 7. Return {'hit_point': hit_point, 'normal': hit_normal, 'distance': t_min}
        
        return None  # Placeholder
    
    def get_normal(self, point):
        """
        Calculate surface normal at a given point on the cube
        
        Args:
            point: numpy array [x, y, z] - Point on cube surface
            
        Returns:
            numpy array - Normalized surface normal pointing outward
        """
        # TODO: Implement normal calculation
        # For cubes, determine which face the point is on:
        # 1. Calculate distance from point to each of 6 faces
        # 2. The face with smallest distance determines the normal
        # 3. Normals are: ±[1,0,0], ±[0,1,0], ±[0,0,1]
        # Note: For cube intersection, normal is calculated during intersection,
        # so this method might not be needed. But it's useful for consistency.
        
        return np.array([0, 1, 0], dtype=float)  # Placeholder
