"""GUI_interface.py"""

import os
import yaml
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


yaml_path = os.path.join(os.path.dirname(__file__), "GUI.yaml")
with open(yaml_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


class MainScreen(MDScreen):
    def on_kv_post(self, base_widget):
        self.fields_map = {field.get("key"): MDTextField(hint_text=field.get("label", ""), mode="line", size_hint_y=None, height=dp(48)) for field in config.get("gui", {}).get("fields", [])}
        self.generate_fields()

    def generate_fields(self):
        container = self.ids.dane_podstawowe_box
        container.clear_widgets()

        for field in config.get("gui", {}).get("fields", []):
            container.add_widget(MDLabel(text=field.get("label", ""), theme_text_color="Primary", bold=True, size_hint_y=None, height=dp(24)))
            container.add_widget(self.fields_map[field.get("key")])

        warunki_box = self.ids.warunki_box
        warunki_box.clear_widgets()

        for warunek in config.get("gui", {}).get("warunki_srodowiskowe", []):
            wrapper = MDBoxLayout(orientation="vertical", size_hint=(1, 1))
            wrapper.add_widget(MDLabel(text=warunek.get("label", ""), theme_text_color="Primary", bold=True, size_hint_y=None, height=dp(24)))
            wrapper.add_widget(MDTextField(mode="line", size_hint_y=None, height=dp(48)))
            warunki_box.add_widget(wrapper)

    def submit_data(self):
        for key, widget in self.fields_map.items():
            print(f"{key}: {widget.text}")

    def copy_last_data(self):
        MDApp.get_running_app().last_data = {key: widget.text for key, widget in self.fields_map.items()}


class TableScreen(MDScreen):
    def generate_table(self, data, header):
        table_layout = MDBoxLayout(orientation="vertical")
        header_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=48)
        header_row.add_widget(MDLabel(text=header, halign="center", valign="middle", theme_text_color="Custom", text_color=(0.2, 0.4, 0.2, 1)))
        table_layout.add_widget(header_row)

        for item in data:
            row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=48)
            row.add_widget(MDLabel(text=item, halign="center", valign="middle", theme_text_color="Custom", text_color=(0.2, 0.4, 0.2, 1)))
            table_layout.add_widget(row)

        self.clear_widgets()
        self.add_widget(table_layout)


class ProtocolApp(MDApp):
    def build(self):
        self.title = "System Protokołów TES"
        kv_path = os.path.join(os.path.dirname(__file__), "Interface.kv")
        Builder.load_file(kv_path)
        self.screen = MainScreen()
        self.last_data = {}

        menu_items = [
            {"text": protokol.get("text", ""), "on_release": lambda x=protokol["text"]: self.set_protokol(x)}
            for protokol in config.get("gui", {}).get("protokoly", [])
        ]

        self.menu = MDDropdownMenu(caller=None, items=menu_items, width_mult=4)
        return self.screen

    def on_start(self):
        self.menu.caller = self.screen.ids.get("protokol", None)

    def set_protokol(self, value):
        self.screen.ids["protokol"].text = value
        self.menu.dismiss()

    def get_selected_protocol(self):
        return self.screen.ids.get("protokol", None).text
