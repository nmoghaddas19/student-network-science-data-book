import os
import time

os.system('git fetch upstream && git diff main upstream/main > diff.diff')

with open("diff.diff", 'r') as f:
    block = []
    blocks = []
    for line in f.readlines():
        if line.startswith('diff --git'):
            if len(block) != 0:
                blocks.append(block)
                block = []
        block.append(line)
    blocks.append(block)

fnames_to_ignore = []
fnames_to_move = []
for b in blocks:
    fname = b[0][12:].split()[0]
    if b[1].startswith('new file mode '):
        fnames_to_ignore.append(fname)
    else:
        fnames_to_move.append(fname)

for fname in fnames_to_move:
    fname_extension = fname.split('.')[-1]
    fname_prefix = '.'.join(fname.split('.')[:-1])
    new_fname = fname_prefix + '_MODIFIED_{}'.format(str(time.time()).split('.')[0]) + '.' + fname_extension
    os.system('cp {} {}'.format(fname[1:], new_fname[1:]))

os.system('git checkout main')
os.system('git merge upstream/main')
