# Implementation Guide - Person 2: Lighting & Shading

## Your Responsibilities
You are implementing all lighting, shading, shadows, reflections, and transparency effects.

## File Structure
- **Main file**: `raytracer/lighting.py` (already created with skeleton)
- **Your TODO items**: Marked with `# TODO:` comments in the code

## Implementation Order (Recommended)

### Phase 1: Basic Phong Lighting (Week 1)
**File**: `lighting.py` → `compute_light_contribution()`

1. **Calculate light direction**
   ```python
   light_direction = normalize(light.position - hit_point)
   ```

2. **Diffuse component** (Lambertian reflection)
   ```python
   diffuse_intensity = max(0, np.dot(normal, light_direction))
   diffuse_color = material.diffuse_color * diffuse_intensity
   ```

3. **Specular component** (Phong model)
   ```python
   reflection_dir = reflect(-light_direction, normal)
   view_dir = normalize(-view_direction)  # Direction to camera
   specular_intensity = max(0, np.dot(view_dir, reflection_dir)) ** material.shininess
   specular_color = material.specular_color * specular_intensity * light.specular_intensity
   ```

4. **Combine with light color**
   ```python
   result = light.color * (diffuse_color + specular_color)
   ```

**Testing**: Create a simple scene with one sphere and one light. You should see basic shading.

---

### Phase 2: Hard Shadows (Week 2 - Part 1)
**File**: `lighting.py` → `compute_shadow_intensity()`

1. **Simple shadow ray** (when `num_shadow_rays == 1`)
   ```python
   shadow_ray_origin = hit_point + normal * 0.001  # Offset to avoid self-intersection
   shadow_ray_direction = normalize(light.position - hit_point)
   
   # Check if any surface blocks the light
   intersection = find_nearest_intersection(shadow_ray_origin, shadow_ray_direction, self.surfaces)
   
   if intersection and intersection['distance'] < distance_to_light:
       # Surface is in shadow
       return (1 - light.shadow_intensity)
   else:
       # Surface is lit
       return 1.0
   ```

2. **Integrate into `compute_light_contribution()`**
   ```python
   light_intensity = self.compute_shadow_intensity(hit_point, light)
   # Multiply final result by light_intensity
   ```

**Testing**: Add a second sphere that casts shadow on the first. You should see hard shadow edges.

---

### Phase 3: Soft Shadows (Week 2 - Part 2)
**File**: `lighting.py` → `compute_shadow_intensity()`

1. **Create perpendicular plane to light direction**
   ```python
   light_dir = normalize(light.position - hit_point)
   
   # Find two perpendicular vectors to light_dir
   if abs(light_dir[0]) > 0.1:
       right = normalize(np.cross(light_dir, np.array([0, 1, 0])))
   else:
       right = normalize(np.cross(light_dir, np.array([1, 0, 0])))
   up = normalize(np.cross(light_dir, right))
   ```

2. **Create N×N grid and sample**
   ```python
   N = self.num_shadow_rays
   cell_size = light.radius / N
   hits = 0
   total_rays = N * N
   
   for i in range(N):
       for j in range(N):
           # Random point in cell [i,j]
           offset_x = (i + np.random.random()) * cell_size - light.radius/2
           offset_y = (j + np.random.random()) * cell_size - light.radius/2
           
           sample_point = light.position + right * offset_x + up * offset_y
           shadow_ray_dir = normalize(sample_point - hit_point)
           
           # Check intersection
           intersection = find_nearest_intersection(hit_point + normal * 0.001, shadow_ray_dir, self.surfaces)
           
           if intersection is None or intersection['distance'] > np.linalg.norm(sample_point - hit_point):
               hits += 1
   
   hit_ratio = hits / total_rays
   return (1 - light.shadow_intensity) + light.shadow_intensity * hit_ratio
   ```

**Testing**: Shadows should now have soft, gradual edges.

---

### Phase 4: Reflections (Week 3 - Part 1)
**File**: `lighting.py` → `compute_reflection()`

1. **Calculate reflection direction**
   ```python
   reflection_dir = self.reflect(incident_direction, normal)
   ```

2. **Shoot reflection ray**
   ```python
   reflection_origin = hit_point + normal * 0.001  # Offset to avoid self-intersection
   intersection = find_nearest_intersection(reflection_origin, reflection_dir, self.surfaces)
   ```

3. **Recursively compute color**
   ```python
   if intersection:
       reflected_color = self.compute_color(
           reflection_origin, 
           reflection_dir, 
           intersection, 
           recursion_depth + 1
       )
   else:
       reflected_color = self.background_color
   
   # Multiply by reflection color (tint)
   return reflected_color * material.reflection_color
   ```

**Testing**: Create a reflective sphere. It should reflect other objects.

---

### Phase 5: Transparency (Week 3 - Part 2)
**File**: `lighting.py` → `compute_transparency()`

