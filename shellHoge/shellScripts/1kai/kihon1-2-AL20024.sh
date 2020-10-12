#!/bin/bash
cd ../../kadaiPrograms/1kai
gcc kihon1-2-AL20024.c -o kihon1-2-AL20024
./kihon1-2-AL20024 << EOF
1
EOF
./kihon1-2-AL20024 << EOF
2
EOF
./kihon1-2-AL20024 << EOF
0
EOF
./kihon1-2-AL20024 << EOF
-1
EOF