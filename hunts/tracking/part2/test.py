#!/usr/bin/env python3

import pytest
import solve

@pytest.mark.parametrize('expected,arg', [
    (b'\x06', '00000110'),
    (b'a',    '01100001')
])
def test_octet_to_byte(expected, arg):
    assert expected == solve.octet_to_byte(arg)
