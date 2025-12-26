import numpy as np


class Ray:
    """
    Represents a ray in 3D space
    
    A ray is defined by: P(t) = origin + t * direction
    where t >= 0
    """
    
    def __init__(self, origin, direction):
        """
        Create a ray with given origin and direction
        
        Args:
            origin: numpy array [x, y, z] or list - Starting point of the ray
            direction: numpy array [x, y, z] or list - Direction vector (will be normalized)
        """
        self.origin = np.array(origin, dtype=float)
        self.direction = self.normalize(np.array(direction, dtype=float))
    
    def point_at(self, t):
        """
        Get point along ray at parameter t
        
        Formula: P(t) = origin + t * direction
        
        Args:
            t: float - Distance parameter along ray (t >= 0)
            
        Returns:
            numpy array [x, y, z] - Point at distance t along the ray
        """
        return self.origin + t * self.direction
    
    @staticmethod
    def normalize(vector):
        """
        Normalize a vector to unit length
        
        Args:
            vector: numpy array - Vector to normalize
            
        Returns:
            numpy array - Normalized vector (length = 1)
            
        Note:
            Returns original vector if length is 0 (to avoid division by zero)
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Ray(origin={self.origin}, direction={self.direction})"
