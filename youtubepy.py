import yt_dlp
import os
import socket
from pathlib import Path

def download_video(url, output_path='downloads', format_id=None):
    """下载指定格式的视频，支持断点续传"""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 增强的下载选项
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: print(f"下载进度: {d['_percent_str']}" if '_percent_str' in d else "")],
            # 断点续传设置
            'continuedl': True,  # 启用断点续传
            'retries': 10,
            'fragment_retries': 10,
            'socket_timeout': 30,
            'nocheckcertificate': True,
            # 网络优化设置
            'buffersize': 1024 * 1024,
            'http_chunk_size': 10485760,
        }
        
        if format_id:
            ydl_opts['format'] = format_id

        # 设置超时时间
        socket.setdefaulttimeout(30)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 先获取视频信息
            try:
                info = ydl.extract_info(url, download=False)
                print(f"\n视频信息：")
                print(f"标题: {info.get('title', 'N/A')}")
                print(f"时长: {info.get('duration', 'N/A')} 秒")
                print(f"预计大小: {info.get('filesize_approx', 0)/1024/1024:.1f} MB")
                
                # 检查是否存在部分下载的文件
                filename = ydl.prepare_filename(info)
                partial_file = Path(filename + '.part')
                temp_file = Path(filename + '.temp')
                
                if partial_file.exists() or temp_file.exists():
                    resume = input("\n检测到未完成的下载，是否继续上次的下载？(y/n): ")
                    if resume.lower() != 'y':
                        # 删除部分下载的文件
                        if partial_file.exists():
                            partial_file.unlink()
                        if temp_file.exists():
                            temp_file.unlink()
                        print("已删除未完成的下载文件，将重新开始下载")
                else:
                    confirm = input("\n确认开始新下载？(y/n): ")
                    if confirm.lower() != 'y':
                        print("下载已取消")
                        return
                
                # 开始下载
                print("\n开始下载...")
                ydl.download([url])
                
            except yt_dlp.utils.DownloadError as e:
                print(f"\n下载中断: {str(e)}")
                retry = input("是否继续尝试下载？(y/n): ")
                if retry.lower() == 'y':
                    print("\n继续下载...")
                    download_video(url, output_path, format_id)
                return
            
        print(f"\n下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"\n发生错误: {str(e)}")

def list_formats(url):
    """列出所有可用的视频格式"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True  # 忽略SSL证书验证
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
                if f.get('vcodec') != 'none':  # 只显示带视频的格式
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
    print("YouTube视频下载器 (增强版)")
    print("="*50)
    main()