from pynput import mouse
import mss
import mss.tools
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2 Point")

        container = QWidget()
        self.setCentralWidget(container)

        label = QLabel("2 Point")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

app = QApplication()

app.setStyle("Fusion")
dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(54, 57, 62))
app.setPalette(dark_palette)

window = MainWindow()
window.show()
app.exec()



#Getting Points
points = []
def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        points.append((x,y))
        print(f"its here @ {(x,y)}")
        if len(points) == 2:
            return False # Stop listener
    return None

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

#Store Points
(x1, y1), (x2,y2) = points

left = min(x1, x2)
top = min(y1, y2)
width = abs(x2 - x1)
height = abs(y2 - y1)

#Screen Capture
with mss.mss() as sct:
    # The screen part to capture
    if width == 0 or height == 0:
        print("Invalid Region: Width or Height Is 0.")
    else:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        output = f"sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)