"""Synthetic safety tests: do not require a commercial ROM or claim integration."""
import unittest
from audit_v30 import span_reason, commands_preserved


class CandidateSafety(unittest.TestCase):
    def setUp(self):
        self.source = b'\x08\x70' + bytes(ord(c)+48 for c in 'Hello world!') + b'\x02'
        self.a, self.b = 2, len(self.source)-1
        self.occupied = bytearray(len(self.source))
        self.baselines = [self.source, self.source]
        self.refs = [{0: [20]}, {0: [20]}, {0: [20]}]

    def gate(self, **changes):
        return span_reason(changes.get('source', self.source),
                           changes.get('baselines', self.baselines),
                           changes.get('occupied', self.occupied),
                           changes.get('refs', self.refs),
                           changes.get('a', self.a), changes.get('b', self.b))

    def test_safe_plain_text(self):
        self.assertIsNone(self.gate())

    def test_invalid_bounds(self):
        self.assertEqual(self.gate(a=-1), 'invalid_bounds')
        self.assertEqual(self.gate(b=len(self.source)+1), 'invalid_bounds')

    def test_ips_collision(self):
        self.occupied[self.a+1] = 1
        self.assertEqual(self.gate(), 'ips_collision')

    def test_baseline_changed(self):
        bad = bytearray(self.source)
        bad[self.a] ^= 1
        self.assertEqual(self.gate(baselines=[self.source, bytes(bad)]), 'baseline_changed')

    def test_wrong_baseline_size(self):
        self.assertEqual(self.gate(baselines=[b'']), 'wrong_baseline_size')

    def test_all_incoming_text_pointers_deferred(self):
        for target in (self.a, self.a+3, self.b-1):
            self.assertEqual(self.gate(refs=[{}, {target: [0]}]), 'interior_or_direct_pointer')
        self.assertIsNone(self.gate(refs=[{}, {self.b: [0]}]))

    def test_command_bytes_rejected(self):
        altered = self.source[:self.a+2] + b'\x01' + self.source[self.a+3:]
        self.assertEqual(self.gate(source=altered, baselines=[altered]), 'not_plain_ascii_text')

    def test_preserve_commands_across_profiles(self):
        self.assertTrue(commands_preserved(self.source, self.baselines, 0,
                                           len(self.source), [(self.a, self.b)]))
        changed = bytearray(self.source)
        changed[0] = 0x09
        self.assertFalse(commands_preserved(self.source, [self.source, bytes(changed)],
                                            0, len(self.source), [(self.a, self.b)]))

    def test_text_change_allowed_but_not_command_change(self):
        changed = bytearray(self.source)
        changed[self.a] ^= 1
        self.assertTrue(commands_preserved(self.source, [bytes(changed)], 0,
                                           len(self.source), [(self.a, self.b)]))

    def test_invalid_mask_rejected(self):
        self.assertFalse(commands_preserved(self.source, self.baselines, 0,
                                            len(self.source), [(0, len(self.source)+1)]))


if __name__ == '__main__':
    unittest.main()
