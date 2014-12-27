# -*- coding: utf-8 -*-

# Utils for devkb

import re

digit_regex = re.compile(r'^(?P<comma>\-?[\d,\s]+)$|^(?P<huma>\-?[\d.\s]+[kKmM])$')
huma_dict = {
    'k': 1000,
    'm': 1000000
}

def parse_int(num):
    if isinstance(num, (int, long, float)):
        return int(num)
    elif isinstance(num, basestring):
        num = num.strip()
        matched = digit_regex.search(num)
        if matched is None:
            return float('NaN')
        elif matched.group('comma'):
            return int(''.join(num.split(',')))
        elif matched.group('huma'):
            base = num[0:-1]
            times = num[-1].lower()
            out = float(base) * huma_dict[times]
            return int(out)
        else:
            return float('NaN')
    else:
        return float('NaN')
