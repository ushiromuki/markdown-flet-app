import pytest
from unittest.mock import MagicMock, patch
import flet as ft
from src.main import main

@pytest.fixture
def mock_page():
    page = MagicMock(spec=ft.Page)
    page.title = ""
    page.theme_mode = ""
    page.padding = 0
    page.bgcolor = ""
    page.overlay = []
    return page

@pytest.fixture
def mock_file_picker():
    return MagicMock(spec=ft.FilePicker)

def test_main_initialization(mock_page):
    """メイン画面の初期化テスト"""
    main(mock_page)
    
    assert mock_page.title == "Markdown Converter"
    assert mock_page.theme_mode == "light"
    assert mock_page.padding == 0
    assert mock_page.bgcolor == "#f0f4f8"
    assert len(mock_page.overlay) == 1

def test_pick_files_result_with_no_files(mock_page):
    """ファイル未選択時のテスト"""
    main(mock_page)
    file_picker = mock_page.overlay[0]
    
    # ファイル未選択イベントをシミュレート
    mock_event = MagicMock()
    mock_event.files = []
    file_picker.on_result(mock_event)
    
    # UIコンポーネントの状態を検証
    container = mock_page.add.call_args[0][0]
    column = container.content
    
    progress_bar = column.controls[2].content
    status_text = column.controls[3].content
    output_path = column.controls[4].content
    
    assert not progress_bar.visible
    assert not status_text.value
    assert not output_path.value

@patch('src.main.MarkItDown')
def test_pick_files_result_with_multiple_files(mock_markitdown, mock_page):
    """複数ファイル処理のテスト"""
    main(mock_page)
    file_picker = mock_page.overlay[0]
    
    # 複数ファイル選択をシミュレート
    mock_event = MagicMock()
    mock_files = [
        MagicMock(path="test1.txt"),
        MagicMock(path="test2.txt")
    ]
    mock_event.files = mock_files
    
    # MarkItDownのモック設定
    mock_converter = mock_markitdown.return_value
    mock_converter.convert.return_value.text_content = "Converted Content"
    
    with patch('builtins.open', MagicMock()):
        file_picker.on_result(mock_event)
    
    # 期待される呼び出し回数を検証
    assert mock_converter.convert.call_count == 2