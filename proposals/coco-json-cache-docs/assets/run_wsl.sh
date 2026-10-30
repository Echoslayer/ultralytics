#!/bin/bash
S=<scratch>
W="$HOME/verify_note_ext4"
echo "fs: $(stat -f -c %T "$HOME")"
python3 -I "$S/verify_hash_posix.py" /mnt/d/tools/ultralytics/.worktrees/coco-json-cache/ultralytics/data/utils.py "$W" "${1:-0}" | sed "s#$HOME#~#"
rm -rf "$W"
# directory size before/after unlink, and timestamp tick
D="$HOME/tick_probe"; mkdir -p "$D"; s0=$(stat -c %s "$D"); touch "$D/a"; rm "$D/a"; echo "dir size: $s0 -> $(stat -c %s "$D")"
python3 -c "
import os,time
p='$D/t'; ts=set()
for _ in range(20000):
    open(p,'w').close(); ts.add(os.stat(p).st_mtime_ns)
v=sorted(ts); print('distinct mtimes in 20000 writes:', len(v), '| min step ms:', round(min(b-a for a,b in zip(v,v[1:]))/1e6,3) if len(v)>1 else None)
"
rm -rf "$D"
