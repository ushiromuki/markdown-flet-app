import flet as ft
import asyncio
from application.conversion_service import ConversionService

def main(page: ft.Page):
    page.title = "Markdown Converter"
    page.theme_mode = "light"
    page.padding = 0
    page.bgcolor = "#f0f4f8"

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    status_container = ft.Column([], scroll=ft.ScrollMode.AUTO)
    total_progress = ft.ProgressBar(width=400, color="#1a73e8", visible=False)
    total_status = ft.Text(color="#1a73e8")

    conversion_service = ConversionService()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            asyncio.run(conversion_service.process_files(e.files, status_container, total_progress, total_status))

    file_picker.on_result = pick_files_result

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("📝 Markdown Converter", size=32, weight="bold", color="#1a73e8"),
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.UPLOAD_FILE),
                                ft.Text("ファイルを選択", size=16),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor="#1a73e8",
                            shadow_color="#0d47a1",
                            elevation=5,
                        ),
                        on_click=lambda _: file_picker.pick_files(
                            allow_multiple=True,
                            file_type=ft.FilePickerFileType.ANY
                        )
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Container(
                    content=total_progress,
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Container(
                    content=total_status,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Container(
                    content=status_container,
                    height=300,
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=5,
                    padding=10,
                ),
            ]),
            padding=40,
            margin=ft.margin.all(20),
            border_radius=10,
            bgcolor="white",
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, "black"),
            )
        )
    )

ft.app(target=main)