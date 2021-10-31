#!/usr/bin/env python3
import sys
from pathlib import Path
from textwrap import dedent
import wget

from eman import EPISODES, ROOT

OUT=sys.stdout

def fd_write(block):
    OUT.write( dedent(block) )
PRELUDE="""\
    #!/bin/bash

    BUILD=./eating.tmp

    die () { echo $BUILD already exists. Remove it first.; exit; }

    [ -d $BUILD ] && die
    [ -f $BUILD ] && die

    mkdir $BUILD
    pushd $BUILD > /dev/null

    which wget || {
        echo wget is unavailable on this host.
        echo executing a dry run, emulating downloads.
        echo all 'downloaded' files will be empty.
        wget () { touch $(basename $1); }
    }

    process () {
        url=$1
        mp4=$2
        png=$3
        printf .
        wget $url
        mv $png $mp4
    }
    """

POSTLUDE="""
    popd > /dev/null
    """

def main():
    paths = list(EPISODES.glob('*'))
    paths.sort()
    fd = sys.stdout
    fd_write(PRELUDE)
    for path in paths:
        load_episode(path,fd)
    fd_write(POSTLUDE)

def load_episode(path,fd):
        episode_name = path.name.split('.')[0]
        fd_write(f"""
            echo {episode_name}
            mkdir {episode_name}
            pushd {episode_name} > /dev/null
            """)

        urls=list(urls_4_file(path))
        for ii,url in enumerate(urls):
            seq = str(10000 + ii)[-4:]
            name=Path(url).name.split('.')[0]
            png = name + '.png'
            mp4 = f"{episode_name}_{seq}.mp4"
            fd_write(f"""
                process {url} {mp4} {png}
                """)
        fd_write(f"""
            popd > /dev/null
            echo
            """)

def urls_4_file(path):
    text = path.read_text()
    parts = text.split()
    for part in parts:
        if part.startswith('http'):
            yield part


if __name__ == '__main__':
    main()
