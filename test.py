import ipuz
from genxword.control import _, Genxword
import tempfile
import os


def test_ipuz_export():
    with tempfile.TemporaryDirectory() as temp:
        # Move to a temporary directory so we don't clog up anything important
        os.chdir(temp)

        # Generate a simple crossword as .puz
        gen = Genxword(auto=True, mixmode=False)
        gen.wlist([
            'land', 'successful', 'climb', 'yet', 'picture', 'traffic', 'skin', 'leadership', 'threaten', 'win'
        ], 10)
        gen.grid_size()
        gen.gengrid('test', 'z')

        with open('test.ipuz') as fp:
            # This does automatic validation
            ipuz.read(''.join(fp.read()))
