"""
Lighting and Shading Module
Person 2 Implementation: Handles all lighting calculations, shadows, reflections, and transparency
"""

import numpy as np


class LightingEngine:
    """
    Handles all lighting computations including:
    - Phong shading (diffuse + specular)
    - Hard and soft shadows
    - Reflections (recursive)
    - Transparency/refraction
    """
    
    def __init__(self, scene_settings, materials, lights, surfaces):
        """
        Initialize the lighting engine
        
        Args:
            scene_settings: SceneSettings object with background color, shadow rays, max recursion
            materials: List of Material objects
            lights: List of Light objects
            surfaces: List of surface objects (spheres, planes, cubes)
        """
        self.scene_settings = scene_settings
        self.materials = materials
        self.lights = lights
        self.surfaces = surfaces
        self.background_color = np.array(scene_settings.background_color)
        self.max_recursion = int(scene_settings.max_recursions)
        self.num_shadow_rays = int(scene_settings.root_number_shadow_rays)
    
    def compute_color(self, ray_origin, ray_direction, intersection_data, recursion_depth=0):
        """
        Main color computation function - integrates all lighting effects
        
        Args:
            ray_origin: Origin point of the ray (camera or reflection point)
            ray_direction: Direction vector of the ray (normalized)
            intersection_data: Dict with keys: 'surface', 'hit_point', 'normal', 'distance'
            recursion_depth: Current recursion level for reflections
            
        Returns:
            RGB color as numpy array [r, g, b] in range [0, 255]
        """
        if intersection_data is None:
            return self.background_color
        
        # Extract intersection information
        surface = intersection_data['surface']
        hit_point = intersection_data['hit_point']
        normal = intersection_data['normal']
        
        # Get material properties
        material = self.materials[surface.material_index - 1]  # material_index is 1-based
        
        # Initialize color components
        diffuse_specular_color = np.zeros(3)
        reflection_color = np.zeros(3)
        background_color = np.zeros(3)
        
        # 1. Compute diffuse and specular lighting from all lights
        for light in self.lights:
            light_contribution = self.compute_light_contribution(
                hit_point, normal, ray_direction, material, light
            )
            diffuse_specular_color += light_contribution
        
        # 2. Compute reflections (if material is reflective and recursion limit not reached)
        if recursion_depth < self.max_recursion and np.any(material.reflection_color > 0):
            reflection_color = self.compute_reflection(
                hit_point, ray_direction, normal, material, recursion_depth
            )
        
        # 3. Compute transparency (background objects visible through transparent surface)
        if material.transparency > 0:
            background_color = self.compute_transparency(
                hit_point, ray_direction, material, recursion_depth
            )
        
        # 4. Combine all color components using the transparency formula
        # output_color = (background_color * transparency) + 
        #                (diffuse + specular) * (1 - transparency) + 
        #                reflection_color
        final_color = (
            background_color * material.transparency +
            diffuse_specular_color * (1 - material.transparency) +
            reflection_color
        )
        
        # Clamp to valid RGB range [0, 255]
        return np.clip(final_color, 0, 255)
    
    def compute_light_contribution(self, hit_point, normal, view_direction, material, light):
        """
        Compute the contribution of a single light source using Phong shading model
        
        Args:
            hit_point: Point on surface being lit
            normal: Surface normal at hit point (normalized)
            view_direction: Direction from hit point to camera (normalized)
            material: Material object with diffuse, specular, shininess properties
            light: Light object
            
        Returns:
            RGB color contribution from this light [r, g, b]
        """
        # TODO: Implement Phong lighting
        # 1. Calculate light_direction (from hit_point to light)
        # 2. Check if light is visible (compute shadow with soft shadows)
        # 3. Calculate diffuse component: max(0, dot(normal, light_direction))
        # 4. Calculate specular component using Phong model:
        #    - reflection_direction = reflect(-light_direction, normal)
        #    - specular = max(0, dot(view_direction, reflection_direction))^shininess
        # 5. Combine: light_color * (diffuse_color * diffuse + specular_color * specular * specular_intensity)
        # 6. Multiply by light_intensity from shadow calculation
        
        return np.zeros(3)  # Placeholder
    
    def compute_shadow_intensity(self, hit_point, light):
        """
        Compute shadow intensity using soft shadows (N×N shadow rays)
        
        Args:
            hit_point: Point on surface to check for shadows
            light: Light object
            
        Returns:
            float: Light intensity at hit_point (0.0 = fully shadowed, 1.0 = fully lit)
        """
        # TODO: Implement soft shadows
        # 1. If num_shadow_rays == 1, do simple hard shadow (one ray to light)
        # 2. Otherwise, create N×N grid on plane perpendicular to light direction
        # 3. For each cell in grid:
        #    - Pick random point in cell
        #    - Shoot ray from hit_point to that point
        #    - Check if ray intersects any surface before reaching light
        # 4. Count how many rays hit the surface vs total rays
        # 5. Apply formula: (1 - shadow_intensity) + shadow_intensity * (hit_ratio)
        
        # BONUS: Account for transparency of objects in the way
        
        return 1.0  # Placeholder (fully lit, no shadows)
    
    def compute_reflection(self, hit_point, incident_direction, normal, material, recursion_depth):
        """
        Compute reflection color by shooting reflection ray
        
        Args:
            hit_point: Point where ray hit the surface
            incident_direction: Direction of incoming ray (normalized)
            normal: Surface normal (normalized)
            material: Material object
            recursion_depth: Current recursion level
            
        Returns:
            RGB color from reflection [r, g, b]
        """
        # TODO: Implement reflections
        # 1. Calculate reflection direction: incident - 2 * dot(incident, normal) * normal
        # 2. Shoot new ray from hit_point in reflection direction
        # 3. Find nearest intersection (call Person 1's intersection function)
        # 4. Recursively compute color at intersection (recursion_depth + 1)
        # 5. Multiply result by material.reflection_color
        
        return np.zeros(3)  # Placeholder
    
    def compute_transparency(self, hit_point, ray_direction, material, recursion_depth):
        """
        Compute color of objects behind transparent surface
        
        Args:
            hit_point: Point on transparent surface
            ray_direction: Direction of ray through surface
            material: Material object
            recursion_depth: Current recursion level
            
        Returns:
            RGB color of background objects [r, g, b]
        """
        # TODO: Implement transparency
        # 1. Continue ray in same direction from hit_point
        # 2. Find next intersection (call Person 1's intersection function)
        # 3. Recursively compute color at that intersection (recursion_depth + 1)
        # 4. Return the color (will be multiplied by transparency in main function)
        
        return self.background_color  # Placeholder
    
    def normalize(self, vector):
        """Utility: Normalize a vector"""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    def reflect(self, incident, normal):
        """
        Utility: Reflect incident vector around normal
        Formula: incident - 2 * dot(incident, normal) * normal
        """
        return incident - 2 * np.dot(incident, normal) * normal


