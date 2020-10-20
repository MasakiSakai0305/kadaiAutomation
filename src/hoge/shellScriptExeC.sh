#!/bin/bash
echo shellScriptHoge.sh実行
gcc hoge.c -o hoge
./hoge << EOF
5
1
EOF
echo shellScriptHoge.sh実行終了

