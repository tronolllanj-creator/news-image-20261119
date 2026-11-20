import os
import shutil
import sys

def main():
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'out')
    os.makedirs(output_dir, exist_ok=True)
    
    src = 'entry.png'
    dst = os.path.join(output_dir, 'entry.png')
    
    shutil.copy2(src, dst)
    
    with open(dst, 'rb') as f:
        magic = f.read(8)
    
    if magic != b'\x89PNG\r\n\x1a\n':
        print(f"Error: {dst} is not a valid PNG", file=sys.stderr)
        sys.exit(1)
    
    size = os.path.getsize(dst)
    print(f"{dst} {size}")

if __name__ == '__main__':
    main()
