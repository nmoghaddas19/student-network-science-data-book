import os
import time
import glob

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

fname_wildcards = []
for fname in fnames_to_move:
    fname_extension = fname.split('.')[-1]
    fname_prefix = '.'.join(fname.split('.')[:-1])
    fname_wildcards.append(fname_prefix + '_MODIFIED_*.' + fname_extension)
    new_fname = fname_prefix + '_MODIFIED_{}'.format(str(time.time()).split('.')[0]) + '.' + fname_extension
    os.system('cp {} {}'.format(fname[1:], new_fname[1:]))

os.system('git checkout main')
os.system('git merge upstream/main')

for wildcard in fname_wildcards:
    print(wildcard)
    keepers = []
    fnames_from_most_recent = sorted([f for f in glob.glob(wildcard[1:])])
    print(fnames_from_most_recent)
    for idx in range(1, len(fnames_from_most_recent)):
        os.system('cmp --silent -- {} {} > mod.txt'.format(
            fnames_from_most_recent[0], 
            fnames_from_most_recent[idx],
        ))
        with open('mod.txt', 'r') as f:
            bytes_diff = ''
            for line in f.readlines():
                bytes_diff.append(line)
            print(len(bytes_diff))
        if len(bytes_diff) == 0:
            os.system('rm {}'.format(fnames_from_most_recent[idx]))
        
                  
        
    
    

