# g_milkstation.py

import upygame

milkStationPixels = b'\
\x00\x00\x00\x00\x00\x00\x11\x11\x11\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x01\x22\x22\x22\x10\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x12\x22\x22\x22\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x22\x33\x33\x22\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x23\x3d\xdd\xd2\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\x33\x32\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\xd3\x32\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\x33\x32\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\xdd\xd2\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\x33\x32\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\x3d\xd3\x32\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x33\xbd\xbb\xbb\x21\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x3b\xbd\xdd\xbb\xb1\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x0c\xcc\xbd\xbb\xbb\xcc\xc0\x00\x00\x00\x00\
\x00\x00\x00\x00\x0b\xbc\xcc\xcc\xcc\xcb\xb0\x00\x00\x00\x00\
\x00\x00\x00\x00\x0c\xdb\xbb\xbb\xbb\xbd\xc0\x00\x00\x00\x00\
\x00\x00\x00\x00\x0c\xdb\xcc\xcc\xcc\xbd\xc0\x00\x00\x00\x00\
\x00\x00\x00\x00\x0c\xdd\xcc\xcc\xcc\xdd\xc0\x00\x00\x00\x00\
\x00\x0c\xbc\xbb\x1c\xdd\xcc\xcc\xcc\xdd\xc1\xbb\xcb\xc0\x00\
\x00\xcb\xcc\xcc\xcc\xdd\xcc\xcc\xcc\xdd\xcc\xcc\xcc\xbc\x00\
\x00\xcc\x00\x00\x0c\xdd\xcc\xcc\xcc\xdd\xc0\x00\x00\xcc\x00\
\x00\xcc\x00\x00\x0c\xdd\xcc\xcc\xcc\xdd\xc0\x00\x00\xcc\x00\
\x0c\xcc\xc0\x00\x0c\xdc\xbb\xbb\xbb\xcd\xc0\x00\x0c\xcc\xc0\
\xcc\xcc\xcc\x00\x0c\xcb\xbb\xbb\xbb\xbc\xc0\x00\xcc\xcc\xcc\
'
milkStation = upygame.surface.Surface(30, 24, milkStationPixels)

kittyPixels = b'\
\x00\x01\x11\x11\x00\x00\
\x00\x2e\x22\x2e\x10\x00\
\x02\x3e\xe3\xee\x21\x00\
\x0e\xe0\xe6\xe0\xee\x00\
\x03\xee\x6d\x6e\xe2\x00\
\x0e\xee\xdd\xde\xee\x00\
\x03\x33\x33\x33\x32\x00\
\x00\x00\x11\xb0\x00\x00\
\x01\xc1\xbb\xbb\xc1\x00\
\x1b\xcb\xbb\xbb\xcb\xb0\
\xb0\x0c\xbb\xbc\x00\xb0\
\x00\x00\xcc\xc0\x00\x00\
\x00\x01\xbc\xbb\x00\x00\
\x00\x1b\x00\x0b\xb0\x00\
'
kitty = upygame.surface.Surface(12, 14, kittyPixels)

