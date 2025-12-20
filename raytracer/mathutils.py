import numpy as np

# Helper functions for vector operations
def cross(a, b):
    return np.cross(a, b)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm