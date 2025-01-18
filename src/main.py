import flet as ft
from pathlib import Path
import markitdown as md


def main(page: ft.Page):
    page.title = "Markdown Converter"
    page.theme_mode = "light"

    # UIコンポーネント
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    status_text = ft.Text()
    output_path = ft.Text()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            status_text.value = "変換中..."
            status_text.update()

            for file in e.files:
                try:
                    # 入力ファイルのパス
                    input_file = Path(file.path)
                    # 出力ファイルのパス
                    output_file = input_file.with_suffix('.md')

                    # markitdownを使用してマークダウンに変換
                    md.convert(
                        input_file,
                        output_file,
                        format_type="markdown"
                    )

                    status_text.value = "変換完了!"
                    output_path.value = f"保存先: {output_file}"
                except Exception as ex:
                    status_text.value = f"エラー: {str(ex)}"

                status_text.update()
                output_path.update()

    file_picker.on_result = pick_files_result

    # UIレイアウト
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("ドキュメントをMarkdownに変換", size=24, weight="bold"),
                    ft.ElevatedButton(
                        "ファイルを選択",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(
                            allow_multiple=True,
                            file_type=ft.FilePickerFileType.ANY
                        )
                    ),
                    status_text,
                    output_path,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
    )


ft.app(target=main)
