from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

import asyncio
import os
from pathlib import Path

# Core imports (reuse)
from app.core.translator import Translator
from app.providers.openrouter_provider import OpenRouterProvider
from app.services.translation_service import TranslationService
from app.services.settings_service import SettingsService
from app.services.file_service import FileService
from app.models.translation_model import TranslationRequest, ContentType
from app.utils.platform_utils import get_app_data_dir

class SmartTranslateApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.title = "SmartTranslateAi - Android"

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = Label(text='SmartTranslateAi\nEnterprise Edition', 
                      size_hint_y=0.08, font_size='18sp', bold=True)

        # Input
        self.input_text = TextInput(multiline=True, hint_text='متن زیرنویس یا محتوای فایل را اینجا paste کنید...', size_hint_y=0.3)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        self.open_file_btn = Button(text='Open File')
        self.open_folder_btn = Button(text='Batch Folder')
        self.translate_btn = Button(text='Start Translation', background_color=(0.2, 0.6, 0.2, 1))
        self.stop_btn = Button(text='Stop', background_color=(0.8, 0.2, 0.2, 1))

        btn_layout.add_widget(self.open_file_btn)
        btn_layout.add_widget(self.open_folder_btn)
        btn_layout.add_widget(self.translate_btn)
        btn_layout.add_widget(self.stop_btn)

        # Progress
        self.progress = ProgressBar(max=100, size_hint_y=0.05)
        self.status_label = Label(text='آماده', size_hint_y=0.05)

        # Output
        output_label = Label(text='خروجی ترجمه:', size_hint_y=0.05)
        self.output_text = TextInput(multiline=True, readonly=True, size_hint_y=0.25)

        # Logs
        logs_label = Label(text='Logs:', size_hint_y=0.05)
        self.logs_scroll = ScrollView(size_hint_y=0.2)
        self.logs_text = TextInput(multiline=True, readonly=True, background_color=(0.05, 0.05, 0.05, 1))

        self.logs_scroll.add_widget(self.logs_text)

        # Add all to layout
        main_layout.add_widget(header)
        main_layout.add_widget(self.input_text)
        main_layout.add_widget(btn_layout)
        main_layout.add_widget(self.progress)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(output_label)
        main_layout.add_widget(self.output_text)
        main_layout.add_widget(logs_label)
        main_layout.add_widget(self.logs_scroll)

        # Bind buttons
        self.translate_btn.bind(on_press=self.start_translation)
        self.stop_btn.bind(on_press=self.stop_translation)
        self.open_file_btn.bind(on_press=self.open_file)
        self.open_folder_btn.bind(on_press=self.open_folder)

        # Initialize core
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()
        self.provider = OpenRouterProvider(self.settings)
        self.translator = Translator(self.provider)
        self.translation_service = TranslationService(self.translator)

        self.batch_mode = False
        self.batch_files = []
        self.is_translating = False

        return main_layout

    def log(self, message):
        self.logs_text.text += f"{message}\n"
        self.logs_text.cursor = (0, len(self.logs_text.text))

    def start_translation(self, instance):
        if self.is_translating:
            return

        text = self.input_text.text.strip()
        if not text:
            self.show_popup("خطا", "متن خالی است!")
            return

        self.is_translating = True
        self.translate_btn.disabled = True
        self.stop_btn.disabled = False
        self.progress.value = 0

        Clock.schedule_once(lambda dt: self._run_translation(text), 0.1)

    async def _run_translation(self, text):
        try:
            request = TranslationRequest(text=text)
            result = await self.translation_service.translate(request, self.progress_callback)
            if result.success:
                self.output_text.text = result.translated_text
                self.log("✅ ترجمه با موفقیت انجام شد")
            else:
                self.log(f"❌ خطا: {result.error}")
        except Exception as e:
            self.log(f"❌ خطای غیرمنتظره: {str(e)}")
        finally:
            self.is_translating = False
            self.translate_btn.disabled = False
            self.stop_btn.disabled = True

    def progress_callback(self, text: str, value: int = None):
        if text:
            self.log(text)
            self.status_label.text = text
        if value is not None:
            self.progress.value = value

    def stop_translation(self, instance):
        self.log("🛑 ترجمه متوقف شد")
        self.is_translating = False
        self.translate_btn.disabled = False
        self.stop_btn.disabled = True

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    # Open File & Folder (Android version)
    def open_file(self, instance):
        self.log("انتخاب فایل در اندروید هنوز کامل پیاده‌سازی نشده (نیاز به plyer)")
        self.show_popup("اطلاع", "انتخاب فایل در اندروید نیاز به کتابخانه plyer دارد")

    def open_folder(self, instance):
        self.log("انتخاب پوشه در اندروید هنوز کامل پیاده‌سازی نشده")
        self.show_popup("اطلاع", "Batch Mode در اندروید در حال توسعه است")

# Run the app
if __name__ == '__main__':
    SmartTranslateApp().run()