# ============================================================================
# INTEGRATION WITH PERSON 1's CODE
# ============================================================================
# Person 1 will implement these functions in intersections.py
# Import them here once Person 1's code is ready:
# from intersections import find_nearest_intersection
# ============================================================================

def find_nearest_intersection(ray_origin, ray_direction, surfaces, ignore_surface=None):
    """
    PLACEHOLDER - Person 1 will implement this in intersections.py
    
    Find the nearest surface intersection along a ray
    
    Args:
        ray_origin: numpy array [x, y, z] - Starting point of ray
        ray_direction: numpy array [x, y, z] - Direction of ray (normalized)
        surfaces: List of all surfaces in scene (Sphere, Plane, Cube objects)
        ignore_surface: Optional surface object to ignore (for reflections)
        
    Returns:
        Dictionary with keys:
            'surface': The surface object that was hit
            'hit_point': numpy array [x, y, z] of intersection point
            'normal': numpy array [x, y, z] of surface normal (normalized)
            'distance': float - distance from ray_origin to hit_point
        Returns None if no intersection found
    
    Example return value:
        {
            'surface': sphere_object,
            'hit_point': np.array([1.5, 2.0, 3.0]),
            'normal': np.array([0.0, 1.0, 0.0]),
            'distance': 5.2
        }
    
    Person 1's Implementation Notes:
        1. Create Ray object from ray_origin and ray_direction
        2. For each surface in surfaces:
           - Skip if surface == ignore_surface
           - Check intersection based on type (Sphere/Plane/Cube)
           - Track nearest intersection
        3. Return nearest intersection with all required fields
        4. Return None if no valid intersection found
    """
    # TEMPORARY PLACEHOLDER - Remove when Person 1's code is ready
    # This allows Person 2 to test lighting without Person 1's code
    return None
