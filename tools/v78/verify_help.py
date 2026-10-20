"""Check paired item-help and stock-display evidence for the current checkpoint."""
import json
from verify_remaining import ROOT,verify
if __name__=='__main__':print(json.dumps(verify(ROOT/'tests/emulation_v78_help'),indent=2))
