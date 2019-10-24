from PyQt5 import QtCore, QtGui, QtWidgets
import re

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

class Tokenizer:
    def tokenize(self, text):
        regex = re.compile(r'([^a-zA-Z0-9 \n\t\r])')
        text = regex.sub(r' \1 ', text)
        return text.split()

class Detector:
    tokenizer = Tokenizer()
    listSinonim = {}
    ngram_match = 0
    def __init__(self,sinonim_path,suspect_text,source_text, n=3):
        self.sinonim_path = sinonim_path
        self.susText = suspect_text
        self.souText = source_text
        self.n = n

    def init_sinonim(self):
        try:
            with open(self.sinonim_path, 'r', encoding='utf-8-sig') as fp:
                for row in fp.readlines():
                    rowSinonim = tuple(row.rstrip().lower().split("=="))
                    valSinonim = rowSinonim[0]
                    for sinonim in rowSinonim:
                        self.listSinonim[sinonim] = valSinonim
        except IOError:
            pass

    def ngramize(self,subset):
        return tuple([self.listSinonim.get(i, i) for i in subset])

    def tokenize(self, text):
        token = self.tokenizer.tokenize(text.lower())
        temp = []
        for i in range(len(token) - self.n +1):
            temp.append(self.ngramize(token[i:i+self.n]))
        return temp

    def detect(self):
        if(self.sinonim_path):
            self.init_sinonim()
        source_ngram=suspect_ngram={}
        self.n+=1
        while(len(source_ngram) is 0 or len(suspect_ngram) is 0):
            self.n -=1
            source_ngram = self.tokenize(self.souText)
            suspect_ngram = self.tokenize(self.susText)
        for data in suspect_ngram:
            if data in source_ngram:
                self.ngram_match += 1
        return self.ngram_match / len(suspect_ngram) * 100

class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(666, 550)
        main.setWindowIcon(iconFromBase64(ico))
        self.labelSuspect = QtWidgets.QLabel(main)
        self.labelSuspect.setGeometry(QtCore.QRect(15, 10, 111, 23))
        self.labelSuspect.setObjectName("labelSuspect")
        self.labelSource = QtWidgets.QLabel(main)
        self.labelSource.setGeometry(QtCore.QRect(345, 10, 111, 23))
        self.labelSource.setObjectName("labelSource")
        self.accuracyBar = QtWidgets.QProgressBar(main)
        self.accuracyBar.setGeometry(QtCore.QRect(10, 420, 641, 23))
        self.accuracyBar.setProperty("value", 0)
        self.accuracyBar.setObjectName("accuracyBar")
        self.startButton = QtWidgets.QPushButton(main)
        self.startButton.setGeometry(QtCore.QRect(540, 500, 100, 30))
        self.startButton.setObjectName("startButton")
        self.suspectedText = QtWidgets.QPlainTextEdit(main)
        self.suspectedText.setGeometry(QtCore.QRect(10, 40, 320, 371))
        self.suspectedText.setObjectName("Suspected")
        self.sourceText = QtWidgets.QPlainTextEdit(main)
        self.sourceText.setGeometry(QtCore.QRect(340, 40, 320, 371))
        self.sourceText.setObjectName("Source")
        self.suspectPath = QtWidgets.QLineEdit(main)
        self.suspectPath.setGeometry(QtCore.QRect(10,460,400,30))
        self.suspectPath.setObjectName("suspectPath")
        self.suspectPath.setReadOnly(True)
        self.suspectButton = QtWidgets.QPushButton(main)
        self.suspectButton.setGeometry(QtCore.QRect(420,460,100,30))
        self.suspectButton.setObjectName("suspectButton")
        self.sourcePath = QtWidgets.QLineEdit(main)
        self.sourcePath.setGeometry(QtCore.QRect(10,500,400,30))
        self.sourcePath.setObjectName("sourcePath")
        self.sourcePath.setReadOnly(True)
        self.sourceButton = QtWidgets.QPushButton(main)
        self.sourceButton.setGeometry(QtCore.QRect(420,500,100,30))
        self.sourceButton.setObjectName("sourceButton")
        self.n = QtWidgets.QComboBox(main)
        self.n.setGeometry(QtCore.QRect(540, 460, 100, 30))
        self.n.addItems(['Auto','1','2','3','4','5'])

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

        self.startButton.clicked.connect(self.startngram)
        self.suspectButton.clicked.connect(lambda:self.selectFile(1))
        self.sourceButton.clicked.connect(lambda:self.selectFile(2))

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Plagiarism Checker"))
        self.labelSuspect.setText(_translate("main", "Suspected Document"))
        self.labelSource.setText(_translate("main", "Source Document"))
        self.startButton.setText(_translate("main", "Start"))
        self.suspectButton.setText(_translate("main", "Suspect"))
        self.sourceButton.setText(_translate("main", "Source"))

    def startngram(self):
        if(self.suspectedText.toPlainText() is not '' and self.sourceText.toPlainText() is not ''):
            finalScore =0
            self.accuracyBar.reset()
            if(self.n.currentIndex()==0):
                for i in range(1,6):
                    program = Detector("synbank.txt", self.suspectedText.toPlainText(), self.sourceText.toPlainText(), i)
                    finalScore+=program.detect()
                finalScore/=5
            else:
                program = Detector("synbank.txt", self.suspectedText.toPlainText(), self.sourceText.toPlainText(), self.n.currentIndex())
                finalScore = program.detect()
            self.accuracyBar.setValue(finalScore)
        else:
            self.accuracyBar.setValue(0)

    def selectFile(self, flag):
        if(flag==1):
            name,type = QtWidgets.QFileDialog.getOpenFileName(filter = "Text files (*.txt)")
            if(name is not ''):
                self.suspectedText.clear()
                with open(name, 'r', encoding='utf-8-sig') as fp:
                    text=fp.read()
                self.suspectPath.setText(name)
                self.suspectedText.insertPlainText(text)
        elif(flag==2):
            names,type = QtWidgets.QFileDialog.getOpenFileNames(filter = "Text files (*.txt)")
            text =''
            for name in names:
                if(name is not ''):
                    with open(name, 'r', encoding='utf-8-sig') as fp:
                        text+="\n" + fp.read()
            if(text != ''):
                self.sourceText.clear()
                self.sourcePath.setText(name)
                self.sourceText.insertPlainText(text)

