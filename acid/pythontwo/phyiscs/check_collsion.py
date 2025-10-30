import math

def is_origin_in_triangle(x1, y1, x2, y2, x3, y3):
    """Check if origin (0,0) is inside triangle using cross products"""
    def sign(px, py, qx, qy):
        return px * qy - py * qx
    
    s1 = sign(x1, y1, x2, y2) 
    s2 = sign(x2, y2, x3, y3)
    s3 = sign(x3, y3, x1, y1)
    
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or \
           (s1 <= 0 and s2 <= 0 and s3 <= 0)

def point_in_triangle(x1, y1, x2, y2, x3, y3, px, py):
    """Check if point (px, py) is inside triangle"""
    def sign(p1x, p1y, p2x, p2y, p3x, p3y):
        return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)
    
    d1 = sign(px, py, x1, y1, x2, y2)
    d2 = sign(px, py, x2, y2, x3, y3)
    d3 = sign(px, py, x3, y3, x1, y1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

# ============ EAR CLIPPING ============

def is_ear(poly, i, indices):
    """Check if vertex i is an ear"""
    n = len(indices)
    prev = indices[(i - 1) % n]
    curr = indices[i]
    next = indices[(i + 1) % n]
    
    ax, ay = poly[prev]
    bx, by = poly[curr]
    cx, cy = poly[next]
    
    # Check if convex
    cross = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    if cross <= 0:
        return False
    
    # Check if any point inside
    for j in range(n):
        if j == (i - 1) % n or j == i or j == (i + 1) % n:
            continue
        px, py = poly[indices[j]]
        if point_in_triangle(ax, ay, bx, by, cx, cy, px, py):
            return False
    
    return True

def ear_clipping(polygon):
    """Triangulate polygon using ear clipping"""
    n = len(polygon)
    if n < 3:
        return []
    
    indices = list(range(n))
    triangles = []
    
    while len(indices) > 3:
        ear_found = False
        
        for i in range(len(indices)):
            if is_ear(polygon, i, indices):
                prev = indices[(i - 1) % len(indices)]
                curr = indices[i]
                next = indices[(i + 1) % len(indices)]
                
                triangles.append((
                    polygon[prev],
                    polygon[curr],
                    polygon[next]
                ))
                
                indices.pop(i)
                ear_found = True
                break
        
        if not ear_found:
            break
    
    if len(indices) == 3:
        triangles.append((
            polygon[indices[0]],
            polygon[indices[1]],
            polygon[indices[2]]
        ))
    
    return triangles

def convex_hull(points):
    """Graham scan convex hull"""
    if len(points) < 3:
        return points
    
    points = sorted(set(points))
    
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]

def minkowski_difference(poly1, poly2):
    """Calculate Minkowski difference A - B"""
    diff_points = []
    
    for x1, y1 in poly1:
        for x2, y2 in poly2:
            diff_points.append((x1 - x2, y1 - y2))
    
    return convex_hull(diff_points)

# ============ MAIN COLLISION CHECK ============

def check_collision(poly1, poly2):
    """Check if two polygons collide using your method"""
    
    # Step 1: Minkowski difference
    diff = minkowski_difference(poly1, poly2)
    
    # Step 2: Triangulate
    triangles = ear_clipping(diff)
    
    # Step 3: Check if origin in any triangle
    for i, tri in enumerate(triangles):
        (x1, y1), (x2, y2), (x3, y3) = tri
        if is_origin_in_triangle(x1, y1, x2, y2, x3, y3):
            return True
    
    return False
