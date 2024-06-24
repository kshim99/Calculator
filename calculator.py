import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scientific Calculator')
        self.setGeometry(300, 300, 400, 500)
        self.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
        """)

        layout = QVBoxLayout()
        
        # Display
        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            background-color: #34495e;
            color: white;
            border: none;
            font-size: 24px;
            padding: 5px;
        """)
        layout.addWidget(self.display)

        # Buttons
        grid = QGridLayout()
        buttons = [
            'sin', 'cos', 'tan', 'exp', '(',
            'asin', 'acos', 'atan', 'log', ')',
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'pow',
            '1', '2', '3', '-', 'pi',
            '0', '.', 'C', '+', '=',
        ]

        positions = [(i, j) for i in range(6) for j in range(5)]

        for position, button in zip(positions, buttons):
            btn = QPushButton(button)
            btn.setFixedSize(70, 70)
            btn.setFont(QFont('Arial', 12))
            btn.clicked.connect(self.on_click)
            if button in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'sqrt', 'pow', 'exp', 'pi']:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #16a085;
                        border: none;
                        color: white;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #1abc9c;
                    }
                """)
            elif button in ['/', '*', '-', '+', '=', '(', ')']:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e67e22;
                        border: none;
                        color: white;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #d35400;
                    }
                """)
            elif button == 'C':
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        border: none;
                        color: white;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #c0392b;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        border: none;
                        color: white;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #2980b9;
                    }
                """)
            grid.addWidget(btn, *position)

        layout.addLayout(grid)
        self.setLayout(layout)

    def on_click(self):
        sender = self.sender()
        current = self.display.text()
        button_text = sender.text()

        if button_text == '=':
            self.calculate()
        elif button_text == 'C':
            self.display.clear()
        elif button_text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'sqrt', 'exp']:
            self.display.setText(current + button_text + '(')
        elif button_text == 'pow':
            self.display.setText(current + '^')
        elif button_text == 'pi':
            self.display.setText(current + 'pi')
        else:
            self.display.setText(current + button_text)

    def calculate(self):
        try:
            expression = self.display.text()
            url = f"http://api.mathjs.org/v4/?expr={expression}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.text
                self.display.setText(result)
            else:
                self.display.setText("Error")
        except:
            self.display.setText("Error")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())