def FIFO(frames, ref_string):
   
    page_frames = [None] * frames
    queue = []
    faults = 0
    hits = 0
    sequence = []
    access_type = []  # True for hit, False for fault
    
    for page in ref_string:
        if page in page_frames:
            hits += 1
            access_type.append(True)  # Hit
        else:
            faults += 1
            access_type.append(False)  # Fault
            if len(queue) < frames:
                # If there's space, add to the end of queue
                queue.append(page)
                page_frames[len(queue) - 1] = page
            else:
                # Replace the oldest page
                oldest = queue.pop(0)
                index = page_frames.index(oldest)
                page_frames[index] = page
                queue.append(page)
        
        # Record the current state
        sequence.append(page_frames.copy())
    
    return {
        'faults': faults,
        'hits': hits,
        'sequence': sequence,
        'access_type': access_type,
        'ref_string': ref_string
    }

def SecondChance(frames, ref_string):
    
   
    page_frames = [None] * frames
    reference_bits = [0] * frames
    queue = []
    faults = 0
    hits = 0
    sequence = []
    ref_bit_history = []
    access_type = []
    
    for page in ref_string:
        if page in page_frames:
            hits += 1
            access_type.append(True)  # Hit
            # Set reference bit to 1
            index = page_frames.index(page)
            reference_bits[index] = 1
        else:
            faults += 1
            access_type.append(False)  # Fault
            if len(queue) < frames:
                # If there's space, add to the end of queue
                queue.append(page)
                page_frames[len(queue) - 1] = page
                reference_bits[len(queue) - 1] = 1
            else:
                # Find a page to replace
                while True:
                    oldest = queue.pop(0)
                    index = page_frames.index(oldest)
                    if reference_bits[index] == 0:
                        # Replace this page
                        page_frames[index] = page
                        reference_bits[index] = 1
                        queue.append(page)
                        break
                    else:
                        # Give second chance
                        reference_bits[index] = 0
                        queue.append(oldest)
        
        # Record the current state
        sequence.append(page_frames.copy())
        ref_bit_history.append(reference_bits.copy())
    
    return {
        'faults': faults,
        'hits': hits,
        'sequence': sequence,
        'reference_bits': ref_bit_history,
        'access_type': access_type,
        'ref_string': ref_string
    } 