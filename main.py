import os
import yaml
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from TABELE.table_generator import TableGenerator
import openpyxl

Window.size = (800, 800)

class MainScreen(Screen):
    def get_data_dict(self):
        return {
            "nazwa_zakladu": self.ids.nazwa_zakladu.text,
            "adres_zakladu": self.ids.adres_zakladu.text,
            "numer_zlecenia": self.ids.numer_zlecenia.text,
            "data_pomiarow": self.ids.data_pomiarow.text,
            "godzina_pomiarow": self.ids.godzina_pomiarow.text,
            "temperatura_before": self.ids.temperatura_before.text,
            "wilgotnosc_before": self.ids.wilgotnosc_before.text,
            "cisnienie_before": self.ids.cisnienie_before.text,
            "temperatura_after": self.ids.temperatura_after.text,
            "wilgotnosc_after": self.ids.wilgotnosc_after.text,
            "cisnienie_after": self.ids.cisnienie_after.text
        }

    def set_data_from_dict(self, data):
        self.ids.nazwa_zakladu.text = data.get("nazwa_zakladu", "")
        self.ids.adres_zakladu.text = data.get("adres_zakladu", "")
        self.ids.numer_zlecenia.text = data.get("numer_zlecenia", "")
        self.ids.data_pomiarow.text = data.get("data_pomiarow", "")
        self.ids.godzina_pomiarow.text = data.get("godzina_pomiarow", "")
        self.ids.temperatura_before.text = data.get("temperatura_before", "")
        self.ids.wilgotnosc_before.text = data.get("wilgotnosc_before", "")
        self.ids.cisnienie_before.text = data.get("cisnienie_before", "")
        self.ids.temperatura_after.text = data.get("temperatura_after", "")
        self.ids.wilgotnosc_after.text = data.get("wilgotnosc_after", "")
        self.ids.cisnienie_after.text = data.get("cisnienie_after", "")

    def submit_data(self):
        data = self.get_data_dict()
        file_path = os.path.join(os.path.dirname(__file__), "dane.yaml")
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
        print("✅ Dane zostały zapisane do 'dane.yaml'.")

    def load_previous_data(self):
        file_path = os.path.join(os.path.dirname(__file__), "dane.yaml")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.set_data_from_dict(data)
                print("📥 Dane zostały wczytane z 'dane.yaml'.")
        else:
            print("⚠️ Nie znaleziono pliku z danymi.")

    def save_to_excel(self):
        data = [
            [self.ids.nazwa_zakladu.text, self.ids.adres_zakladu.text, self.ids.numer_zlecenia.text,
             self.ids.data_pomiarow.text, self.ids.godzina_pomiarow.text],
        ]
        warunki_przed = self.ids.temperatura_before.text
        warunki_po = self.ids.temperatura_after.text
        wyposazenie = "Wyposażenie 1, Wyposażenie 2"

        file_path = os.path.join(os.path.dirname(__file__), "protokol_pomiarowy.xlsx")
        export_protocol_to_excel(file_path, data, warunki_przed, warunki_po, wyposazenie)
        print(f"✅ Protokół zapisano do pliku: {file_path}")

    def add_stanowisko(self):
        protokol = "halas_ultradzwiekowy"
        sekcja = "drgania_ogolne"
        table = self.table_generator.generate_table(protokol, sekcja)
        self.ids.tabelka.add_widget(table)

    def add_protokol(self):
        protokol = "chemia"
        sekcja = "drgania_miejscowe"
        table = self.table_generator.generate_table(protokol, sekcja)
        self.ids.tabelka.add_widget(table)

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        Builder.load_file("GUI_look/interface.kv")

        self.sm = WindowManager()
        self.main_screen = MainScreen(name="main")
        self.sm.add_widget(self.main_screen)
        self.main_screen.table_generator = TableGenerator()
        return self.sm

    def set_protocol(self, text_item):
        self.main_screen.ids.protokol.text = text_item
        self.menu.dismiss()

    def get_selected_protocol(self):
        return self.main_screen.ids.protokol.text

    def on_start(self):
        Clock.schedule_once(self.create_menu, 1)

    def create_menu(self, dt):
        menu_items = [
            {"text": "Hałas", "on_release": lambda x="Hałas": self.set_protocol(x)},
            {"text": "Hałas ultradźwiękowy", "on_release": lambda x="Hałas ultradźwiękowy": self.set_protocol(x)},
            {"text": "Drgania mechaniczne", "on_release": lambda x="Drgania mechaniczne": self.set_protocol(x)},
            {"text": "Próbki powietrza", "on_release": lambda x="Próbki powietrza": self.set_protocol(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.main_screen.ids.protokol,
            items=menu_items,
            width_mult=4,
        )

    def open_menu(self):
        if self.menu:
            self.menu.open()

if __name__ == "__main__":
    MainApp().run()
