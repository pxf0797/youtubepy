import yt_dlp
import os
from pathlib import Path

def download_video(url, output_path='downloads', format_id=None):
    """下载指定格式的视频，支持断点续传和分片下载"""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 优化的下载选项
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: print(f"下载进度: {d['_percent_str']}" if '_percent_str' in d else "")],
            # 断点续传和重试设置
            'continuedl': True,
            'retries': 3,
            'fragment_retries': 3,
            'retry_sleep': 3,
            # 优化的网络参数
            'http_chunk_size': 1048576,  # 1MB分块
            'file_access_retries': 3,
            # 使用aria2作为外部下载器来提高稳定性
            'external_downloader': 'aria2c',
            'external_downloader_args': [
                '--max-connection-per-server=5',  # 每个服务器的最大连接数
                '--min-split-size=1M',           # 最小分片大小
                '--split=5',                     # 单个文件分成5片下载
                '--max-concurrent-downloads=5',   # 最大并发下载数
                '--retry-wait=3',                # 重试等待时间
                '--timeout=10',                  # 连接超时时间
                '--connect-timeout=10',          # 建立连接超时时间
                '--auto-file-renaming=false'     # 禁止自动重命名
            ]
        }
        
        if format_id:
            ydl_opts['format'] = format_id

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # 获取视频信息
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                partial_file = Path(filename + '.part')
                
                # 显示当前下载进度
                if partial_file.exists():
                    downloaded_size = partial_file.stat().st_size
                    total_size = info.get('filesize', 0)
                    if total_size > 0:
                        progress = (downloaded_size/total_size)*100
                        print(f"\n已下载: {downloaded_size/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB")
                        print(f"完成度: {progress:.1f}%")
                
                print("\n继续下载...")
                ydl.download([url])
                
            except yt_dlp.utils.DownloadError as e:
                print(f"\n下载中断: {str(e)}")
                print("\n请选择操作：")
                print("1. 继续尝试当前下载")
                print("2. 选择较低质量继续下载")
                print("3. 保存已下载部分并退出")
                
                choice = input("请输入选项 (1-3): ")
                
                if choice == '1':
                    return download_video(url, output_path, format_id)
                elif choice == '2':
                    new_format = input("请输入新的格式ID (较低质量): ")
                    return download_video(url, output_path, new_format)
                else:
                    print("已保存当前进度，您可以稍后继续下载")
                    return
                
        print(f"\n下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"\n发生错误: {str(e)}")

def list_formats(url):
    """列出所有可用的视频格式"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            print("\n可用的视频格式：")
            print("=" * 80)
            print(f"{'格式ID':<8} {'扩展名':<8} {'分辨率':<12} {'文件大小':<12} {'注释':<20}")
            print("-" * 80)
            
            for f in formats:
                if f.get('vcodec') != 'none':
                    format_id = f.get('format_id', 'N/A')
                    ext = f.get('ext', 'N/A')
                    resolution = f.get('resolution', 'N/A')
                    filesize = f.get('filesize', 0)
                    filesize_str = f"{filesize/1024/1024:.1f}MB" if filesize else 'N/A'
                    note = f.get('format_note', '')
                    
                    print(f"{format_id:<8} {ext:<8} {resolution:<12} {filesize_str:<12} {note:<20}")
            
            return formats
    except Exception as e:
        print(f"获取格式列表失败: {str(e)}")
        return None

def main():
    print("YouTube视频下载器 (优化版)")
    print("="*50)
    
    while True:
        url = input("\n请输入YouTube视频URL (输入q退出): ")
        if url.lower() == 'q':
            break
            
        formats = list_formats(url)
        if not formats:
            continue
            
        format_id = input("\n请输入想要下载的格式ID (直接回车下载最佳质量): ")
        if not format_id:
            format_id = 'best'
            
        download_video(url, format_id=format_id)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()