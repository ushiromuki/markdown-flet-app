import flet as ft

class FileConversionStatus:
    def __init__(self, filename: str):
        self.filename = filename
        self.progress = ft.ProgressBar(width=300, color="#1a73e8", value=0)
        self.status = ft.Text(color="#1a73e8", size=14)
        self.container = ft.Container(
            content=ft.Column([
                ft.Text(filename, size=14, color="#4a4a4a"),
                self.progress,
                self.status
            ]),
            margin=ft.margin.only(bottom=10)
        )