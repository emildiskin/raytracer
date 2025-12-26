import numpy as np
from intersection import Intersection


class Sphere:
    def __init__(self, position, radius, material_index):
        self.position = np.array(position, dtype=float)
        self.radius = radius
        self.material_index = material_index
    
    def intersect(self, ray):
        """
        Find intersection of ray with this sphere
        
        Args:
            ray: Ray object with origin and direction
            
        Returns:
            Intersection object or None if no intersection
        """
        # TODO: Implement sphere intersection
        # 1. Calculate vector from ray origin to sphere center: oc = ray.origin - self.position
        # 2. Calculate quadratic coefficients:
        #    a = dot(ray.direction, ray.direction)
        #    b = 2.0 * dot(oc, ray.direction)
        #    c = dot(oc, oc) - self.radius²
        # 3. Calculate discriminant: b² - 4ac
        # 4. If discriminant < 0: return None (no intersection)
        # 5. Calculate t values: t = (-b ± sqrt(discriminant)) / 2a
        # 6. Choose nearest positive t (> 0.0001 to avoid self-intersection)
        # 7. Calculate hit_point = ray.point_at(t)
        # 8. Calculate normal using get_normal(hit_point)
        # 9. Return Intersection(hit_point=hit_point, normal=normal, distance=t)

        oc = ray.origin - self.position

        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None
        
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        t = None
        if t1 > 0.0001:
            t = t1
        elif t2 > 0.0001:
            t = t2
        if t is None:
            return None
        
        hit_point = ray.point_at(t)
        normal = self.get_normal(hit_point)
        return Intersection(hit_point=hit_point, normal=normal, distance=t)
    
    
    def get_normal(self, point):
        """
        Calculate surface normal at a given point on the sphere
        
        Args:
            point: numpy array [x, y, z] - Point on sphere surface
            
        Returns:
            numpy array - Normalized surface normal pointing outward
        """

        # Normal = (point - center) / radius
        normal = (point - self.position) / self.radius
        return normal
