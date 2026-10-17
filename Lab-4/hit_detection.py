"""
hit_detection: figures out whether a click landed on a target.
"""


import math

def check_hit(pos, targets):
    """
    Checks if a click position (x, y) lands inside any circular target in the list.
    
    :param targets: List of Target instances or a single Target instance
    :param pos: Tuple of (click_x, click_y)
    :return: The target object that was hit, or None if missed
    """
    click_x, click_y = pos

    # Handle case where targets is a list of Target objects
    if isinstance(targets, list):
        for target in targets:
            distance = math.hypot(click_x - target.x, click_y - target.y)
            if distance <= target.radius:
                return target  # Return the specific target that was hit
        return None  # No target was hit (miss)
    
    # Handle case where a single Target instance is passed directly
    else:
        distance = math.hypot(click_x - targets.x, click_y - targets.y)
        if distance <= targets.radius:
            return targets
        return None
