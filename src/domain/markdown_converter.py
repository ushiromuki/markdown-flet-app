from markitdown import MarkItDown

class MarkdownConverter:
    def convert(self, file_path):
        md_converter = MarkItDown()
        return md_converter.convert(file_path)