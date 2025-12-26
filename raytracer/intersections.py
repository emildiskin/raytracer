import numpy as np
from ray import Ray
from intersection import Intersection
from surfaces.sphere import Sphere
from surfaces.infinite_plane import InfinitePlane
from surfaces.cube import Cube


def intersect_sphere(ray, sphere):
    return sphere.intersect(ray)


def intersect_plane(ray, plane):
    return plane.intersect(ray)


def intersect_cube(ray, cube):
    return cube.intersect(ray)

def find_all_intersections(ray, surfaces, ignore_surface=None):
    """
    Find all surface intersections along a ray
    
    Args:
        ray: Ray object with origin and direction
        surfaces: List of all surface objects in the scene (Sphere, Plane, Cube)
        ignore_surface: Optional surface object to ignore (used for reflections
                       to avoid self-intersection)
        
    Returns:
        List of Intersection objects, each with:
            surface: The surface object that was hit
            hit_point: numpy array [x, y, z] - intersection point
            normal: numpy array [x, y, z] - surface normal (normalized)
            distance: float - distance from ray origin to hit point
        Returns empty list if no intersections found
    """
    intersections = []
    
    for surface in surfaces:
        # Skip if this is the surface to ignore (avoid self-intersection)
        if surface is ignore_surface:
            continue
        
        # Call the surface's intersect method
        intersection = surface.intersect(ray)
        
        # If intersection found, add surface reference and append to list
        if intersection is not None:
            intersection.surface = surface
            intersections.append(intersection)
    
    return intersections


def find_nearest_intersection(ray, surfaces, ignore_surface=None):
    """
    Find the nearest surface intersection along a ray
        
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
    """
    nearest_intersection = None
    nearest_distance = np.inf
    
    for surface in surfaces:
        # Skip if this is the surface to ignore (avoid self-intersection)
        if surface is ignore_surface:
            continue
        
        # Call the surface's intersect method
        intersection = surface.intersect(ray)
        
        # Check if this is the closest intersection so far
        if intersection is not None and intersection.distance < nearest_distance:
            nearest_distance = intersection.distance
            nearest_intersection = intersection
            # Add reference to the surface that was hit
            nearest_intersection.surface = surface
    
    return nearest_intersection