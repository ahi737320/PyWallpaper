def hex_to_RGB(hex_value):
    return ((hex_value>>8>>8)%256, (hex_value>>8)%256, hex_value%256)