1. **Continue ray through surface**
   ```python
   # Small offset to avoid self-intersection
   transparency_origin = hit_point - normal * 0.001
   
   # Find what's behind the transparent surface
   intersection = find_nearest_intersection(transparency_origin, ray_direction, self.surfaces)
   ```

2. **Recursively compute background color**
   ```python
   if intersection:
       background = self.compute_color(
           transparency_origin,
           ray_direction,
           intersection,
           recursion_depth + 1
       )
   else:
       background = self.background_color
   
   return background
   ```

**Testing**: Create a transparent sphere. You should see objects behind it.

---

## Integration with Person 1's Code

### What You Need from Person 1:

1. **`find_nearest_intersection(ray_origin, ray_direction, surfaces)`**
   - Returns: `{'surface': obj, 'hit_point': np.array, 'normal': np.array, 'distance': float}`
   - Or `None` if no intersection

2. **Surface normal calculation** (might be built into intersection function)

### What Person 1 Needs from You:

1. **`LightingEngine` class** - initialized with scene data
2. **`compute_color()` method** - called for each pixel

### Integration Point in `ray_tracer.py`:

```python
# After Person 1 generates rays and finds intersections:
lighting_engine = LightingEngine(scene_settings, materials, lights, surfaces)

for pixel in image:
    ray_origin, ray_direction = camera.generate_ray(pixel)
    intersection = find_nearest_intersection(ray_origin, ray_direction, surfaces)
    color = lighting_engine.compute_color(ray_origin, ray_direction, intersection)
    image[pixel] = color
```

---

## Important Formulas

### Phong Shading
```
diffuse = Kd * max(0, N · L)
specular = Ks * max(0, R · V)^shininess
where:
  Kd = diffuse color
  Ks = specular color
  N = surface normal
  L = light direction
  R = reflection of L around N
  V = view direction (to camera)
```

### Reflection
```
R = I - 2(I · N)N
where:
  I = incident direction
  N = surface normal
```

### Color Combination (from assignment)
```
output = (background * transparency) + 
         (diffuse + specular) * (1 - transparency) + 
         reflection
```

### Shadow Intensity
```
light_intensity = (1 - shadow_intensity) + 
                  shadow_intensity * (rays_hit / total_rays)
```

---

## Testing Strategy

1. **Test incrementally** - implement one feature at a time
2. **Simple scenes first** - one sphere, one light
3. **Visual debugging** - if something looks wrong, add print statements for:
   - Light directions
   - Normal vectors
   - Color values before clamping
4. **Compare with reference images** - use provided test scenes

---

## Common Pitfalls

1. **Self-intersection**: Always offset ray origins slightly along the normal
   ```python
   new_origin = hit_point + normal * 0.001
   ```

2. **Vector normalization**: Always normalize direction vectors
   ```python
   direction = normalize(target - origin)
   ```

3. **Color clamping**: RGB values must be in [0, 255]
   ```python
   color = np.clip(color, 0, 255)
   ```

4. **Material indexing**: Materials are 1-indexed in scene file
   ```python
   material = materials[surface.material_index - 1]
   ```

5. **Recursion limit**: Check before recursive calls
   ```python
   if recursion_depth < self.max_recursion:
       # Make recursive call
   ```

---

## BONUS: Transparency in Shadows (+5 points)

In `compute_shadow_intensity()`, when checking if a surface blocks light:

```python
# Instead of just checking if intersection exists:
if intersection:
    blocking_material = self.materials[intersection['surface'].material_index - 1]
    
    # If blocking object is transparent, some light passes through
    if blocking_material.transparency > 0:
        # Reduce shadow based on transparency
        # More transparent = less shadow
        shadow_factor = 1 - blocking_material.transparency
        # Accumulate this in your shadow calculation
```

---

## Performance Tips (for bonus points)

1. **Vectorize operations** - use numpy array operations instead of loops where possible
2. **Early termination** - if recursion depth is max, don't compute reflections
3. **Shadow ray optimization** - if shadow_intensity is 0, skip shadow calculation
4. **Cache calculations** - store normalized vectors instead of recalculating

---

## Questions to Ask Your Teammate

1. What format does `find_nearest_intersection()` return?
2. Are normals already normalized?
3. How are you handling the small offset for avoiding self-intersection?
4. What coordinate system are you using (right-handed vs left-handed)?

---

## Debugging Checklist

- [ ] Diffuse lighting works (surfaces facing light are brighter)
- [ ] Specular highlights appear on shiny surfaces
- [ ] Hard shadows work (sharp edges)
- [ ] Soft shadows work (gradual edges)
- [ ] Reflections work (mirrors reflect other objects)
- [ ] Transparency works (can see through objects)
- [ ] Recursive reflections work (mirror reflecting mirror)
- [ ] Colors are in valid range [0, 255]
- [ ] No self-intersection artifacts
- [ ] Background color shows when no intersection

Good luck! 🚀
