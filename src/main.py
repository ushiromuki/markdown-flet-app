import flet as ft
import asyncio
from application.conversion_service import ConversionService
from application.pdf_compression_service import PDFCompressionService

def main(page: ft.Page):
    page.title = "Markdown & PDF Converter"
    page.theme_mode = "light"
    page.padding = 0
    page.bgcolor = "#f0f4f8"

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    status_container = ft.Column([], scroll=ft.ScrollMode.AUTO)
    total_progress = ft.ProgressBar(width=400, color="#1a73e8", visible=False)
    total_status = ft.Text(color="#1a73e8")

    conversion_service = ConversionService()

    pdf_file_picker = ft.FilePicker()
    page.overlay.append(pdf_file_picker)
    
    pdf_status = ft.Text(color="#1a73e8")
    pdf_progress = ft.ProgressBar(width=400, color="#1a73e8", visible=False)
    
    compression_value_text = ft.Text(
        value="75%",
        size=16,
        color="#4caf50",
        weight="bold"
    )

    def on_slider_change(e):
        compression_value_text.value = f"{int(pdf_compression_ratio.value)}%"
        compression_value_text.update()

    pdf_compression_ratio = ft.Slider(
        min=0,
        max=100,
        value=75,
        label="圧縮率",
        width=300,
        active_color="#4caf50",
        inactive_color="#a5d6a7",
        on_change=on_slider_change
    )

    pdf_compression_service = PDFCompressionService()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            asyncio.run(conversion_service.process_files(e.files, status_container, total_progress, total_status))

    file_picker.on_result = pick_files_result

    def pick_pdf_result(e: ft.FilePickerResultEvent):
        if e.files:
            asyncio.run(pdf_compression_service.compress_pdf(
                e.files[0], 
                pdf_status, 
                pdf_progress,
                compression_ratio=pdf_compression_ratio.value
            ))

    pdf_file_picker.on_result = pick_pdf_result

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("📝 Markdown & PDF Converter", size=32, weight="bold", color="#1a73e8"),
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.UPLOAD_FILE),
                                ft.Text("Markdownファイルを選択", size=16),
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
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PICTURE_AS_PDF),
                                ft.Text("PDFファイルを圧縮", size=16),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor="#4caf50",
                            shadow_color="#2e7d32",
                            elevation=5,
                        ),
                        on_click=lambda _: pdf_file_picker.pick_files(
                            allow_multiple=False,
                            allowed_extensions=["pdf"]
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
                    content=pdf_progress,
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Container(
                    content=pdf_status,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("PDF圧縮設定", size=16, color="#4a4a4a"),
                        ft.Row(
                            controls=[
                                pdf_compression_ratio,
                                compression_value_text
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]),
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