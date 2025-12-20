"""
Simple test file for Person 2 to test lighting implementation independently
This creates a minimal scene to test each lighting feature incrementally
"""

import numpy as np
from PIL import Image

# Mock classes for testing without Person 1's code
class MockIntersection:
    """Mock intersection data for testing"""
    def __init__(self, hit_point, normal, distance):
        self.surface = MockSurface()
        self.hit_point = np.array(hit_point)
        self.normal = np.array(normal) / np.linalg.norm(normal)  # Normalize
        self.distance = distance

class MockSurface:
    """Mock surface for testing"""
    def __init__(self):
        self.material_index = 1

class MockMaterial:
    """Mock material for testing"""
    def __init__(self):
        self.diffuse_color = np.array([200, 50, 50])  # Red
        self.specular_color = np.array([255, 255, 255])  # White
        self.reflection_color = np.array([0, 0, 0])  # No reflection
        self.shininess = 50
        self.transparency = 0.0

class MockLight:
    """Mock light for testing"""
    def __init__(self):
        self.position = np.array([5, 5, 5])
        self.color = np.array([1, 1, 1])  # White light
        self.specular_intensity = 1.0
        self.shadow_intensity = 1.0
        self.radius = 0.5

class MockSceneSettings:
    """Mock scene settings for testing"""
    def __init__(self):
        self.background_color = [50, 50, 100]  # Dark blue
        self.root_number_shadow_rays = 1  # Start with hard shadows
        self.max_recursions = 3


def test_basic_lighting():
    """
    Test 1: Basic Phong lighting without shadows
    Expected: Red sphere with white specular highlight
    """
    print("Test 1: Basic Phong Lighting")
    print("-" * 50)
    
    # Import your lighting module
    try:
        from lighting import LightingEngine
    except ImportError:
        print("ERROR: Cannot import lighting.py")
        print("Make sure lighting.py is in the same directory")
        return
    
    # Setup mock scene
    scene_settings = MockSceneSettings()
    materials = [MockMaterial()]
    lights = [MockLight()]
    surfaces = []  # Empty for now
    
    # Create lighting engine
    engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    # Test point on sphere surface
    hit_point = np.array([0, 0, 0])
    normal = np.array([0, 1, 0])  # Pointing up
    ray_direction = np.array([0, 0, -1])  # Camera looking along -Z
    
    intersection_data = {
        'surface': MockSurface(),
        'hit_point': hit_point,
        'normal': normal,
        'distance': 5.0
    }
    
    # Compute color
    color = engine.compute_color(
        ray_origin=np.array([0, 0, 5]),
        ray_direction=ray_direction,
        intersection_data=intersection_data,
        recursion_depth=0
    )
    
    print(f"Computed color: {color}")
    print(f"Expected: Red-ish color with some brightness")
    print(f"R: {color[0]:.1f}, G: {color[1]:.1f}, B: {color[2]:.1f}")
    
    # Check if color is reasonable
    if color[0] > color[1] and color[0] > color[2]:
        print("✓ Color is red-dominant (correct)")
    else:
        print("✗ Color should be red-dominant")
    
    if np.any(color > 0):
        print("✓ Surface is lit (not black)")
    else:
        print("✗ Surface should be lit, not black")
    
    print()


def test_no_intersection():
    """
    Test 2: Ray that doesn't hit anything
    Expected: Background color
    """
    print("Test 2: Background Color (No Intersection)")
    print("-" * 50)
    
    try:
        from lighting import LightingEngine
    except ImportError:
        print("ERROR: Cannot import lighting.py")
        return
    
    scene_settings = MockSceneSettings()
    materials = [MockMaterial()]
    lights = [MockLight()]
    surfaces = []
    
    engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    # No intersection
    color = engine.compute_color(
        ray_origin=np.array([0, 0, 0]),
        ray_direction=np.array([0, 0, -1]),
        intersection_data=None,
        recursion_depth=0
    )
    
    print(f"Computed color: {color}")
    print(f"Expected: {scene_settings.background_color}")
    
    if np.allclose(color, scene_settings.background_color):
        print("✓ Background color is correct")
    else:
        print("✗ Background color doesn't match")
    
    print()


