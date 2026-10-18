"""Guard against counting inactive text states as live script access."""
import unittest
from live_text import BASE, STRIDE, TOP, current_pointer
class LiveTextTests(unittest.TestCase):
    def memory(self,index):
        raw=bytearray(TOP+2-BASE);raw[TOP-BASE:TOP+2-BASE]=index.to_bytes(2,'little');return raw
    def test_inactive_stack_ignores_stale_rom_pointers(self):
        raw=self.memory(0xFFFF);raw[:4]=(0xC7E400).to_bytes(4,'little')
        self.assertIsNone(current_pointer(raw))
    def test_only_top_frame_is_live(self):
        raw=self.memory(1);raw[:4]=(0xC7E400).to_bytes(4,'little');raw[STRIDE:STRIDE+4]=(0xF30EE5).to_bytes(4,'little')
        self.assertEqual(current_pointer(raw),{'stack_index':1,'rom_offset':'330EE5'})
        raw[STRIDE:STRIDE+4]=(0x7E1234).to_bytes(4,'little');self.assertIsNone(current_pointer(raw))
    def test_invalid_capture_is_rejected(self):
        with self.assertRaises(ValueError):current_pointer(self.memory(10))
        with self.assertRaises(ValueError):current_pointer(self.memory(1)[:-1])
if __name__=='__main__':unittest.main()
