import os
import sys
from datetime import datetime
import design
import about
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor

class Window2(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window")

class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getStatistics)
        self.pushButtonAbout.clicked.connect(self.showDialog)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.dateEditTo.setDate(datetime.now())
        self.dateEditFrom.setDate(datetime(datetime.now().year,1,1))
        # self.calendarWidgetTo.setSelectedDate(datetime.now())
        # self.calendarWidgetFrom.setSelectedDate(datetime(datetime.now().year,1,1))
        self.getStatistics()


    def window2(self):
        self.w = Window2()
        self.w.show()


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
            for i in range(0, kol):
                if ar[i][j] != 0:
                    empty = False
                    totals[j] = totals[j] + ar[i][j]

        excluded.append(1)

        for i in range(0, kol):
            empty = True
            for j in range(2, len(ar[0])):
                if ar[i][j] != 0:
                    empty = False

            d = datetime.strptime(ar[i][0], '%d.%m.%Y').date()
            d = datetime(d.year, d.month, d.day)
            dFrom = datetime(self.dateEditFrom.date().year(), self.dateEditFrom.date().month(), self.dateEditFrom.date().day())
            dTo = datetime(self.dateEditTo.date().year(), self.dateEditTo.date().month(), self.dateEditTo.date().day())
            # dFrom = datetime(self.calendarWidgetFrom.selectedDate().year(), self.calendarWidgetFrom.selectedDate().month(), self.calendarWidgetFrom.selectedDate().day())
            # dTo = datetime(self.calendarWidgetTo.selectedDate().year(), self.calendarWidgetTo.selectedDate().month(), self.calendarWidgetTo.selectedDate().day())
            if empty:
                excluded_rows.append(i)
            elif (d < dFrom) or (d > dTo):
                excluded_rows.append(i)
        top = []

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        columns = 0
        #

        totals = totals[1:]
        for i in range(0, len(totals)):
            for j in range(1, i):
                if totals[i] > totals[j]:
                    sw = totals[i]
                    totals[i] = totals[j]
                    totals[j] = sw

                    for k in range(0, len(ar)):
                        sw = ar[k][i + 1]
                        ar[k][i + 1] = ar[k][j + 1]
                        ar[k][j + 1] = sw

                    sw = headers[i+1]
                    headers[i+1] = headers[j+1]
                    headers[j + 1] = sw


        self.tableWidget.setRowCount(kol-len(excluded_rows))

        totals = []

        list_headers = []
        for j in range(2, len(ar[i])):
            if not (j in excluded):
                sum = 0
                for i in range(0, kol):
                    if not (i in excluded_rows):
                        if ar[i][j] != 0:
                            sum = sum + float(ar[i][j])
                if sum != 0:
                    st_item = headers[j].replace('totalOfSelected', 'Total').replace('-PERP', '')
                    list_headers.append(st_item + '\n' + str(float('{:.1f}'.format(float(sum)))))
                    totals.append(sum)
                    self.tableWidget.setColumnCount(self.tableWidget.columnCount() + 1)
                else:
                    excluded.append(j)
        self.tableWidget.setHorizontalHeaderLabels(list_headers)

        rows = 0

        for i in range(0, kol):
            if not (i in excluded_rows):
                rows += 1
                cols = 0
                for j in range(1, len(ar[i])):
                    if not (j in excluded):
                        cols += 1
                        if ar[i][j] != 0:
                            self.tableWidget.setItem(rows-1, cols, QTableWidgetItem('{:.1f}'.format(float(ar[i][j]))))
                        else:
                            self.tableWidget.setItem(rows-1, cols, QTableWidgetItem(str('')))

                    self.tableWidget.setItem(rows-1, 0, QTableWidgetItem(str(ar[i][0])))

        for i in range(1, len(totals)):
            for j in range(1, i):
                if totals[i] > totals[j]:
                    sw = totals[i]
                    totals[i] = totals[j]
                    totals[j] = sw

                    sw = list_headers[i]
                    list_headers[i] = list_headers[j]
                    list_headers[j] = sw

                    for k in range(0, self.tableWidget.rowCount()):
                        if self.tableWidget.item(k,i+1) == None:
                            sw =  QTableWidgetItem('')
                        else:
                            sw =  QTableWidgetItem(self.tableWidget.item(k,i+1).text())

                        if self.tableWidget.item(k,j+1) == None:
                            obj =  QTableWidgetItem('')
                        else:
                            obj =  QTableWidgetItem(self.tableWidget.item(k,j+1).text())

                        self.tableWidget.setItem(k,i+1,obj)
                        self.tableWidget.setItem(k,j+1,sw)

        list_vertical_headers = []

        for i in range(1, self.tableWidget.rowCount()):
            for j in range(1, self.tableWidget.columnCount()):
                if self.tableWidget.item(i,j) != None:
                    if self.tableWidget.item(i,j).text() == '':
                        cell = 0
                    else:
                        cell = float(self.tableWidget.item(i,j).text())
                    if cell < 0:
                        self.tableWidget.item(i, j).setForeground(QBrush(QColor(255, 0, 0)))

        for i in range(0, self.tableWidget.rowCount()):
            d = datetime.strptime(str(self.tableWidget.item(i,0).text()), '%d.%m.%Y').date().strftime('%a')
            d = d.replace('Mon', 'Пн')
            d = d.replace('Tue', 'Вт')
            d = d.replace('Wed', 'Ср')
            d = d.replace('Thu', 'Чт')
            d = d.replace('Fri', 'Пт')
            d = d.replace('Sat', 'Сб')
            d = d.replace('Sun', 'Вс')
            list_vertical_headers.append(str(i+1) + ') '+ str(self.tableWidget.item(i,0).text()))

        self.tableWidget.setVerticalHeaderLabels(list_vertical_headers)

        self.tableWidget.removeColumn(0)

        self.tableWidget.setHorizontalHeaderLabels(list_headers)

        for i in range(0, self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(i)

    def showDialog(self):
        QMessageBox.about(self, "О программе","""
FTX PnL Statistics v0.2

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
