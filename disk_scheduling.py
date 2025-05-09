def SCAN(request_queue, head_start, disk_size, direction="right"):
    request_queue.append(disk_size-1)
    page_frames = sorted(request_queue)
    left = [r for r in page_frames if r < head_start]
    right = [r for r in page_frames if r >= head_start]

    seek_sequence = []
    seek_distance = 0
    current = head_start

    if direction == "right":
        # Move right
        for r in right:
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
        # Go to end of disk
        if current != disk_size - 1:
            seek_distance += abs(current - (disk_size - 1))
            current = disk_size - 1
        # Then reverse and move left
        for r in reversed(left):
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
    else:
        # Move left
        for r in reversed(left):
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
        # Go to start of disk
        if current != 0:
            seek_distance += abs(current - 0)
            current = 0
        # Then reverse and move right
        for r in right:
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
        

    return {
        'sequence': seek_sequence,
        'seek_distance': seek_distance,
    }

def LOOK(request_queue, head_start, direction="right"):
    page_frames = sorted(request_queue)
    left = [r for r in page_frames if r < head_start]
    right = [r for r in page_frames if r >= head_start]

    seek_sequence = []
    seek_distance = 0
    current = head_start

    if direction == "right":
        for r in right:
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
        for r in reversed(left):
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
    else:
        for r in reversed(left):
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r
        for r in right:
            seek_sequence.append(r)
            seek_distance += abs(current - r)
            current = r

    return {
        'sequence': seek_sequence,
        'seek_distance': seek_distance,
    } 