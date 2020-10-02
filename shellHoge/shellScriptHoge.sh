#!/bin/bash
echo shellScriptHoge.sh実行
gcc hogeho.c -o hoge
./hoge << EOF
5
EOF
echo shellScriptHoge.sh実行終了

