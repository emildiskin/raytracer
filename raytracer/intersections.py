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

def intersect_sphere(ray, sphere):
    """
    Find intersection of ray with sphere using quadratic formula
    
    Mathematical Background:
        Sphere equation: |P - C|² = r²
        Ray equation: P(t) = O + tD
        Substitute ray into sphere: |O + tD - C|² = r²
        Expand to quadratic: at² + bt + c = 0
        where:
            a = D·D (always 1 since direction is normalized)
            b = 2(O-C)·D
            c = (O-C)·(O-C) - r²
    
    Args:
        ray: Ray object with origin and direction
        sphere: Sphere object with position (center) and radius
        
    Returns:
        Dictionary with keys:
            'hit_point': numpy array [x, y, z] - intersection point
            'normal': numpy array [x, y, z] - surface normal (normalized)
            'distance': float - distance from ray origin to hit point
        Returns None if no intersection
        
    Example:
        ray = Ray([0, 0, 5], [0, 0, -1])
        sphere = Sphere([0, 0, 0], 1.0, 1)
        result = intersect_sphere(ray, sphere)
        # result = {'hit_point': [0, 0, 1], 'normal': [0, 0, 1], 'distance': 4.0}
    """
    # TODO: Implement sphere intersection
    # 1. Calculate vector from ray origin to sphere center: oc = ray.origin - sphere.position
    # 2. Calculate quadratic coefficients:
    #    a = dot(ray.direction, ray.direction)
    #    b = 2.0 * dot(oc, ray.direction)
    #    c = dot(oc, oc) - sphere.radius²
    # 3. Calculate discriminant: b² - 4ac
    # 4. If discriminant < 0: return None (no intersection)
    # 5. Calculate t values: t = (-b ± sqrt(discriminant)) / 2a
    # 6. Choose nearest positive t (> 0.0001 to avoid self-intersection)
    # 7. Calculate hit_point = ray.point_at(t)
    # 8. Calculate normal = (hit_point - sphere.position) / sphere.radius
    # 9. Return {'hit_point': hit_point, 'normal': normal, 'distance': t}
    
    return None  # Placeholder


def intersect_plane(ray, plane):
    """
    Find intersection of ray with infinite plane
    
    Mathematical Background:
        Plane equation: P·N = c (where N is normal, c is offset)
        Ray equation: P(t) = O + tD
        Substitute: (O + tD)·N = c
        Solve for t: t = (c - O·N) / (D·N)
    
    Args:
        ray: Ray object with origin and direction
        plane: InfinitePlane object with normal and offset
        
    Returns:
        Dictionary with keys:
            'hit_point': numpy array [x, y, z] - intersection point
            'normal': numpy array [x, y, z] - surface normal (normalized)
            'distance': float - distance from ray origin to hit point
        Returns None if no intersection (ray parallel to plane or behind ray)
        
    Example:
        ray = Ray([0, 5, 0], [0, -1, 0])
        plane = InfinitePlane([0, 1, 0], 0, 1)  # Horizontal plane at y=0
        result = intersect_plane(ray, plane)
        # result = {'hit_point': [0, 0, 0], 'normal': [0, 1, 0], 'distance': 5.0}
    """
    # TODO: Implement plane intersection
    # 1. Normalize plane normal: normal = plane.normal / |plane.normal|
    # 2. Calculate denominator: denom = dot(ray.direction, normal)
    # 3. If |denom| < 1e-6: return None (ray parallel to plane)
    # 4. Calculate t: t = (plane.offset - dot(ray.origin, normal)) / denom
    # 5. If t < 0.0001: return None (intersection behind ray)
    # 6. Calculate hit_point = ray.point_at(t)
    # 7. Return {'hit_point': hit_point, 'normal': normal, 'distance': t}
    
    return None  # Placeholder


def intersect_cube(ray, cube):
    """
    Find intersection of ray with axis-aligned cube using slabs method
    
    Mathematical Background:
        The slabs method treats the cube as the intersection of 3 pairs of
        parallel planes (slabs), one pair for each axis (X, Y, Z).
        
        For each axis:
        1. Calculate t values where ray enters and exits the slab
        2. Track the maximum entry t (t_min) and minimum exit t (t_max)
        3. If t_min > t_max at any point, ray misses the cube
        4. The face corresponding to t_min determines the hit normal
    
    Args:
        ray: Ray object with origin and direction
        cube: Cube object with position (center) and scale (edge length)
        
    Returns:
        Dictionary with keys:
            'hit_point': numpy array [x, y, z] - intersection point
            'normal': numpy array [x, y, z] - surface normal (normalized)
            'distance': float - distance from ray origin to hit point
        Returns None if no intersection
        
    Example:
        ray = Ray([0, 0, 5], [0, 0, -1])
        cube = Cube([0, 0, 0], 2.0, 1)  # 2x2x2 cube centered at origin
        result = intersect_cube(ray, cube)
        # result = {'hit_point': [0, 0, 1], 'normal': [0, 0, 1], 'distance': 4.0}
    """
    # TODO: Implement cube intersection using slabs method
    # 1. Calculate cube bounds:
    #    half_size = cube.scale / 2
    #    min_bound = cube.position - half_size
    #    max_bound = cube.position + half_size
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
    # 6. Return {'hit_point': hit_point, 'normal': hit_normal, 'distance': t_min}
    
    return None  # Placeholder


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
        Dictionary with keys:
            'surface': The surface object that was hit
            'hit_point': numpy array [x, y, z] - intersection point
            'normal': numpy array [x, y, z] - surface normal (normalized)
            'distance': float - distance from ray origin to hit point
        Returns None if no intersection found
        
    Example Usage (from Person 2's code):
        from intersections import find_nearest_intersection
        from ray import Ray
        
        ray = Ray([0, 0, 5], [0, 0, -1])
        intersection = find_nearest_intersection(ray, surfaces)
        
        if intersection:
            hit_point = intersection['hit_point']
            normal = intersection['normal']
            surface = intersection['surface']
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
    #    - Determine surface type and call appropriate function:
    #      * if isinstance(surface, Sphere): intersection = intersect_sphere(ray, surface)
    #      * elif isinstance(surface, InfinitePlane): intersection = intersect_plane(ray, surface)
    #      * elif isinstance(surface, Cube): intersection = intersect_cube(ray, surface)
    #    - If intersection exists and intersection['distance'] < nearest_distance:
    #      * Update nearest_distance = intersection['distance']
    #      * Update nearest_intersection = intersection
    #      * Add surface to intersection: nearest_intersection['surface'] = surface
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
