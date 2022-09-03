# -*- coding: utf8 -*-
import random
import subprocess


def edit_text(content: str) -> str:
    """调起外部编辑器来编辑文本并读入完整的内容。"""
    filename = '/tmp/fledgling_{}.txt'.format(random.randint(0, 100))
    with open(filename, 'w') as f:
        f.write(content)

    p = subprocess.Popen(['/usr/bin/vim', filename])
    p.wait()
    with open(filename) as f:
        return f.read()
