def transform_position(x, y, play_y, play_h, local_id):
    if local_id == 1:
        y = play_y + play_h - (y - play_y)
    return x, y