ico=b"iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAM9SURBVHhe7d2xbSVVGIZhQxekVLEpIT0sNVALARVAD4Sk28ImpETUAFgaCcn6ZQ2au/POnPs8kuWJrVdH99MZ2199+Panv18g8vX2HRICJCVAUgIkJUBSAiQlQFICJCVAUk93E/Lpjx+3p96/P/vt6Xk5AUkJkJQASQmQ1NIjZBocn37/c3t6jA/ffbM9/eeX73/dnt73w28ft6f3rTxWnICkBEhKgKQESGqZEbL3huNKI2QyDRMjBL4QAZISICkBkrrlCDnjhmOvR4+Qyco3Jk5AUgIkJUBSAiR1qRFS3WYcMY2QyaOHyeSOtyhOQFICJCVAUgIkdfkRMn14nz5sP9swWeV2xAlISoCkBEhKgKSyEbJ3cEz2fgC/4zB5NCME3iFAUgIkJUBStxwhk6vfjlSm8XOlYeIEJCVAUgIkJUBSAiQlQFICJCVAUgIkdcpNyBm3HhM3IbMr3Y44AUkJkJQASQmQ1OVHiMHxeEYIbARISoCkBEgqGyFHGByzI7/8boTwlARISoCkBEjq4SNkGhxGw+PtHRxHbpzOGCZOQFICJCVAUgIkJcCFvA6Ot19XJ0BSAiQlQFICJCVAUgIkJUBSAiQlQFKHXsfy6lVneh3r0TcfP3/+a3v6cpyApARISoCkBEhq6REyfVBfZSSdMULO+D0RJyApAZISICkBklpmhBz5y1B7XX1gTY4MEyOE5QmQlABJCZDULUfIkcGx90P5Hf8/yRlDzAhhKQIkJUBSAiS1zAg54y9BPds/Tpx+zkYISxEgKQGSEiApAf4Pr0Pn7RfHCJCUAEkJkJQASS0T4Ostxdsvrs8JSEqApARISoCkDr2ONVn5Fa29w+aOr2Od8erVxAlISoCkBEhKgKSWHiF7TWPF4DiHE5CUAEkJkJQAST18hExW+VO+dxwcEyMENgIkJUBSAiR1ygiZTMNkssoH/8mRQXRENTgmTkBSAiQlQFICJJWNkL2udItyxN7Bsff3WPa+LnalwTFxApISICkBkhIgqcuPkMkdb1GmEXJkcFx9XOzlBCQlQFICJCVAUrccIXvtHStXt8rgmDgBSQmQlABJCZDU0iOE63MCkhIgKQGSEiChl5d/AG2mJMp4S80KAAAAAElFTkSuQmCC"

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QDialog()
    ui = Ui_main()
    ui.setupUi(main)
    main.show()
    sys.exit(app.exec_())
