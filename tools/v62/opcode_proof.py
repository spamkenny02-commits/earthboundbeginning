"""Byte-anchored proof of the remake's 1A 21: 32-bit equality, no operand.
Only read-only analysis: this module never writes ROM or emulator memory.
"""
ANCHORS={
 'active_window_getter':(0x10301,'c231ade088c9ffffd005a9fe858013ad5889227b9af8eaa0520022f78fc01869508660'),
 'open_window_index_hook':(0x389A7B,'aabde48829ff00898000f0030900ff6b'),
 'main_1a_dispatch':(0x18AD4,'a0567b841e4c5487'),
 'patched_1a_tree':(0x17B56,'c2310b7b69eeff5b220ebff8a900002b60'),
 'indexed_long_dispatch':(0x38BF0E,'da8a0a0aaabfd0bdf88dbc00e8e8bfd0bdf88dbe00fa8adcbc00'),
 'subcommand_21_pointer':(0x38BE54,'4db9f700'),
 'equality_handler':(0x37B94D,'c2310b487b69eeff5b6822cbbef8a5068500a508850222c4bef8640e6410a606e400f0034c7fb9a608e402f0034c7fb9e60e22e9bef82b6b'),
 'argument_getter_bridge':(0x38BEC4,'f402005cdc03c1'),
 'working_getter_bridge':(0x38BECB,'f402005c0a04c1'),
 'working_setter_bridge':(0x38BEE9,'f402005c5d04c1'),
 'argument_getter':(0x103DC,'c2310b7b69f2ff5b20010318691b00a8b900008506b902008508a5068514a50885162b60'),
 'working_getter':(0x1040A,'c2310b7b69f2ff5b20010318691700a8b900008506b902008508a5068514a50885162b60'),
 'working_setter':(0x1045D,'c2310b7b69f2ff5ba51c8506a51e850820010318691700a8a506990000a508990200a5068514a50885162b60')
}
SOURCE='https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/'
def prove(data):
 for label,(a,h) in ANCHORS.items():
  if data[a:a+len(bytes.fromhex(h))]!=bytes.fromhex(h):raise ValueError('Preuve moteur divergente: '+label)
 return {'opcode':'1A 21','length_bytes':2,'operand_bytes':0,'semantics':'working_memory = 1 if working_memory == argument_memory else 0; both operands are 32-bit','handler_offset':'37B94D','dispatch_table_offset':'38BDD0','subcommand_index':33,'script_pointer_read_or_increment_in_handler':False,'anchors':{label:{'offset':f'{a:06X}','hex':h} for label,(a,h) in ANCHORS.items()},'primary_sources':[SOURCE+p for p in ('src/text/display_text.asm','src/text/ccs/tree_1A.asm','src/text/get_argument_memory.asm','src/text/get_working_memory.asm','src/text/set_working_memory.asm')],'scope':'The original disassembly explains the dispatch/getter conventions; the remake-specific hook and equality body are verified from its ROM bytes.'}
