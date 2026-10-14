"""Exact source layout verification with wider limits for long scripts."""
import re
from preparer_v17 import PARTS

def decode_layout(source, start, english):
    """Reconstitue les commandes et les retours 00 / 03 00."""
    if (not english.endswith("[02]") or "@" not in english or
            english.count("\n") > 64 or len(english) > 8000 or
            len(re.findall(r"\[[0-9A-Fa-f ]+\]", english)) > 512):
        return None
    parts = [p for p in PARTS.split(english) if p]
    choices = [(start, 0, [])]  # offset, masque de retours, segments texte
    newline_index = 0
    for part in parts:
        next_choices = []
        if part == "\n":
            for pos, mask, spans in choices:
                for marker, short in ((b"\x00", True), (b"\x03\x00", False)):
                    if source[pos:pos+len(marker)] == marker:
                        next_choices.append((pos+len(marker),
                                             mask | ((1 << newline_index) if short else 0),
                                             spans))
            newline_index += 1
        else:
            if part == "@":
                payload = b"\x70"
            elif part.startswith("[") and part.endswith("]"):
                try:
                    payload = bytes.fromhex(part[1:-1])
                except ValueError:
                    return None
                if not payload:
                    return None
            else:
                if any(not 32 <= ord(c) <= 122 or c in "[]" for c in part):
                    return None
                payload = bytes(ord(c) + 48 for c in part)
            for pos, mask, spans in choices:
                if source[pos:pos+len(payload)] == payload:
                    new_spans = spans if (part == "@" or part.startswith("[")) else spans + [(pos, pos+len(payload))]
                    next_choices.append((pos+len(payload), mask, new_spans))
        choices = next_choices
        if not choices:
            return None
    if len(choices) != 1:
        return None
    end, mask, spans = choices[0]
    return (end, mask, spans) if spans and end > start else None
