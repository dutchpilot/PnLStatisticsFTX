import os
import sys
from datetime import datetime
import design
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor

class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getStatistics)
        self.pushButtonAbout.clicked.connect(self.showDialog)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.getStatistics()

    def getStatistics(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'pnl.csv')
        file_csv = open(filename, "r")
        lines = file_csv.readlines()

        headers = []

        line_cnt = 0
        ar = []
        for line in lines:
            line_cnt += 1
            if line_cnt == 1:
                headers = line.replace('"', '').replace('\n', '').split(',')
            elif line_cnt < len(lines):
                list = line.replace('"', '').replace('\n', '').split(',')

                for i in range(1, len(list)):
                    if list[i] == '':
                        list[i] = '0'
                    list[i] = float(list[i])
                list[0] = get_date(list[0])
                ar.append(list)
        file_csv.close()

        limit = '0'

        ar.sort(key=lambda x: x[2], reverse=True)
        kol = 0
        limit = float(limit)

        # ar_matrix = np.array(ar)
        #
        # ar_matrix_transpose = ar_matrix.transpose()
        #
        # ar_transp = ar_matrix_transpose.tolist()
        # print(ar_transp)
        # json_auth_filename = os.path.join(dirname, '1234.json')
        # gc = pygsheets.authorize(service_file=json_auth_filename)
        # sh = gc.open_by_url('1234')
        # wks = sh[0]
        # wks.update_value((0, 0), "1234")

        if kol == 0:
            kol = len(ar)

        totals = [0 for i in range(0, len(ar[0]))]

        excluded = []
        excluded_rows = []

        for j in range(2, len(ar[0])):
            empty = True
            for i in range(0, kol-1):
                if ar[i][j] != 0:
                    empty = False
                    totals[j] = totals[j] + ar[i][j]
            if (empty)or(abs(totals[j]) < limit):
                excluded.append(j)
        excluded.append(1)

        for i in range(0, kol - 1):
            empty = True
            for j in range(2, len(ar[0])):
                if ar[i][j] != 0:
                    empty = False
            if empty:
                excluded_rows.append(i)
        print(excluded_rows)
        top = []

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        columns = 0
        list_headers = [""]

        totals = totals[1:]
        a = ar
        for i in range(1, len(totals) - 1):
            for j in range(1, i):
                if totals[i] > totals[j]:
                    sw = totals[i]
                    totals[i] = totals[j]
                    totals[j] = sw

                    for k in range(0, len(a) - 1):
                        sw = a[k][i + 1]
                        a[k][i + 1] = a[k][j + 1]
                        a[k][j + 1] = sw

                    sw = headers[i+1]
                    headers[i+1] = headers[j+1]
                    headers[j + 1] = sw

        for i in range(2, len(headers)):
            st_item = headers[i].replace('totalOfSelected', 'Total').replace('-PERP', '')
            if not(i in excluded):
                list_headers.append(st_item + '\n' + str(float('{:.1f}'.format(float(totals[i-1])))))
                columns += 1
                self.tableWidget.setColumnCount(self.tableWidget.columnCount() + 1)

            top.append((st_item, totals[i-1]))

        self.tableWidget.setHorizontalHeaderLabels(list_headers)

        self.tableWidget.setRowCount(kol-1-len(excluded_rows))
        rows = 0
        for i in range(0, kol-1):
            if not (i in excluded_rows):
                rows += 1
                for j in range(1, len(ar[i])-1):
                    if not (j in excluded):
                        if ar[i][j] != 0:
                            self.tableWidget.setItem(rows-1, j-1, QTableWidgetItem(str(float('{:.1f}'.format(float(ar[i][j]))))))
                            if ar[i][j] > 0:
                                self.tableWidget.item(rows-1, j-1).setForeground(QBrush(QColor('green')))
                            else:
                                self.tableWidget.item(rows-1, j-1).setForeground(QBrush(QColor(255, 0, 0)))
                        else:
                            self.tableWidget.setItem(rows-1, j - 1, QTableWidgetItem(str('')))
                self.tableWidget.setItem(rows-1, 0, QTableWidgetItem(str(ar[i][0])))


        for i in range(1, self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(i)

   def showDialog(self):
        QMessageBox.about(self, "О программе","""
FTX PnL Statistics v0.1

Контакты:
t.me/s1esarev
L1FT@yandex.ru"""
                          )

def get_date(st):
    st = st[0:len(st) - 2]
    if st.isdigit():
        ts = int(st)
        ts = datetime.utcfromtimestamp(ts).strftime('%d.%m.%Y')
        return ts
    else:
        return 'Total'

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
