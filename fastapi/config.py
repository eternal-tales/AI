#@markdown # Dependencies

from IPython.utils import capture
import time
import os

print('[1;32mInstalling dependencies...')
with capture.capture_output() as cap:
    os.chdir('/content')
    !pip install -qq --no-deps accelerate==0.12.0
    !wget -q -i https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dependencies/dbdeps.txt
    !dpkg -i *.deb
    !tar -C / --zstd -xf gcolabdeps.tar.zst
    !rm *.deb | rm *.zst | rm *.txt
    !git clone -q --depth 1 --branch main https://github.com/TheLastBen/diffusers
    !pip install gradio==3.16.2 --no-deps -qq

    if not os.path.exists('gdrive/MyDrive/sd/libtcmalloc/libtcmalloc_minimal.so.4'):
        %env CXXFLAGS=-std=c++14
        !wget -q https://github.com/gperftools/gperftools/releases/download/gperftools-2.5/gperftools-2.5.tar.gz && tar zxf gperftools-2.5.tar.gz && mv gperftools-2.5 gperftools
        !wget -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/Patch
        %cd /content/gperftools
        !patch -p1 < /content/Patch
        !./configure --enable-minimal --enable-libunwind --enable-frame-pointers --enable-dynamic-sized-delete-support --enable-sized-delete --enable-emergency-malloc; make -j4
        !mkdir -p /content/gdrive/MyDrive/sd/libtcmalloc && cp .libs/libtcmalloc*.so* /content/gdrive/MyDrive/sd/libtcmalloc
        %env LD_PRELOAD=/content/gdrive/MyDrive/sd/libtcmalloc/libtcmalloc_minimal.so.4
        %cd /content
        !rm *.tar.gz Patch && rm -r /content/gperftools
    else:
        %env LD_PRELOAD=/content/gdrive/MyDrive/sd/libtcmalloc/libtcmalloc_minimal.so.4

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    os.environ['PYTHONWARNINGS'] = 'ignore'

print('[1;32mDone, proceed')