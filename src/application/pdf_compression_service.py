import flet as ft
import os
import asyncio
import pikepdf
from PIL import Image
import io
import logging

# ログの設定 - デバッグレベルで詳細なログを出力
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFCompressionService:
    """PDFファイルの圧縮を行うサービスクラス
    
    主な機能：
    - PDFファイル内の画像を検出し圧縮
    - 進捗状況のリアルタイム表示
    - 圧縮率の計算と結果表示
    """
    
    async def compress_pdf(self, file_info, status: ft.Text, progress: ft.ProgressBar, compression_ratio: float = 75.0):
        """PDFファイルを圧縮する非同期メソッド
        
        Args:
            file_info: 入力PDFファイルの情報
            status: 状態表示用のTextコンポーネント
            progress: 進捗表示用のProgressBarコンポーネント
            compression_ratio: 圧縮率（0-100）、デフォルト75%
        """
        try:
            # UI初期化
            progress.visible = True
            status.value = "PDFを圧縮中..."
            progress.value = 0
            progress.update()
            status.update()

            # 入出力パスの設定
            input_path = file_info.path
            output_path = os.path.join(
                os.path.dirname(input_path),
                f"compressed_{os.path.basename(input_path)}"
            )

            # ログ出力
            logger.info(f"入力ファイル: {input_path}")
            logger.info(f"出力ファイル: {output_path}")
            logger.info(f"圧縮率設定: {compression_ratio}%")

            # 画像品質の設定（圧縮率から計算）
            quality = max(5, 100 - compression_ratio)
            logger.info(f"画像品質設定: {quality}")

            # PDFファイルを開いて処理
            with pikepdf.open(input_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"総ページ数: {total_pages}")

                # 各ページを処理
                for i, page in enumerate(pdf.pages):
                    logger.info(f"ページ {i+1}/{total_pages} を処理中")
                    
                    # ページ内の画像を検索して処理
                    if hasattr(page, 'Resources') and '/XObject' in page.Resources:
                        for name, xobj in page.Resources.XObject.items():
                            try:
                                # 画像オブジェクトの場合のみ処理
                                if xobj.get('/Subtype') == '/Image':
                                    logger.info(f"画像を検出: {name}")
                                    # すでにJPEG圧縮されている場合はスキップ
                                    if xobj.get('/Filter') == '/DCTDecode':
                                        logger.info(f"既存のJPEG画像をスキップ: {name}")
                                        continue
                                    
                                    try:
                                        # 画像データの取得と処理
                                        image_data = xobj.read_raw_bytes()
                                        img = Image.open(io.BytesIO(image_data))
                                        logger.info(f"画像サイズ: {img.size}, モード: {img.mode}")
                                        
                                        # RGB形式に変換（必要な場合）
                                        if img.mode != 'RGB':
                                            img = img.convert('RGB')
                                        
                                        # 画像の圧縮
                                        output = io.BytesIO()
                                        img.save(output, format='JPEG', quality=int(quality), optimize=True)
                                        xobj.write(output.getvalue(), filter_=pikepdf.Name('/DCTDecode'))
                                        logger.info(f"画像を圧縮: {name}")
                                    except Exception as e:
                                        logger.warning(f"画像処理をスキップ: {str(e)}")
                                        continue
                            except Exception as e:
                                logger.warning(f"XObjectの処理をスキップ: {str(e)}")
                                continue

                    # 進捗状況の更新
                    progress.value = (i + 1) / total_pages
                    progress.update()
                    await asyncio.sleep(0.01)

                # 圧縮したPDFを保存
                logger.info("PDFを保存中...")
                pdf.save(
                    output_path,
                    compress_streams=True,
                    object_stream_mode=pikepdf.ObjectStreamMode.generate,
                    recompress_flate=True
                )
                logger.info("PDF保存完了")

            # ファイルサイズのフォーマット用関数
            def format_size(size):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f}{unit}"
                    size /= 1024.0
                return f"{size:.1f}GB"

            # 圧縮結果の計算
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            actual_ratio = (1 - compressed_size / original_size) * 100

            # 結果のログ出力
            logger.info(f"圧縮結果 - 元サイズ: {format_size(original_size)}, "
                       f"圧縮後: {format_size(compressed_size)}, "
                       f"圧縮率: {actual_ratio:.1f}%")

            # UI更新
            status.value = (
                f"圧縮完了！\n"
                f"元のサイズ: {format_size(original_size)}\n"
                f"圧縮後のサイズ: {format_size(compressed_size)}\n"
                f"圧縮率: {actual_ratio:.1f}%\n"
                f"保存先: {output_path}"
            )
            progress.value = 1
            
        except Exception as e:
            # エラー処理
            logger.error(f"エラーが発生: {str(e)}", exc_info=True)
            status.value = f"エラーが発生しました: {str(e)}"
        finally:
            # UI更新の確実な実行
            status.update()
            progress.update() 