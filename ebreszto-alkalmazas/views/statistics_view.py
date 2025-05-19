from PySide6.QtWidgets import QLabel, QPushButton, QButtonGroup
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageQt
import io

class StatisticsView:
    def __init__(self, statisticsPage_widget):
        self.statisticsPage = statisticsPage_widget

        # Buttons
        self.week_button: QPushButton = self.statisticsPage.findChild(QPushButton, "weekButton")
        self.month_button: QPushButton = self.statisticsPage.findChild(QPushButton, "monthButton")
        self.year_button: QPushButton = self.statisticsPage.findChild(QPushButton, "yearButton")

        # Set buttons as checkable
        for btn in [self.week_button, self.month_button, self.year_button]:
            btn.setCheckable(True)

        # Create button group to enforce mutual exclusivity
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.week_button)
        self.button_group.addButton(self.month_button)
        self.button_group.addButton(self.year_button)

        # Labels
        self.sleep_label: QLabel = self.statisticsPage.findChild(QLabel, "sleepStatisticsQlabel")
        self.water_label: QLabel = self.statisticsPage.findChild(QLabel, "waterStatisticsQlabel")
        self.avg_sleep_label: QLabel = self.statisticsPage.findChild(QLabel, "averageSleepLabel")
        self.avg_water_label: QLabel = self.statisticsPage.findChild(QLabel, "averageWaterLabel")

    def connect_controller(self, controller):
        self.week_button.clicked.connect(lambda: controller.on_range_selected("Week"))
        self.month_button.clicked.connect(lambda: controller.on_range_selected("Month"))
        self.year_button.clicked.connect(lambda: controller.on_range_selected("Year"))

    def update_chart(self, sleep_data, water_data, avg_sleep, avg_water):
        def create_chart(data, avg, title, ylabel, color):
            fig = Figure(figsize=(4, 2.5))
            canvas = FigureCanvasAgg(fig)
            ax = fig.add_subplot(111)
            x = list(range(len(data)))
            ax.plot(x, data, marker='o', color=color, label=ylabel)
            ax.axhline(avg, linestyle='--', color='gray', label=f'Average ({avg})')
            ax.set_title(title)
            ax.set_xlabel("Period")
            ax.set_ylabel(ylabel)
            ax.legend()
            fig.tight_layout()
            buf = io.BytesIO()
            canvas.print_png(buf)
            buf.seek(0)
            img = Image.open(buf)
            return QPixmap.fromImage(ImageQt.ImageQt(img))

        self.sleep_label.setPixmap(create_chart(sleep_data, avg_sleep, "Sleep Statistics", "Hours", "blue"))
        self.sleep_label.setAlignment(Qt.AlignCenter)

        self.water_label.setPixmap(create_chart(water_data, avg_water, "Water Intake", "Liters", "green"))
        self.water_label.setAlignment(Qt.AlignCenter)

        self.avg_sleep_label.setText(f"{avg_sleep} h")
        self.avg_water_label.setText(f"{avg_water} L")
