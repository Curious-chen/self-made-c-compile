from PyQt5.QtCore import Qt, QVariant, QRect, QDir, QFile, QFileInfo, QTextStream, QRegExp, QSettings, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QFont
import sys, os


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.setFont(QFont("黑体", 9))
        self.fname = ""
        self.filename = ""


    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    # def fileSave(self):
    #     print("filename: "+self.filename)
    #     if (self.filename != ""):
    #         file = QFile(self.filename+'.txt')
    #         if not file.open(QFile.WriteOnly | QFile.Text):
    #             QMessageBox.warning(self, "Error",
    #                                 "Cannot write file %s:\n%s." % (self.filename, file.errorString()))
    #             return
    #
    #         outstr = QTextStream(file)
    #         QApplication.setOverrideCursor(Qt.WaitCursor)
    #         outstr << self.toPlainText()
    #         # QApplication.restoreOverrideCursor()
    #         # self.setModified(False)
    #         # self.fname = QFileInfo(self.filename).fileName()
    #         # self.setWindowTitle(self.fname + "[*]")
    #         # self.setCurrentFile(self.filename)
    #     else:
    #         self.fileSaveAs()
    #         ### save File
    #
    # def fileSaveAs(self):
    #     fn, _ = QFileDialog.getSaveFileName(self, "Save as...", self.filename, ".txt")
    #     if not fn:
    #         print("Error saving")
    #         return False
    #
    #     lfn = fn.lower()
    #
    #     self.filename = fn
    #     self.fname = os.path.splitext(str(fn))[0].split("/")[-1]
    #     return self.fileSave()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeEditor = QCodeEditor()
    codeEditor.show()
    sys.exit(app.exec_())
