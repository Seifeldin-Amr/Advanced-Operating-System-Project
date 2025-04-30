def SCAN(cylinders, current_pos, queue):
    
    # Sort the queue
    queue = sorted(queue)
    
    # Initialize variables
    sequence = [current_pos]
    total_distance = 0
    current = current_pos
    direction = 1  # 1 for moving up, -1 for moving down
    
    # Create a copy of the queue to modify
    remaining = queue.copy()
    
    while remaining:
        # Move in current direction until we hit a boundary or find a request
        while True:
            current += direction
            
            # Check if we hit a boundary
            if current >= cylinders:
                current = cylinders - 1
                direction = -1
                break
            elif current < 0:
                current = 0
                direction = 1
                break
            
            # Check if current position has a request
            if current in remaining:
                remaining.remove(current)
                sequence.append(current)
                total_distance += 1
                break
            
            total_distance += 1
    
    return {
        'sequence': sequence,
        'total_distance': total_distance
    }

def LOOK(cylinders, current_pos, queue):
    
    # Sort the queue
    queue = sorted(queue)
    
    # Initialize variables
    sequence = [current_pos]
    total_distance = 0
    current = current_pos
    direction = 1  # 1 for moving up, -1 for moving down
    
    # Create a copy of the queue to modify
    remaining = queue.copy()
    
    while remaining:
        # Find the next request in current direction
        next_request = None
        if direction == 1:
            # Look for requests above current position
            for request in sorted(remaining):
                if request > current:
                    next_request = request
                    break
        else:
            # Look for requests below current position
            for request in sorted(remaining, reverse=True):
                if request < current:
                    next_request = request
                    break
        
        if next_request is None:
            # No more requests in current direction, change direction
            direction *= -1
            continue
        
        # Move to the next request
        total_distance += abs(next_request - current)
        current = next_request
        remaining.remove(current)
        sequence.append(current)
    
    return {
        'sequence': sequence,
        'total_distance': total_distance
    } 