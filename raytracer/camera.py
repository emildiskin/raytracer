"""
Camera Module - Person 1 Implementation
Handles camera setup and ray generation through pixels
"""

import numpy as np
from ray import Ray


class Camera:
    """
    Camera class for ray tracing
    
    The camera defines the viewpoint and generates rays through each pixel
    of the image plane (screen).
    """
    
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        """
        Initialize camera with position and orientation
        
        Args:
            position: list/array [x, y, z] - Camera position in world space
            look_at: list/array [x, y, z] - Point the camera is looking at
            up_vector: list/array [x, y, z] - Approximate up direction (will be corrected)
            screen_distance: float - Distance from camera to image plane
            screen_width: float - Width of the image plane
            
        Example:
            camera = Camera(
                position=[0, 0, 5],
                look_at=[0, 0, 0],
                up_vector=[0, 1, 0],
                screen_distance=1.0,
                screen_width=2.0
            )
        """
        self.position = np.array(position, dtype=float)
        self.look_at = np.array(look_at, dtype=float)
        self.up_vector = np.array(up_vector, dtype=float)
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        
        # Compute camera coordinate system (forward, right, up)
        self._setup_camera_basis()
    
    def _setup_camera_basis(self):
        """
        Compute camera's orthonormal coordinate system
        
        Creates three perpendicular unit vectors:
        - forward: direction camera is looking (from position to look_at)
        - right: perpendicular to forward and up (points to camera's right)
        - up: perpendicular to forward and right (corrected up direction)
        
        This forms a right-handed coordinate system.
        
        Implementation Notes:
            1. forward = normalize(look_at - position)
            2. right = normalize(cross(forward, up_vector))
            3. up = normalize(cross(right, forward))
        """
        # TODO: Implement camera basis setup
        # 1. Calculate forward direction: self.forward = normalize(self.look_at - self.position)
        # 2. Calculate right direction: self.right = normalize(cross(self.forward, self.up_vector))
        # 3. Calculate corrected up: self.up = normalize(cross(self.right, self.forward))
        
        # Placeholder - replace with actual implementation
        self.forward = np.array([0, 0, -1], dtype=float)
        self.right = np.array([1, 0, 0], dtype=float)
        self.up = np.array([0, 1, 0], dtype=float)
    
    def generate_ray(self, pixel_x, pixel_y, image_width, image_height):
        """
        Generate a ray from camera through a specific pixel
        
        This is the MAIN FUNCTION called by the ray tracer for each pixel.
        
        Args:
            pixel_x: int - X coordinate of pixel (0 to image_width-1)
            pixel_y: int - Y coordinate of pixel (0 to image_height-1)
            image_width: int - Total width of image in pixels
            image_height: int - Total height of image in pixels
            
        Returns:
            Ray object pointing from camera through the pixel center
            
        Example:
            ray = camera.generate_ray(250, 250, 500, 500)  # Center pixel
            
        Implementation Steps:
            1. Calculate aspect ratio and screen height
            2. Convert pixel coordinates to screen coordinates [-0.5, 0.5]
            3. Scale by screen dimensions
            4. Calculate point on screen in world coordinates
            5. Create ray from camera to screen point
        """
        # TODO: Implement ray generation
        # 1. Calculate aspect_ratio = image_width / image_height
        # 2. Calculate screen_height = self.screen_width / aspect_ratio
        # 3. Convert pixel to normalized coordinates:
        #    screen_x = (pixel_x + 0.5) / image_width - 0.5
        #    screen_y = 0.5 - (pixel_y + 0.5) / image_height  # Flip Y
        # 4. Scale to screen dimensions:
        #    screen_x *= self.screen_width
        #    screen_y *= screen_height
        # 5. Calculate screen center: screen_center = self.position + self.forward * self.screen_distance
        # 6. Calculate screen point: screen_point = screen_center + self.right * screen_x + self.up * screen_y
        # 7. Calculate ray direction: ray_direction = screen_point - self.position
        # 8. Return Ray(self.position, ray_direction)
        
        # Placeholder - replace with actual implementation
        return Ray(self.position, [0, 0, -1])
    
    @staticmethod
    def normalize(vector):
        """
        Normalize a vector to unit length
        
        Args:
            vector: numpy array - Vector to normalize
            
        Returns:
            numpy array - Normalized vector (length = 1)
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