def test_multiple_lights():
    """
    Test 3: Multiple lights illuminating the same point
    Expected: Brighter color (additive lighting)
    """
    print("Test 3: Multiple Lights")
    print("-" * 50)
    
    try:
        from lighting import LightingEngine
    except ImportError:
        print("ERROR: Cannot import lighting.py")
        return
    
    scene_settings = MockSceneSettings()
    materials = [MockMaterial()]
    
    # Two lights from different positions
    light1 = MockLight()
    light1.position = np.array([5, 5, 5])
    light2 = MockLight()
    light2.position = np.array([-5, 5, 5])
    
    lights = [light1, light2]
    surfaces = []
    
    engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    hit_point = np.array([0, 0, 0])
    normal = np.array([0, 1, 0])
    ray_direction = np.array([0, 0, -1])
    
    intersection_data = {
        'surface': MockSurface(),
        'hit_point': hit_point,
        'normal': normal,
        'distance': 5.0
    }
    
    color = engine.compute_color(
        ray_origin=np.array([0, 0, 5]),
        ray_direction=ray_direction,
        intersection_data=intersection_data,
        recursion_depth=0
    )
    
    print(f"Computed color with 2 lights: {color}")
    print("Expected: Brighter than single light test")
    
    # Should be brighter than with single light
    if np.any(color > 100):
        print("✓ Surface is well-lit with multiple lights")
    else:
        print("✗ Surface should be brighter with multiple lights")
    
    print()


def create_test_image():
    """
    Create a simple test image to visualize lighting
    This tests a grid of points with different normals
    """
    print("Test 4: Creating Test Image")
    print("-" * 50)
    
    try:
        from lighting import LightingEngine
    except ImportError:
        print("ERROR: Cannot import lighting.py")
        return
    
    scene_settings = MockSceneSettings()
    materials = [MockMaterial()]
    lights = [MockLight()]
    surfaces = []
    
    engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    # Create 100x100 test image
    width, height = 100, 100
    image = np.zeros((height, width, 3))
    
    print("Rendering test image...")
    
    for y in range(height):
        for x in range(width):
            # Create a normal that varies across the image
            # This simulates a curved surface
            nx = (x - width/2) / (width/2)
            ny = (y - height/2) / (height/2)
            nz = np.sqrt(max(0, 1 - nx*nx - ny*ny))
            
            if nz > 0:  # Only render if normal is valid
                normal = np.array([nx, ny, nz])
                normal = normal / np.linalg.norm(normal)
                
                hit_point = np.array([nx, ny, 0])
                ray_direction = np.array([0, 0, -1])
                
                intersection_data = {
                    'surface': MockSurface(),
                    'hit_point': hit_point,
                    'normal': normal,
                    'distance': 5.0
                }
                
                color = engine.compute_color(
                    ray_origin=np.array([0, 0, 5]),
                    ray_direction=ray_direction,
                    intersection_data=intersection_data,
                    recursion_depth=0
                )
                
                image[y, x] = color
            else:
                # Background
                image[y, x] = scene_settings.background_color
    
    # Save image
    img = Image.fromarray(np.uint8(image))
    img.save('test_lighting_output.png')
    print("✓ Test image saved as 'test_lighting_output.png'")
    print("  Expected: Red sphere with shading and specular highlight")
    print()


def main():
    """Run all tests"""
    print("=" * 50)
    print("LIGHTING MODULE TESTS - PERSON 2")
    print("=" * 50)
    print()
    
    test_basic_lighting()
    test_no_intersection()
    test_multiple_lights()
    create_test_image()
    
    print("=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Implement compute_light_contribution() in lighting.py")
    print("2. Run this test again to see if basic lighting works")
    print("3. Check test_lighting_output.png for visual verification")
    print("4. Move on to shadows, reflections, and transparency")


if __name__ == '__main__':
    main()
