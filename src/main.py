import flet as ft
from pathlib import Path
from markitdown import MarkItDown
import asyncio
import aiofiles

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

    async def convert_file(file_path: Path, status: FileConversionStatus):
        try:
            md_converter = MarkItDown()
            result = md_converter.convert(file_path)
            output_file = file_path.with_suffix('.md')
            
            async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
                await f.write(result.text_content)
            
            status.progress.value = 1.0
            status.status.value = "完了 ✅"
        except Exception as ex:
            status.status.value = f"エラー: {str(ex)} ❌"
        finally:
            status.progress.update()
            status.status.update()

    async def process_files(files):
        total_progress.visible = True
        total_progress.value = 0
        total_status.value = "変換中..."
        status_container.controls.clear()
        
        file_statuses = []
        for file in files:
            status = FileConversionStatus(Path(file.path).name)
            file_statuses.append(status)
            status_container.controls.append(status.container)
        
        status_container.update()
        total_progress.update()
        total_status.update()

        tasks = [
            convert_file(Path(file.path), status) 
            for file, status in zip(files, file_statuses)
        ]
        
        for i, task in enumerate(asyncio.as_completed(tasks)):
            await task
            total_progress.value = (i + 1) / len(tasks)
            total_progress.update()

        total_status.value = "すべての変換が完了しました 🎉"
        total_status.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            asyncio.run(process_files(e.files))

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