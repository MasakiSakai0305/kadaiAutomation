import os
if __name__ == "__main__":
    path = "./kadaiPrograms/"
    number = 2
    for number in range(3, 15):
        os.makedirs(path + "{}kai/codes/ok".format(number))
        os.makedirs(path + "{}kai/exec/ok".format(number))