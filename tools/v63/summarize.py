"""Compare sampled DISPLAY_TEXT cursors with V62's static graph.
A cursor points at the next script byte, not necessarily a displayed glyph.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'v62'))
import runtime as b
from live_text import prove
ROOT=b.ROOT

def summarize(source, data, result, audit):
    prove(source);prove(data)
    assert b.sha(data)==result['rom_sha256']==audit['baseline_sha256']
    assert result['rom_modified_for_probe'] is False and result['wram_written_by_probe'] is False
    ranges=[]
    for root in audit['paths']:
        a=int(root,16);p=b.parse(data,a,8192,extra_glyphs=range(0xB0,0xC0))
        if not p['error'] and p['terminal']:ranges.append((a,p['end']))
    cases={}
    for name,c in result['cases'].items():
        assert c['returncode']==0 and c['sampled_frames']>0
        observed={int(a,16) for a in c['pointer_frame_counts']}
        # Include the end cursor: after consuming a terminal byte, the saved
        # pointer can point one byte past the script. It is not a new entry.
        missing=sorted(a for a in observed if not any(lo<=a<=hi for lo,hi in ranges))
        groups=[]
        for a in missing:
            if groups and a-groups[-1][-1]<=16:groups[-1].append(a)
            else:groups.append([a])
        cases[name]={'sampled_frames':c['sampled_frames'],'unique_rom_cursors':len(observed),'cursors_outside_v62_parsed_intervals':len(missing),'outside_cursor_groups':[{'first':f'{g[0]:06X}','last':f'{g[-1]:06X}','sampled_cursors':[f'{a:06X}' for a in g]} for g in groups]}
    return {'version':'v63','profile':result['profile'],'input_patch':'v61','new_ips':False,'rom_sha256':b.sha(data),'comparison':'Sampled next-byte cursors versus successfully parsed V62 script intervals (including end cursors)','frame_sampling_is_exhaustive':False,'outside_cursor_is_new_english_text':False,'natural_controller_routes_from_saved_state':True,'full_game_text_completion_certified':False,'cases':cases}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for n in ('rom','results','out'):ap.add_argument('--'+n,type=Path,required=True)
    args=ap.parse_args();source=args.rom.read_bytes();assert b.sha(source)==b.ROM_SHA
    result=json.loads(args.results.read_text());p=result['profile']
    data=b.apply(source,b.records((ROOT/f'patches/EarthBound_Beginnings_FR_v61_{p}.ips').read_bytes()))
    suffix='_ascii' if p=='ascii' else ''
    audit=json.loads((ROOT/f'tools/v62/alias_audit_v62{suffix}.json').read_text())
    args.out.write_text(json.dumps(summarize(source,data,result,audit),indent=2)+'\n')
