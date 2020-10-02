#!/bin/bash
echo shellScriptHoge.sh実行
gcc hoge.c -o hoge
./hoge << EOF
100
EOF