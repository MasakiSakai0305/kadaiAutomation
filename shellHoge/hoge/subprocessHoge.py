import subprocess

print(subprocess.call(['cat', 'hello.py'])) # 0
# 標準入力・標準出力を指定する（2つ目はhello2.pyが作成される）
print(subprocess.call(['cat'], stdin=open('hello.py','rb'))) # 0