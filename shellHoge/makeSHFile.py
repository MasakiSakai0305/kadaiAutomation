import json
studentIDList = [23,24,25,26,27,28,29,30,32,33,35,36]

def makeSHFiles(studenID: int, jugyoNum: int):
    """
    jsonを読み込んで，自動的にシェルスクリプトを作成する．

    args
        studentID: int
            学籍番号（下二桁）
        jugyoNum: int
            授業の回
        kadaiNum: str
            課題番号(例: kihon1)
    """

    jsonPath = "json/{}kai.json".format(jugyoNum)
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kadaiNums = list(jsonDict.keys())


if __name__ == "__main__":
   makeSHFiles(studenID=23, jugyoNum=1) 