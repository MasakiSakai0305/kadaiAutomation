import os
import glob

def remove_glob(pathname, recursive=True):
    print("削除するファイルのパス: {}".format(pathname))
    for p in glob.glob(pathname, recursive=recursive):
        if os.path.isfile(p):
            print("削除: {}".format(p))
            os.remove(p)
            
if __name__ == "__main__":
    
    jugyoNum = input("削除する授業の回を入力: ")
    path = "./kadaiPrograms/{}kai/".format(jugyoNum)
    remove_glob(pathname=path + "codes/ok/*.c")
    remove_glob(pathname=path + "exec/ok/*")