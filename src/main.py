import flet as ft
from pathlib import Path
from markitdown import MarkItDown
import logging
logging.basicConfig(level=logging.DEBUG)

def main(page: ft.Page):
    # テーマとスタイルの設定
    page.title = "Markdown Converter"
    page.theme_mode = "light"
    page.padding = 0
    page.bgcolor = "#f0f4f8"

    # UIコンポーネント
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    status_text = ft.Text(color="#1a73e8")
    output_path = ft.Text(color="#4a4a4a")
    progress_bar = ft.ProgressBar(width=400, color="#1a73e8", visible=False)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            progress_bar.value = 0
            progress_bar.visible = True
            status_text.value = "変換中..."
            status_text.update()
            progress_bar.update()

            total_files = len(e.files)

            md_converter = MarkItDown()

            for index, file in enumerate(e.files):
                try:
                    input_file = Path(file.path)
                    output_file = input_file.with_suffix('.md')
                    
                    
                    result = md_converter.convert(
                        input_file
                    )
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.text_content)


                    progress_bar.value = (index + 1) / total_files
                    progress_bar.update()

                    status_text.value = "変換完了! 🎉"
                    output_path.value = f"保存先: {output_file}"
                except Exception as ex:
                    status_text.value = f"エラー: {str(ex)} ❌"

                status_text.update()
                output_path.update()

    file_picker.on_result = pick_files_result

    # UIレイアウト
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "📝 Markdown Converter",
                            size=32,
                            weight="bold",
                            color="#1a73e8"
                        ),
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
                        content=progress_bar,
                        margin=ft.margin.only(bottom=10)
                    ),
                    ft.Container(
                        content=status_text,
                        margin=ft.margin.only(bottom=10)
                    ),
                    ft.Container(
                        content=output_path,
                        margin=ft.margin.only(bottom=20)
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
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
