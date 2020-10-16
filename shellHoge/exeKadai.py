import subprocess
import os

jugyoNum = 1
path = "./kadaiPrograms/{}kai".format(jugyoNum)

def decodeByteToStr(byte_list: list) -> list:
	return  [i.decode('utf8') for i in byte_list]

def compileAssignments(specificFiles):
    print('\n*****コンパイル状況*****\n')
    compileError = []
    for i, file in enumerate(specificFiles):
        print("file:{}".format(file))
        p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format("1") + file , '-o', './kadaiPrograms/{}kai/exec/'.format(1) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.readlines()
        stderr = p.stderr.readlines()
        print('対象ファイル: {0} ({1}/{2})'.format(file, i+1, len(specificFiles)))
        print('return: {}'.format(p.wait()))
        print('stdout: {}'.format(''.join(decodeByteToStr(stdout))))
        print('stderr:\n{}'.format(''.join(decodeByteToStr(stderr))))
        if len(stderr) > 0:
            compileError.append([file.rstrip('.c'), ''.join(decodeByteToStr(stderr))])
            os.remove('./kadaiPrograms/{}kai/exec/'.format(1) + file.rstrip('.c'))
    return compileError

if __name__ == "__main__":
    jugyoNum = 1
    path = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    files = os.listdir(path=path)
    compileError = compileAssignments(files)