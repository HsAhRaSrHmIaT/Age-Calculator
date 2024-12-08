from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, \
    QLineEdit, QCalendarWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter

import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        main_layout = QVBoxLayout()

        name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        dob_label = QLabel("Date of Birth:")
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("dd/mm/yyyy")

        self.dob_input_choose = QCalendarWidget()
        self.dob_input_choose.setGridVisible(True)
        self.dob_input_choose.selectionChanged.connect(self.update_dob_input)
        self.dob_input_choose.hide()

        calendar_button = QPushButton()
        svg_data = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" fill="#ffffff" stroke="#000000" stroke-width="2"/>
              <line x1="3" y1="10" x2="21" y2="10" stroke="#000000" stroke-width="2"/>
              <line x1="7" y1="4" x2="7" y2="2" stroke="#000000" stroke-width="2"/>
              <line x1="17" y1="4" x2="17" y2="2" stroke="#000000" stroke-width="2"/>
              <circle cx="7" cy="14" r="1.5" fill="#000000"/>
              <circle cx="12" cy="14" r="1.5" fill="#000000"/>
              <circle cx="17" cy="14" r="1.5" fill="#000000"/>
              <circle cx="7" cy="18" r="1.5" fill="#000000"/>
              <circle cx="12" cy="18" r="1.5" fill="#000000"/>
              <circle cx="17" cy="18" r="1.5" fill="#000000"/>
            </svg>
        """
        svg_renderer = QSvgRenderer(QByteArray(svg_data.encode('utf-8')))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        icon = QIcon(pixmap)
        calendar_button.setIcon(icon)
        calendar_button.clicked.connect(self.show_calendar)

        dob_layout = QHBoxLayout()
        dob_layout.addWidget(self.dob_input)
        dob_layout.addWidget(calendar_button)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_age)

        result_label = QLabel("Result will be displayed here")

        output_label = QLabel()
        output_label.setObjectName("output_label")
        output_label.hide()

        output_label_days = QLabel()
        output_label_days.setObjectName("output_label_days")
        output_label_days.hide()

        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(dob_label)
        main_layout.addLayout(dob_layout)
        main_layout.addWidget(self.dob_input_choose)
        main_layout.addWidget(calculate_button)
        main_layout.addWidget(result_label)
        main_layout.addWidget(output_label)
        main_layout.addWidget(output_label_days)

        self.setLayout(main_layout)

    def show_calendar(self):
        if self.dob_input_choose.isHidden():
            self.dob_input_choose.show()
        else:
            self.dob_input_choose.hide()
        self.adjustSize()

    def update_dob_input(self):
        dob = self.dob_input_choose.selectedDate().toString("dd/MM/yyyy")
        self.dob_input.setText(dob)
        self.dob_input_choose.hide()
        self.adjustSize()

    def calculate_age(self):
        if not self.dob_input.text():
            output_label = self.findChild(QLabel, "output_label")
            output_label_days = self.findChild(QLabel, "output_label_days")
            output_label.show()
            output_label_days.hide()
            output_label.setText("Please enter your date of birth")
            return
        try:
            dob = self.dob_input.text()
            dob = datetime.strptime(dob, "%d/%m/%Y")
            age = abs(datetime.now() - dob)
            output_label = self.findChild(QLabel, "output_label")
            output_label.setText(f"Your age is: {age.days // 365}")

            output_label_days = self.findChild(QLabel, "output_label_days")
            output_label_days.setText(f"Your age in days is: {age.days}")
        except ValueError:
            output_label = self.findChild(QLabel, "output_label")
            output_label_days = self.findChild(QLabel, "output_label_days")
            output_label.show()
            output_label_days.hide()
            output_label.setText("Please enter a valid date of birth")
            self.dob_input.clear()
            return

        self.dob_input.clear()
        self.name_input.clear()
        output_label.show()
        output_label_days.show()


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
