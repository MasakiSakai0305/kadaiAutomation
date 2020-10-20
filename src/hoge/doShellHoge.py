import subprocess

print("コマンド：ls -l")
subprocess.run(['ls', '-l'])

fileName = "hoge"
print("コマンド：gcc hoge.c -o hogeCreateByPython")
subprocess.run(['gcc', '{}.c'.format(fileName), '-o', 'hogeCreateByPython'])

x="""
\n
10
EOF
"""
input_text = """
5
""".strip()
print(input_text)
print("コマンド：./hogeCreateByPython << END_TEXT")
subprocess.run(['./hogeCreateByPython'], input=input_text, text=True)
# subprocess.Popen(['./hogeCreateByPython']).communicate(input="5")
# subprocess.run([])
# subprocess.run([])

# print("入力:5")
# subprocess.run('5')

# print("コマンド：EOF")
# subprocess.run(['EOF'])
