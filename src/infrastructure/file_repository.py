import aiofiles

class FileRepository:
    async def write_content(self, file_path, content):
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)