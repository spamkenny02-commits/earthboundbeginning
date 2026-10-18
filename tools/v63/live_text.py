"""Read the current DISPLAY_TEXT frame without changing emulated memory.
Frame sampling is not a CPU trace: code completed within one frame can be missed.
"""
BASE, STRIDE, COUNT, TOP = 0x96AA, 27, 10, 0x97B8
ANCHORS = {
    'allocate_text_state': (0x14012, 'c2310b7b69f2ff5baeb897e88eb8978602a90a0018e50270041007800230039cb897adb89785040a65040a0a65040a65041869aa962b60'),
    'initialize_text_pointer': (0x1866D, 'c2310b487b69f0ff5b68850ea51e8506a5208508a50ed005a900008011aa9e0400a8a506990000a508990200a50e2b60'),
}
def prove(data):
    for label, (address, value) in ANCHORS.items():
        expected = bytes.fromhex(value)
        if data[address:address+len(expected)] != expected:
            raise ValueError('Unexpected engine bytes: ' + label)
    return {k: {'offset': f'{a:06X}', 'hex': h} for k, (a, h) in ANCHORS.items()}

def current_pointer(raw, start=BASE):
    """Return only the top state. Inactive states contain stale pointers."""
    if start > BASE or start + len(raw) < TOP + 2:
        raise ValueError('Incomplete DISPLAY_TEXT state capture')
    index = int.from_bytes(raw[TOP-start:TOP-start+2], 'little')
    if index == 0xFFFF:
        return None
    if index >= COUNT:
        raise ValueError(f'Invalid text stack index: {index}')
    offset = BASE + index * STRIDE - start
    pointer = int.from_bytes(raw[offset:offset+4], 'little')
    # This audit follows ROM text, not strings generated in WRAM.
    if not 0xC00000 <= pointer < 0x1000000:
        return None
    return {'stack_index': index, 'rom_offset': f'{pointer-0xC00000:06X}'}
