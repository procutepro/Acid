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

def closest_point_to_origin(triangle):
    """Return the point on the triangle closest to origin (0,0)"""
    def distance_sq(p):
        return p[0]**2 + p[1]**2

    # Include vertices
    candidates = list(triangle)

    # Also include projections onto edges
    for i in range(3):
        a = triangle[i]
        b = triangle[(i+1)%3]
        ab = [b[0]-a[0], b[1]-a[1]]
        t = max(0, min(1, -(a[0]*ab[0] + a[1]*ab[1]) / (ab[0]**2 + ab[1]**2)))
        proj = [a[0]+ab[0]*t, a[1]+ab[1]*t]
        candidates.append(proj)
    
    # Return the closest
    return min(candidates, key=lambda p: distance_sq(p))

def compute_mtv(poly1, poly2):
    """Return minimum translation vector to resolve collision"""
    diff = minkowski_difference(poly1, poly2)
    triangles = ear_clipping(diff)

    mtv = None
    min_dist_sq = float('inf')

    for tri in triangles:
        if is_origin_in_triangle(*tri[0], *tri[1], *tri[2]):
            # find closest point on this triangle to origin
            point = closest_point_to_origin(tri)
            dist_sq = point[0]**2 + point[1]**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                mtv = point
    
    if mtv:
        # MTV = vector from origin to closest point
        return [-mtv[0], -mtv[1]]
    return [0,0]  # no collision

# --- Usage example ---
def resolve_collision(rb1, rb2):
    mtv = compute_mtv(rb1.world_polygon(), rb2.world_polygon())
    rb1.pos[0] += mtv[0]
    rb1.pos[1] += mtv[1]

class collsion_body:
    def __init__(self, shape_structure):
        self.shape_structure = shape_structure  # list of points in local space

class rigid_body:
    def __init__(self, body: collsion_body, texture, pos, static):
        self.texture = texture
        self.pos = list(pos)
        self.velocity = [0, 0]
        self.accelation = [0, 0]
        self.body = body
        self.static = static
    
    def apply_force(self, force: list):
        self.velocity[0] += force[0]
        self.velocity[1] += force[1]
    
    def update_pos(self, new_pos):
        self.pos = list(new_pos)

    def world_polygon(self):
        """Return the polygon points in world coordinates (offset by pos)"""
        return [[x + self.pos[0], y + self.pos[1]] for x, y in self.body.shape_structure]

    def check_collsion(self, another_body):
        """Check collision against another rigid_body"""
        return check_collision(self.world_polygon(), another_body.world_polygon())

    def solve_collsion(self, another_body):
        if self.static == 0:
            resolve_collision(self, another_body)

    def step(self):
        self.velocity[0] += self.accelation[0]
        self.velocity[1] += self.accelation[1]
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
