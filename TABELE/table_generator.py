import os
import yaml
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


class TableGenerator:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        yaml_path = os.path.join(current_dir, "tabele.yaml")
        with open(yaml_path, encoding="utf-8") as f:
            self.yaml_data = yaml.safe_load(f)

        print(f"Załadowane dane z YAML: {self.yaml_data}")

        self.colors = {
            "halas_ultradzwiekowy": {
                "bg": (0.95, 0.9, 1, 1),
                "header": (0.8, 0.6, 0.9, 1),
                "label": (0.9, 0.2, 0.6, 1),
            },
            # Dodaj resztę kolorów...
        }

    def generate_table(self, protokol, sekcja):
        tabele = self.yaml_data.get("tabele", {})

        print(f"Protokol: {protokol}")
        print(f"Sekcja: {sekcja}")

        wspolne_pola = tabele.get("wspolne_pola_dla_sekcji", {}).get(protokol, {}).get(sekcja, [])
        tabela = tabele.get(protokol, {}).get(sekcja, {}).get("kolumny", [])

        print(f"Wspólne pola: {wspolne_pola}")
        print(f"Tabela: {tabela}")

        if not wspolne_pola or not tabela:
            print("Brak danych do wygenerowania tabeli!")
            return None

        main_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=self.calculate_height(wspolne_pola, tabela),
            md_bg_color=self.colors[protokol]["bg"],
            radius=[dp(15)]
        )

        for field in wspolne_pola:
            row_box = MDBoxLayout(
                orientation="vertical",
                spacing=dp(5),
                size_hint_y=None,
                height=dp(80)
            )

            row_box.add_widget(MDLabel(
                text=field,
                theme_text_color="Custom",
                text_color=self.colors[protokol]["label"]
            ))

            text_field = MDTextField(
                hint_text=f"Podaj: {field}",
                mode="filled",
                size_hint_y=None,
                height=dp(48)
            )

            row_box.add_widget(text_field)
            main_card.add_widget(row_box)

        if tabela:
            header_box = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(40)
            )
            for header in tabela:
                header_box.add_widget(MDLabel(
                    text=header,
                    halign="center",
                    theme_text_color="Custom",
                    text_color=self.colors[protokol]["header"]
                ))
            main_card.add_widget(header_box)

        return main_card

    def calculate_height(self, wspolne_pola, tabela):
        return dp(100 + len(wspolne_pola) * 90 + (60 if tabela else 0))
