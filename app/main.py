import sys
from pathlib import Path

def is_android():
    return "android" in sys.platform.lower() or hasattr(sys, 'getandroidapilevel')

if is_android():
    from app.ui.main_window_kivy import SmartTranslateApp
    SmartTranslateApp().run()
else:
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow
    from app.utils.platform_utils import get_app_data_dir

    def main():
        app = QApplication(sys.argv)
        app.setApplicationName("SmartTranslateAi")
        app.setApplicationVersion("1.5.3")
        
        get_app_data_dir().mkdir(parents=True, exist_ok=True)
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()