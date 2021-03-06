from keypipe import seal

from test.helpers import *

def test_empty():
    expected=b'\x01' + b'\x00' * 12 + uh('763c62df413000674199240567321ec1')
    assert do_aepipe(docs_key, b'', seal) == expected

def test_multiblock():
    buf = BytesIO()
    with aepipe_ctx(docs_key, buf, seal) as p:
        for i in range(128):
            os.write(p, b'\x00' * 8192)
    open('hi', 'wb').write(buf.getvalue())

def test_gcm13():
    expected = b'\x01' + b'\x00' * 12 + uh('530f8afbc74536b9a963b4f1c4cb738b')
    assert do_aepipe(b'\x00' * 32, b'', seal) == expected

def test_gcm14():
    expected = (b'\x01' + b'\x00' * 8 + b'\x00\x00\x00\x10' +
        uh('d0d1c8a799996bf0265b98b5d48ab919' +
            'cea7403d4d606b6e074ec5d3baf39d18') + 
        uh('0' * 8 + '8486364fc8409762f6e6232b65376b97'))
    assert do_aepipe(b'\x00' * 32, b'\x00'*16, seal) == expected
