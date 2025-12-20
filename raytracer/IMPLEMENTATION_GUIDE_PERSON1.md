# Implementation Guide - Person 1: Core Ray Tracing & Geometry

## Your Responsibilities
You are implementing ray generation, camera setup, and all ray-surface intersection calculations.

## File Structure
- **Main files**: 
  - `raytracer/camera.py` - Camera ray generation
  - `raytracer/ray.py` - Ray class (you'll create this)
  - `raytracer/intersections.py` - Intersection logic (you'll create this)
  - `raytracer/ray_tracer.py` - Main integration point

## Implementation Order (Recommended)

### Phase 1: Camera & Ray Generation (Week 1)
**Files**: `camera.py`, `ray.py`

#### Step 1: Create Ray Class
Create `raytracer/ray.py`:

```python
import numpy as np

class Ray:
    """Represents a ray with origin and direction"""
    
    def __init__(self, origin, direction):
        """
        Args:
            origin: numpy array [x, y, z] - starting point
            direction: numpy array [x, y, z] - direction (will be normalized)
        """
        self.origin = np.array(origin, dtype=float)
        self.direction = self.normalize(np.array(direction, dtype=float))
    
    def point_at(self, t):
        """
        Get point along ray at parameter t
        Formula: P(t) = origin + t * direction
        """
        return self.origin + t * self.direction
    
    @staticmethod
    def normalize(vector):
        """Normalize a vector to unit length"""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
```

#### Step 2: Implement Camera Ray Generation
Update `raytracer/camera.py`:

```python
import numpy as np
from ray import Ray

class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = np.array(position, dtype=float)
        self.look_at = np.array(look_at, dtype=float)
        self.up_vector = np.array(up_vector, dtype=float)
        self.screen_distance = screen_distance
        self.screen_width = screen_width
        
        # Compute camera coordinate system
        self._setup_camera_basis()
    
    def _setup_camera_basis(self):
        """
        Compute camera's coordinate system (right, up, forward vectors)
        This creates an orthonormal basis for the camera
        """
        # Forward direction (from camera to look_at point)
        self.forward = self.normalize(self.look_at - self.position)
        
        # Right direction (perpendicular to forward and up)
        self.right = self.normalize(np.cross(self.forward, self.up_vector))
        
        # True up direction (perpendicular to forward and right)
        # This corrects the up_vector to be truly perpendicular
        self.up = self.normalize(np.cross(self.right, self.forward))
    
    def generate_ray(self, pixel_x, pixel_y, image_width, image_height):
        """
        Generate a ray from camera through a specific pixel
        
        Args:
            pixel_x: X coordinate of pixel (0 to image_width-1)
            pixel_y: Y coordinate of pixel (0 to image_height-1)
            image_width: Total width of image in pixels
            image_height: Total height of image in pixels
            
        Returns:
            Ray object going through the pixel
        """
        # Calculate aspect ratio
        aspect_ratio = image_width / image_height
        screen_height = self.screen_width / aspect_ratio
        
        # Convert pixel coordinates to screen coordinates [-0.5, 0.5]
        # Center of pixel (0,0) should be at top-left
        screen_x = (pixel_x + 0.5) / image_width - 0.5
        screen_y = 0.5 - (pixel_y + 0.5) / image_height  # Flip Y (image Y goes down)
        
        # Scale to actual screen dimensions
        screen_x *= self.screen_width
        screen_y *= screen_height
        
        # Calculate point on screen in world coordinates
        screen_center = self.position + self.forward * self.screen_distance
        screen_point = (screen_center + 
                       self.right * screen_x + 
                       self.up * screen_y)
        
        # Ray direction from camera to screen point
        ray_direction = screen_point - self.position
        
        return Ray(self.position, ray_direction)
    
    @staticmethod
    def normalize(vector):
        """Normalize a vector to unit length"""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
```

**Testing**: Generate a few rays and print their directions. They should point in slightly different directions.

---

### Phase 2: Sphere Intersection (Week 1)
**File**: `raytracer/intersections.py`

Create `raytracer/intersections.py`:

```python
import numpy as np
from surfaces.sphere import Sphere
from surfaces.infinite_plane import InfinitePlane
from surfaces.cube import Cube

def intersect_sphere(ray, sphere):
    """
    Find intersection of ray with sphere
    
    Mathematical approach:
    Sphere equation: |P - C|² = r²
    Ray equation: P(t) = O + tD
    Substitute and solve quadratic: at² + bt + c = 0
    
    Args:
        ray: Ray object
        sphere: Sphere object
        
    Returns:
        dict with keys: 'hit_point', 'normal', 'distance'
        or None if no intersection
    """
    # Vector from ray origin to sphere center
    oc = ray.origin - np.array(sphere.position)
    
    # Quadratic equation coefficients
    # a = D·D (always 1 since direction is normalized)
    a = np.dot(ray.direction, ray.direction)
    b = 2.0 * np.dot(oc, ray.direction)
    c = np.dot(oc, oc) - sphere.radius ** 2
    
    # Discriminant
    discriminant = b * b - 4 * a * c
    
    # No intersection if discriminant is negative
    if discriminant < 0:
        return None
    
    # Find nearest intersection (smallest positive t)
    sqrt_discriminant = np.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2.0 * a)
    t2 = (-b + sqrt_discriminant) / (2.0 * a)
    
    # Choose nearest positive t
    t = None
    if t1 > 0.0001:  # Small epsilon to avoid self-intersection
        t = t1
    elif t2 > 0.0001:
        t = t2
    else:
        return None  # Both intersections behind camera
    
    # Calculate hit point and normal
    hit_point = ray.point_at(t)
    normal = (hit_point - np.array(sphere.position)) / sphere.radius
    
    return {
        'hit_point': hit_point,
        'normal': normal,
        'distance': t
    }


def intersect_plane(ray, plane):
    """
    Find intersection of ray with infinite plane
    
    Plane equation: P·N = c
    Ray equation: P(t) = O + tD
    Solve: (O + tD)·N = c
           t = (c - O·N) / (D·N)
    
    Args:
        ray: Ray object
        plane: InfinitePlane object
        
    Returns:
        dict with keys: 'hit_point', 'normal', 'distance'
        or None if no intersection
    """
    normal = np.array(plane.normal)
    normal = normal / np.linalg.norm(normal)  # Ensure normalized
    
    # Check if ray is parallel to plane
    denom = np.dot(ray.direction, normal)
    if abs(denom) < 1e-6:
        return None  # Ray parallel to plane
    
    # Calculate t
    t = (plane.offset - np.dot(ray.origin, normal)) / denom
    
    # Check if intersection is in front of ray
    if t < 0.0001:
        return None
    
    hit_point = ray.point_at(t)
    
    return {
        'hit_point': hit_point,
        'normal': normal,
        'distance': t
    }


def intersect_cube(ray, cube):
    """
    Find intersection of ray with axis-aligned cube using slabs method
    
    The slabs method:
    1. Treat cube as intersection of 3 pairs of parallel planes (slabs)
    2. For each axis, find entry and exit t values
    3. Cube is hit if all slabs overlap
    
    Args:
        ray: Ray object
        cube: Cube object
        
    Returns:
        dict with keys: 'hit_point', 'normal', 'distance'
        or None if no intersection
    """
    center = np.array(cube.position)
    half_size = cube.scale / 2.0
    
    # Cube bounds
    min_bound = center - half_size
    max_bound = center + half_size
    
    # Initialize t ranges
    t_min = -np.inf
    t_max = np.inf
    hit_normal = np.array([0, 0, 0], dtype=float)
    
    # Check each axis (X, Y, Z)
    for i in range(3):
        if abs(ray.direction[i]) < 1e-6:
            # Ray parallel to slab
            if ray.origin[i] < min_bound[i] or ray.origin[i] > max_bound[i]:
                return None  # Ray outside slab, no intersection
        else:
            # Calculate intersection t values for this slab
            t1 = (min_bound[i] - ray.origin[i]) / ray.direction[i]
            t2 = (max_bound[i] - ray.origin[i]) / ray.direction[i]
            
            # Ensure t1 <= t2
            if t1 > t2:
                t1, t2 = t2, t1
            
            # Update t_min (entry point)
            if t1 > t_min:
                t_min = t1
                # Normal points in direction of slab we entered
                hit_normal = np.array([0, 0, 0], dtype=float)
                hit_normal[i] = -np.sign(ray.direction[i])
            
            # Update t_max (exit point)
            if t2 < t_max:
                t_max = t2
            
            # Check if slabs don't overlap
            if t_min > t_max:
                return None
    
    # Check if intersection is in front of ray
    if t_min < 0.0001:
        if t_max < 0.0001:
            return None
        # Ray starts inside cube, use exit point
        t_min = t_max
        hit_normal = -hit_normal
    
    hit_point = ray.point_at(t_min)
    
    return {
        'hit_point': hit_point,
        'normal': hit_normal,
        'distance': t_min
    }


def find_nearest_intersection(ray, surfaces, ignore_surface=None):
    """
    Find the nearest surface intersection along a ray
    
    This is the main function that Person 2 will call!
    
    Args:
        ray: Ray object
        surfaces: List of all surfaces (spheres, planes, cubes)
        ignore_surface: Optional surface to ignore (for reflections)
        
    Returns:
        dict with keys: 'surface', 'hit_point', 'normal', 'distance'
        or None if no intersection
    """
    nearest_intersection = None
    nearest_distance = np.inf
    
    for surface in surfaces:
        # Skip ignored surface
        if surface is ignore_surface:
            continue
        
        # Check intersection based on surface type
        intersection = None
        
        if isinstance(surface, Sphere):
            intersection = intersect_sphere(ray, surface)
        elif isinstance(surface, InfinitePlane):
            intersection = intersect_plane(ray, surface)
        elif isinstance(surface, Cube):
            intersection = intersect_cube(ray, surface)
        
        # Update nearest intersection
        if intersection and intersection['distance'] < nearest_distance:
            nearest_distance = intersection['distance']
            nearest_intersection = intersection
            nearest_intersection['surface'] = surface
    
    return nearest_intersection
```

**Testing**: Create a simple scene with one sphere and shoot rays at it. Print hit points.

---

### Phase 3: Plane & Cube Intersections (Week 2)
Already included in the code above! Test each one:

**Plane Testing**:
```python
# Create horizontal plane at y=0
plane = InfinitePlane([0, 1, 0], 0, 1)
ray = Ray([0, 5, 0], [0, -1, 0])  # Ray pointing down
intersection = intersect_plane(ray, plane)
# Should hit at (0, 0, 0)
```

**Cube Testing**:
```python
# Create cube at origin
cube = Cube([0, 0, 0], 2, 1)  # 2x2x2 cube
ray = Ray([0, 0, 5], [0, 0, -1])  # Ray pointing at cube
intersection = intersect_cube(ray, cube)
# Should hit front face
```

---

### Phase 4: Integration with Person 2 (Week 3)
**File**: `raytracer/ray_tracer.py`

Update the main ray tracer file:

```python
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


def parse_scene_file(file_path):
    """Parse scene file - already implemented"""
    objects = []
    camera = None
    scene_settings = None
    materials = []
    lights = []
    surfaces = []
    
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
                materials.append(material)
            elif obj_type == "sph":
                sphere = Sphere(params[:3], params[3], int(params[4]))
                surfaces.append(sphere)
            elif obj_type == "pln":
                plane = InfinitePlane(params[:3], params[3], int(params[4]))
                surfaces.append(plane)
            elif obj_type == "box":
                cube = Cube(params[:3], params[3], int(params[4]))
                surfaces.append(cube)
            elif obj_type == "lgt":
                light = Light(params[:3], params[3:6], params[6], params[7], params[8])
                lights.append(light)
    
    return camera, scene_settings, materials, lights, surfaces


def render_scene(camera, scene_settings, materials, lights, surfaces, width, height):
    """
    Main rendering function - THIS IS THE INTEGRATION POINT!
    
    Args:
        camera: Camera object
        scene_settings: SceneSettings object
        materials: List of Material objects
        lights: List of Light objects
        surfaces: List of surface objects
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        numpy array of shape (height, width, 3) with RGB values
    """
    # Initialize image array
    image = np.zeros((height, width, 3))
    
    # Create lighting engine (Person 2's code)
    lighting_engine = LightingEngine(scene_settings, materials, lights, surfaces)
    
    print(f"Rendering {width}x{height} image...")
    
    # Render each pixel
    for y in range(height):
        if y % 50 == 0:
            print(f"  Rendering row {y}/{height}...")
        
        for x in range(width):
            # PERSON 1: Generate ray through pixel
            ray = camera.generate_ray(x, y, width, height)
            
            # PERSON 1: Find nearest intersection
            intersection = find_nearest_intersection(ray, surfaces)
            
            # PERSON 2: Compute color at intersection
            color = lighting_engine.compute_color(
                ray_origin=ray.origin,
                ray_direction=ray.direction,
                intersection_data=intersection,
                recursion_depth=0
            )
            
            # Store color in image
            image[y, x] = color
    
    print("Rendering complete!")
    return image


def save_image(image_array, output_path):
    """Save rendered image to file"""
    image = Image.fromarray(np.uint8(image_array))
    image.save(output_path)
    print(f"Image saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Python Ray Tracer')
    parser.add_argument('scene_file', type=str, help='Path to the scene file')
    parser.add_argument('output_image', type=str, help='Name of the output image file')
    parser.add_argument('--width', type=int, default=500, help='Image width')
    parser.add_argument('--height', type=int, default=500, help='Image height')
    args = parser.parse_args()

    # Parse the scene file
    camera, scene_settings, materials, lights, surfaces = parse_scene_file(args.scene_file)
    
    # Render the scene
    image_array = render_scene(camera, scene_settings, materials, lights, surfaces, 
                               args.width, args.height)
    
    # Save the output image
    save_image(image_array, args.output_image)


if __name__ == '__main__':
    main()
```

---

## Integration Points with Person 2

### What Person 2 Needs from You:

1. **`find_nearest_intersection(ray, surfaces, ignore_surface=None)`**
   - Input: Ray object, list of surfaces, optional surface to ignore
   - Output: Dictionary with keys:
     - `'surface'`: The surface object that was hit
     - `'hit_point'`: numpy array [x, y, z] of intersection point
     - `'normal'`: numpy array [x, y, z] of surface normal (normalized)
     - `'distance'`: float distance from ray origin to hit point
   - Returns `None` if no intersection

2. **Ray class** with:
   - `ray.origin`: numpy array [x, y, z]
   - `ray.direction`: numpy array [x, y, z] (normalized)
   - `ray.point_at(t)`: method to get point along ray

### What You Need from Person 2:

1. **`LightingEngine` class**
2. **`compute_color(ray_origin, ray_direction, intersection_data, recursion_depth)`** method

---

## Important Formulas

### Ray-Sphere Intersection
```
Sphere: |P - C|² = r²
Ray: P(t) = O + tD
Substitute: |O + tD - C|² = r²
Expand to quadratic: at² + bt + c = 0
where:
  a = D·D
  b = 2(O-C)·D
  c = (O-C)·(O-C) - r²
```

### Ray-Plane Intersection
```
Plane: P·N = c
Ray: P(t) = O + tD
Solve: (O + tD)·N = c
       t = (c - O·N) / (D·N)
```

### Camera Ray Generation
```
1. Compute camera basis: forward, right, up
2. Convert pixel to screen coordinates [-0.5, 0.5]
3. Scale by screen dimensions
4. Point on screen = camera_pos + forward*distance + right*x + up*y
5. Ray direction = screen_point - camera_pos
```

---

## Testing Strategy

1. **Test camera ray generation**
   - Generate rays for corners and center
   - Verify they point in correct directions

2. **Test sphere intersection**
   - Ray hitting sphere center
   - Ray missing sphere
   - Ray starting inside sphere

3. **Test plane intersection**
   - Ray perpendicular to plane
   - Ray parallel to plane
   - Ray at angle

4. **Test cube intersection**
   - Ray hitting each face
   - Ray missing cube
   - Ray starting inside cube

5. **Test find_nearest_intersection**
   - Multiple surfaces
   - Verify nearest is returned
   - Test with ignore_surface parameter

---

## Common Pitfalls

1. **Self-intersection**: Use small epsilon (0.0001) when checking t > 0
2. **Vector normalization**: Always normalize direction vectors
3. **Coordinate system**: Ensure camera basis is orthonormal
4. **Cube normals**: Normal depends on which face was hit
5. **Plane normal**: Ensure plane normal is normalized

---

## Debugging Checklist

- [ ] Camera generates rays in correct directions
- [ ] Rays hit spheres at correct points
- [ ] Sphere normals point outward
- [ ] Rays hit planes correctly
- [ ] Plane normals are correct
- [ ] Rays hit cubes on correct faces
- [ ] Cube normals match hit face
- [ ] find_nearest_intersection returns nearest surface
- [ ] No self-intersection artifacts
- [ ] Integration with Person 2 works

---

## Performance Tips (for bonus)

1. **Early ray termination**: Stop if t > max_distance
2. **Bounding volumes**: Check simple bounds before complex intersection
3. **Vectorization**: Use numpy operations instead of loops where possible
4. **Avoid redundant calculations**: Cache normalized vectors

Good luck! 🚀
