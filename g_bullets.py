# g_bullets.py

import upygame

enemyBulletPixels = b'\
\x07\xe7\x00\
\x7e\x6e\x70\
\xe6\x16\xe0\
\x7e\x6e\x70\
\x07\xe7\x00\
'
enemyBullet = upygame.surface.Surface(6, 5, enemyBulletPixels)

enemyBullet02Pixels = b'\
\x05\x35\x00\
\x53\x23\x50\
\x32\x12\x30\
\x53\x23\x50\
\x05\x35\x00\
'
enemyBullet02 = upygame.surface.Surface(6, 5, enemyBullet02Pixels)

playerBulletPixels = b'\
\x55\x32\x12\x30\
\x53\x21\x13\x30\
\x55\x32\x12\x30\
\x53\x21\x13\x30\
\x55\x32\x12\x30\
'
playerBullet = upygame.surface.Surface(8, 5, playerBulletPixels)

playerPowerBulletPixels = b'\
\x88\x7e\x6e\x70\
\x87\xe6\x67\x70\
\x88\x7e\x6e\x70\
\x87\xe6\x67\x70\
\x88\x7e\x6e\x70\
'
playerPowerBullet = upygame.surface.Surface(8, 5, playerPowerBulletPixels)
