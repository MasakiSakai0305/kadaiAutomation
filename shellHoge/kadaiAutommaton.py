from exeSH import executeKadaiAndGetOutputResult
from exeSH import getStudentID
from exeSH import checkKadai
from exeSH import checkKadaiString
from exeSH import parseJsonAndGetAnswers
from exeSH import parseJsonAndGetCheckPoint

import subprocess
import re
from typing import List
import json
import os


class jugyoKadai:
    def __init__(self, jugyoNo, kihonNum, hattenNum):
        #授業の回数(n回目)
        self.jugyoNo = jugyoNo
        #その回の基本課題の数(shファイル作成に使用)
        self.kihonNum = kihonNum
        #発展課題の数(shファイル作成に使用)
        self.hattenNum = hattenNum
        #チェックを終えた課題をリスト化し，重複実行しないようにする（仮）
        self.checkedKadaiList = []
    
    def checkKadaiByExecuteSHFile(self):
        """
        shファイルを実行して課題のチェックを行う関数
        以下の動作を行う．
        1. ディレクトリ内のc言語（学生が提出したもの）を探索
        2. 存在するcファイルに該当するshファイルのみ選択
        3. 選択されたshファイルの実行
            3.1 課題チェックの方法が違うので，方法の選択
                出力された数字で見る場合もあれば，文字列がチェックの対象となる場合もある
        4. 実行した課題の正解・不正解を表示

        """

        for check in ["kihon1-1-AL20024", "kihon1-2-AL20024"]:
            print("check:{}".format(check))
            self.executeSHFile(kadaiFileName=check)
        pass
    
    def searchCProgramFile(self) -> List[str]:
        """
        ディレクトリ内を探索し，全ての課題のファイル名をリストとして返す

        return
            ディレクトリ内の全ての課題のファイル名が格納されているリスト
            kadaiFiles: List[str]
        
        """

        path = "kadaiPrograms/{}kai".format(self.jugyoNo)
        listdir = os.listdir(path)
        files = [f for f in listdir if os.path.isfile(os.path.join(path, f))]
        kadaiFiles = [cFile.split(".c")[0] for cFile in files if os.path.splitext(cFile)[1] == ".c"]
        return kadaiFiles

    def listUncheckedKadai(self, kadaiFiles: List[str]) -> List[str]:
        """
        ディレクトリ内の課題名リスト受け取り，チェックしていない課題のファイル名のみをリストとして返す．
        1. logファイル(チェックしている課題名のみ記載されている)をオープン
        2. 記載されていないもののみ，抽出してリスト化

        args
            全ての課題のファイル名が格納されているリスト
            kadaiFiles: List[str]

        return
            まだチェックしていないファイル名が格納されているリスト
            uncheckedKadaiFiles: List[str]
        """
        uncheckedKadaiFiles = []
        filePath = "kadaiPrograms/{}kai/kadaiCheckLog.csv".format(self.jugyoNo)
        with open(filePath, "r") as f:
            checkedFiles = [s.strip() for s in f.readlines()]
            

        for kadai in kadaiFiles:
            if kadai not in checkedFiles:
                uncheckedKadaiFiles.append(kadai)
        print(uncheckedKadaiFiles)
        return uncheckedKadaiFiles

    def writeCheckedKadaiToLogFile(self, kadaiFileName: str, result: bool):
        """
        実行した課題名(ex, kihon1-1-AL20023)をログファイルへ記載する
        正解の時のみ記載する，不正解の時が記載しない
        args
            kadaiFileName: str,  学生の課題のファイル名（.c拡張子なし）
                例：kihon1-1-AL20024
            result: bool
                正解:True, 不正解:False
        """
        #print(os.getcwd())
        #print(result)
        if result:
            filePath = "kadaiPrograms/{}kai/kadaiCheckLog.csv".format(self.jugyoNo)
            with open(filePath, "a") as f:
                f.write("\n" + kadaiFileName)
                print("kadaiFileName:{}".format(kadaiFileName))            



    def executeSHFile(self, kadaiFileName: str):
        """
        checkKadaiByExecuteSHFile関数内で呼ばれる．
        実行課題ファイル名に応じて，shファイルを実行する．
        shファイル実行の際に，チェックポイントに応じて使用する関数を選ぶ．
        課題の中には，数値を元にチェックを行うものや，文字列を元にチェックするものがある．
        例：
        1. 数字をチェック
            入力: x, y
            出力: x + y
            この場合，出力値が(x+y)になっているかどうかを確認
        2. 文字列をチェック
            入力: x
            出力: xは閏年である．or xは閏年ではない．
            この場合，出力値で見るべきポイントは閏年「である」，「ではない」となる．

        args
            kadaiFileName: str,  学生の課題のファイル名（.c拡張子なし）
            例：kihon1-1-AL20024
        """


        kadaiNum = kadaiFileName[:5] + kadaiFileName[7]
        shFile = kadaiFileName+".sh"
        answerList = parseJsonAndGetAnswers(jsonPath="json/{}kai.json".format(self.jugyoNo), kadaiNum=kadaiNum)
        checkPoint = parseJsonAndGetCheckPoint(jsonPath="json/{}kai.json".format(self.jugyoNo), kadaiNum=kadaiNum)
        os.chdir("shellScripts/{}kai".format(self.jugyoNo))

        outputResult = executeKadaiAndGetOutputResult(shFile=shFile)
        studentID = getStudentID(filename=shFile)
        #print(outputResult, studentID, answerList)

        if checkPoint == "figure":
            result = checkKadai(outputResults=outputResult, studentID=studentID, answer=answerList, kadaiNum=kadaiNum)
        elif checkPoint == "string":
            result = checkKadaiString(outputResults=outputResult, studentID=studentID, answer=answerList, kadaiNum=kadaiNum)
        os.chdir("../..")
        print(os.getcwd())
        self.writeCheckedKadaiToLogFile(kadaiFileName=kadaiFileName, result=result)
        

if __name__ == "__main__":
    hoge = jugyoKadai(jugyoNo=1, kihonNum=1,hattenNum=0)
    hoge.checkKadaiByExecuteSHFile()
    
    hoge.listUncheckedKadai(kadaiFiles=hoge.searchCProgramFile())
    