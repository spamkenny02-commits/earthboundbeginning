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

class EvidenceTests(unittest.TestCase):
    def test_published_traces_are_consistent(self):
        import collections,json
        from pathlib import Path
        root=Path(__file__).resolve().parents[2]
        expected={'use_card','eat_card','give_card_to_self','drop_card','help_card','telepathy','help_card_description'}
        for profile in ('accents','ascii'):
            report=json.loads((root/f'tests/emulation_v63/results_{profile}.json').read_text())
            self.assertEqual(set(report['cases']),expected)
            self.assertFalse(report['rom_modified_for_probe']);self.assertFalse(report['wram_written_by_probe'])
            for case in report['cases'].values():
                counts=collections.Counter();events=case['events'];n=case['sampled_frames']
                self.assertEqual(case['returncode'],0)
                self.assertTrue(events)
                self.assertLessEqual(events[-1]['frame'],n)
                for i,event in enumerate(events):
                    stop=events[i+1]['frame'] if i+1<len(events) else n+1
                    self.assertGreater(stop,event['frame'])
                    if event['pointer']:counts[event['pointer']['rom_offset']]+=stop-event['frame']
                self.assertEqual(dict(counts),case['pointer_frame_counts'])
                self.assertTrue((root/case['capture']['path']).is_file())

if __name__=='__main__':unittest.main()
