import asyncio
from pathlib import Path
from domain.markdown_converter import MarkdownConverter
from infrastructure.file_repository import FileRepository

class ConversionService:
    def __init__(self):
        self.converter = MarkdownConverter()
        self.repository = FileRepository()

    async def convert_file(self, file_path: Path, status):
        try:
            result = self.converter.convert(file_path)
            output_file = file_path.with_suffix('.md')
            await self.repository.write_content(output_file, result.text_content)
            status.progress.value = 1.0
            status.status.value = "完了 ✅"
        except Exception as ex:
            status.status.value = f"エラー: {str(ex)} ❌"
        finally:
            status.progress.update()
            status.status.update()

    async def process_files(self, files, status_container, total_progress, total_status):
        total_progress.visible = True
        total_progress.value = 0
        total_status.value = "変換中..."
        status_container.controls.clear()

        file_statuses = []
        # Presentation層に定義したFileConversionStatusをインポートして利用
        from presentation.conversion_status import FileConversionStatus
        for file in files:
            status = FileConversionStatus(Path(file.path).name)
            file_statuses.append(status)
            status_container.controls.append(status.container)

        status_container.update()
        total_progress.update()
        total_status.update()

        tasks = [
            self.convert_file(Path(file.path), status)
            for file, status in zip(files, file_statuses)
        ]

        for i, task in enumerate(asyncio.as_completed(tasks)):
            await task
            total_progress.value = (i + 1) / len(tasks)
            total_progress.update()

        total_status.value = "すべての変換が完了しました 🎉"
        total_status.update()