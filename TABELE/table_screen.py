import os
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFlatButton
from utils.excel_export import export_protocol_to_excel
from table_generator import TableGenerator


class TableScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generator = TableGenerator()


        self.protokol = "halas_ultradzwiekowy"
        self.section = "miejsce"

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )

        self.scroll = MDScrollView()
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)


        self.generate_table(self.protokol, self.section)

    def generate_table(self, protokol, sekcja):
        self.protokol = protokol
        self.section = sekcja
        self.layout.clear_widgets()


        table_card = self.generator.generate_table(protokol, sekcja)
        self.layout.add_widget(table_card)


        self.layout.add_widget(MDFlatButton(
            text="Eksportuj do Excela",
            on_release=self.export_to_excel,
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.4, 0.6, 0.4, 1)
        ))


        self.layout.add_widget(MDFlatButton(
            text="WSTECZ",
            on_release=self.back_to_main,
            size_hint_y=None,
            height=dp(48),
            md_bg_color=(0.6, 0.4, 0.4, 1)
        ))

    def export_to_excel(self, instance):

        data = self.generator.get_table_data(self.protokol, self.section)  # Pobierz dane z tabeli
        file_path = os.path.join(os.path.dirname(__file__), f"protokol_{self.protokol}.xlsx")


        warunki_przed = "Warunki przed testem"
        warunki_po = "Warunki po teście"
        wyposazenie = "Zestaw sprzętu"

        export_protocol_to_excel(file_path, data, warunki_przed, warunki_po, wyposazenie)
        print(f"✅ Protokół zapisano do pliku: {file_path}")

    def back_to_main(self, instance):
        self.manager.current = "main"
