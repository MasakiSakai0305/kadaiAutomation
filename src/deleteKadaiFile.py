import os
import glob

def remove_glob(pathname, recursive=True):
    print("\n削除するファイルのパス: {}".format(pathname))
    print("削除するファイルの数: {}\n".format(len(glob.glob(pathname, recursive=recursive))))
    for p in glob.glob(pathname, recursive=recursive):
        if os.path.isfile(p):
            print("削除: {}".format(p))
            os.remove(p)
          
if __name__ == "__main__":
    
    jugyoNum = input("削除する授業の回を入力: ")
    path = "./kadaiPrograms/{}kai/".format(jugyoNum)
    remove_glob(pathname=path + "codes/ok/*.c")
    remove_glob(pathname=path + "exec/ok/*")

    if input("okフォルダに入っていないファイルも削除しますか[y/n]") == "y":
        remove_glob(pathname=path + "codes/*.c")
        remove_glob(pathname=path + "exec/*")
    
    else:
        print("終了")