"""V61 ROM utilities with the isolated, proven V62 parsing schema."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'v61'))
from build_v61 import *
from parser_v62 import parse,length,spans_fr,commands
