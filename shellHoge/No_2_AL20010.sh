#!/bin/bash
gcc kihon2-1-AL20010.c -o kihon2-1-AL20010
gcc kihon2-2-AL20010.c -o kihon2-2-AL20010
gcc hatten2-1-AL20010.c -o hatten2-1-AL20010
gcc hatten2-2-AL20010.c -o hatten2-2-AL20010
./kihon2-1-AL20010 << EOF
1
2
EOF
./kihon2-1-AL20010 << EOF
2
EOF
./kihon2-1-AL20010 << EOF
3
EOF
./kihon2-2-AL20010 << EOF
4
EOF
./kihon2-2-AL20010 << EOF
5
EOF
./kihon2-2-AL20010 << EOF
6
EOF
./kihon2-2-AL20010 << EOF
7
EOF
./kihon2-1-AL20010 << EOF
8
EOF
./kihon2-1-AL20010 << EOF
9
EOF
./kihon2-1-AL20010 << EOF
10
EOF
./kihon2-1-AL20010 << EOF
11
EOF
./kihon2-2-AL20010 << EOF
12
EOF
./kihon2-2-AL20010 << EOF
13
EOF
./kihon2-2-AL20010 << EOF
14
EOF
