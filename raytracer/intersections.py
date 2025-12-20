"""
Intersection Module - Person 1 Implementation
Handles ray-surface intersection calculations for spheres, planes, and cubes
"""

import numpy as np
from ray import Ray
from surfaces.sphere import Sphere
from surfaces.infinite_plane import InfinitePlane
from surfaces.cube import Cube


# ============================================================================
# INTERSECTION FUNCTIONS
# ============================================================================

# These functions are deprecated - kept for backwards compatibility
# Use surface.intersect(ray) instead
# All functions now return Intersection objects instead of dictionaries

def intersect_sphere(ray, sphere):
    """Deprecated: Use sphere.intersect(ray) instead. Returns Intersection object or None."""
    return sphere.intersect(ray)


def intersect_plane(ray, plane):
    """Deprecated: Use plane.intersect(ray) instead. Returns Intersection object or None."""
    return plane.intersect(ray)


def intersect_cube(ray, cube):
    """Deprecated: Use cube.intersect(ray) instead. Returns Intersection object or None."""
    return cube.intersect(ray)


# ============================================================================
# MAIN INTERSECTION FUNCTION - USED BY PERSON 2
# ============================================================================

def find_nearest_intersection(ray, surfaces, ignore_surface=None):
    """
    Find the nearest surface intersection along a ray
    
    This is the MAIN FUNCTION that Person 2 will call from lighting.py
    
    Args:
        ray: Ray object with origin and direction
        surfaces: List of all surface objects in the scene (Sphere, Plane, Cube)
        ignore_surface: Optional surface object to ignore (used for reflections
                       to avoid self-intersection)
        
    Returns:
        Intersection object with:
            surface: The surface object that was hit
            hit_point: numpy array [x, y, z] - intersection point
            normal: numpy array [x, y, z] - surface normal (normalized)
            distance: float - distance from ray origin to hit point
        Returns None if no intersection found
        
    Example Usage (from Person 2's code):
        from intersections import find_nearest_intersection
        from ray import Ray
        
        ray = Ray([0, 0, 5], [0, 0, -1])
        intersection = find_nearest_intersection(ray, surfaces)
        
        if intersection:
            hit_point = intersection.hit_point
            normal = intersection.normal
            surface = intersection.surface
            material = materials[surface.material_index - 1]
            # ... compute lighting ...
    
    Implementation Notes:
        1. Initialize nearest_distance = infinity
        2. For each surface in surfaces:
           - Skip if surface == ignore_surface
           - Call appropriate intersection function based on type
           - If intersection found and distance < nearest_distance:
             - Update nearest_distance and nearest_intersection
        3. Add 'surface' key to nearest_intersection dict
        4. Return nearest_intersection (or None if no hits)
    """
    # TODO: Implement find_nearest_intersection
    # 1. Initialize tracking variables:
    #    nearest_intersection = None
    #    nearest_distance = np.inf
    # 2. Loop through each surface in surfaces:
    #    - Skip if surface is ignore_surface
    #    - Call surface.intersect(ray) - all surfaces now have this method!
    #    - If intersection exists and intersection.distance < nearest_distance:
    #      * Update nearest_distance = intersection.distance
    #      * Update nearest_intersection = intersection
    #      * Add surface to intersection: nearest_intersection.surface = surface
    # 3. Return nearest_intersection
    
    return None  # Placeholder


# ============================================================================
# ALTERNATIVE: FUNCTION THAT TAKES RAY COMPONENTS INSTEAD OF RAY OBJECT
# ============================================================================
# Person 2 might call with ray components instead of Ray object
# This wrapper handles both cases

def find_nearest_intersection_from_components(ray_origin, ray_direction, surfaces, ignore_surface=None):
    """
    Wrapper function that accepts ray components instead of Ray object
    
    This allows Person 2 to call the function without creating a Ray object:
        intersection = find_nearest_intersection_from_components(
            ray_origin=camera_position,
            ray_direction=pixel_direction,
            surfaces=all_surfaces
        )
    
    Args:
        ray_origin: numpy array [x, y, z] - Starting point of ray
        ray_direction: numpy array [x, y, z] - Direction of ray
        surfaces: List of all surface objects
        ignore_surface: Optional surface to ignore
        
    Returns:
        Same as find_nearest_intersection()
    """
    ray = Ray(ray_origin, ray_direction)
    return find_nearest_intersection(ray, surfaces, ignore_surface)
