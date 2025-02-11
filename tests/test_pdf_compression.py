import pytest
from pathlib import Path
import flet as ft
import os
from application.pdf_compression_service import PDFCompressionService
from unittest.mock import MagicMock, patch
import pikepdf
from PIL import Image
import io

@pytest.fixture
def mock_pdf_file():
    # テスト用のPDFファイル情報をモック
    mock_file = MagicMock()
    mock_file.path = "test.pdf"
    return mock_file

@pytest.fixture
def compression_service():
    return PDFCompressionService()

@pytest.fixture
def ui_components():
    # UI要素のモック作成
    status = ft.Text()
    progress = ft.ProgressBar()
    return status, progress

async def test_pdf_compression_initialization(compression_service, mock_pdf_file, ui_components):
    """PDF圧縮の初期化テスト"""
    status, progress = ui_components
    
    with patch('pikepdf.open') as mock_open:
        mock_pdf = MagicMock()
        mock_pdf.pages = []
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        await compression_service.compress_pdf(mock_pdf_file, status, progress)
        
        assert progress.visible == True
        assert status.value.startswith("PDFを圧縮中")

async def test_pdf_compression_with_images(compression_service, mock_pdf_file, ui_components):
    """画像を含むPDFの圧縮テスト"""
    status, progress = ui_components
    
    with patch('pikepdf.open') as mock_open, \
         patch('PIL.Image.open') as mock_image_open, \
         patch('os.path.getsize') as mock_getsize:
        
        # PDFのモックを設定
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_xobj = MagicMock()
        
        # 画像オブジェクトの設定
        mock_xobj.get.side_effect = lambda x: '/Image' if x == '/Subtype' else None
        mock_xobj.read_raw_bytes.return_value = b'dummy_image_data'
        
        # ページリソースの設定
        mock_page.Resources = MagicMock()
        mock_page.Resources.XObject = {'image1': mock_xobj}
        mock_pdf.pages = [mock_page]
        
        mock_open.return_value.__enter__.return_value = mock_pdf
        
        # PILイメージのモック
        mock_image = MagicMock()
        mock_image.mode = 'RGB'
        mock_image.save = MagicMock()
        mock_image_open.return_value = mock_image
        
        # ファイルサイズのモック
        mock_getsize.side_effect = lambda x: 1000 if 'compressed' in x else 2000
        
        await compression_service.compress_pdf(mock_pdf_file, status, progress)
        
        assert progress.value == 1
        assert "圧縮完了" in status.value
        assert "50.0%" in status.value  # 圧縮率の確認

async def test_pdf_compression_error_handling(compression_service, mock_pdf_file, ui_components):
    """エラーハンドリングのテスト"""
    status, progress = ui_components
    
    with patch('pikepdf.open', side_effect=Exception("テストエラー")):
        await compression_service.compress_pdf(mock_pdf_file, status, progress)
        
        assert "エラーが発生しました" in status.value 