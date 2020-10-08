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
    
    def searchCProgramFile(self, parameter_list):
        """
        ディレクトリ内を探索し，まだチェックしてない課題(cファイル)をリストとして返す

        return
        kadaiSHFiles: List[str]
        実行する課題のファイル名が格納されているリスト
        """
        pass

    def executeSHFile(self, kadaiFileName: str):
        """
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
        kadaiFileName，例：kihon1-1-AL20024
        """


        kadaiNum = kadaiFileName[:5] + kadaiFileName[7]
        shFile = kadaiFileName+".sh"
        answerList = parseJsonAndGetAnswers(jsonPath="json/1kai.json", kadaiNum=kadaiNum)
        checkPoint = parseJsonAndGetCheckPoint(jsonPath="json/1kai.json", kadaiNum=kadaiNum)
        os.chdir("scriptAndprogram/")

        outputResult = executeKadaiAndGetOutputResult(shFile=shFile)
        studentID = getStudentID(filename=shFile)
        #print(outputResult, studentID, answerList)

        if checkPoint == "figure":
            checkKadai(outputResults=outputResult, studentID=studentID, answer=answerList, kadaiNum=kadaiNum)
        elif checkPoint == "string":
            checkKadaiString(outputResults=outputResult, studentID=studentID, answer=answerList, kadaiNum=kadaiNum)
        os.chdir("..")


if __name__ == "__main__":
    hoge = jugyoKadai(jugyoNo=1, kihonNum=1,hattenNum=0)
    hoge.checkKadaiByExecuteSHFile()