import argparse
from PIL import Image
import numpy as np

from camera import Camera
from light import Light
from material import Material
from scene_settings import SceneSettings
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from lighting import LightingEngine
from intersections import find_nearest_intersection
from ray import Ray


def parse_scene_file(file_path):
    objects = []
    camera = None
    scene_settings = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            obj_type = parts[0]
            params = [float(p) for p in parts[1:]]
            if obj_type == "cam":
                camera = Camera(params[:3], params[3:6], params[6:9], params[9], params[10])
            elif obj_type == "set":
                scene_settings = SceneSettings(params[:3], params[3], params[4])
            elif obj_type == "mtl":
                material = Material(params[:3], params[3:6], params[6:9], params[9], params[10])
                objects.append(material)
            elif obj_type == "sph":
                sphere = Sphere(params[:3], params[3], int(params[4]))
                objects.append(sphere)
            elif obj_type == "pln":
                plane = InfinitePlane(params[:3], params[3], int(params[4]))
                objects.append(plane)
            elif obj_type == "box":
                cube = Cube(params[:3], params[3], int(params[4]))
                objects.append(cube)
            elif obj_type == "lgt":
                light = Light(params[:3], params[3:6], params[6], params[7], params[8])
                objects.append(light)
            else:
                raise ValueError("Unknown object type: {}".format(obj_type))
    return camera, scene_settings, objects


def save_image(image_array, output_path):
    """Save the rendered image to a file"""
    image = Image.fromarray(np.uint8(image_array))
    image.save(output_path)


def main():
    parser = argparse.ArgumentParser(description='Python Ray Tracer')
    parser.add_argument('scene_file', type=str, help='Path to the scene file')
    parser.add_argument('output_image', type=str, help='Name of the output image file')
    parser.add_argument('--width', type=int, default=500, help='Image width')
    parser.add_argument('--height', type=int, default=500, help='Image height')
    args = parser.parse_args()

    # Parse the scene file
    camera, scene_settings, objects = parse_scene_file(args.scene_file)

    # Separate objects into materials, lights, and surfaces
    materials = []
    lights = []
    surfaces = []
    
    for obj in objects:
        if isinstance(obj, Material):
            materials.append(obj)
        elif isinstance(obj, Light):
            lights.append(obj)
        elif isinstance(obj, (Sphere, InfinitePlane, Cube)):
            surfaces.append(obj)
    
    # Initialize the lighting engine
    lighting_engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    # Create image array
    image_width = args.width
    image_height = args.height
    image_array = np.zeros((image_height, image_width, 3))
    
    print(f"Rendering {image_width}x{image_height} image...")
    print(f"Scene: {len(surfaces)} surfaces, {len(lights)} lights, {len(materials)} materials")
    print(f"Settings: {int(scene_settings.root_number_shadow_rays)}x{int(scene_settings.root_number_shadow_rays)} shadow rays, max recursion: {int(scene_settings.max_recursions)}")
    
    # Ray trace each pixel
    for y in range(image_height):
        if y % 50 == 0:
            print(f"Progress: {y}/{image_height} rows ({100*y//image_height}%)")
        
        for x in range(image_width):
            # Generate ray through this pixel
            ray = camera.generate_ray(x, y, image_width, image_height)
            
            # Find nearest intersection
            intersection = find_nearest_intersection(ray, surfaces)
            
            # Compute color using lighting engine
            color = lighting_engine.compute_color(
                ray.origin,
                ray.direction,
                intersection,
                recursion_depth=0
            )
            
            # Store color in image array
            image_array[y, x] = color
    
    print("Rendering complete!")
    
    # Save the output image
    save_image(image_array, args.output_image)
    print(f"Image saved to: {args.output_image}")


if __name__ == '__main__':
    main()
