import yt_dlp
import os
import socket

def download_video(url, output_path='downloads', format_id=None):
    """下载指定格式的视频，带重试和错误处理"""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 增强的下载选项
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: print(f"下载进度: {d['_percent_str']}" if '_percent_str' in d else "")],
            # 添加重试和超时设置
            'retries': 10,  # 重试次数
            'fragment_retries': 10,  # 分片下载重试次数
            'socket_timeout': 30,  # 超时设置
            'nocheckcertificate': True,  # 忽略SSL证书验证
            # 添加网络设置
            'buffersize': 1024 * 1024,  # 缓冲区大小
            'http_chunk_size': 10485760,  # 分块大小（10MB）
        }
        
        if format_id:
            ydl_opts['format'] = format_id

        # 设置更长的超时时间
        socket.setdefaulttimeout(30)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"\n视频信息：")
            print(f"标题: {info.get('title', 'N/A')}")
            print(f"时长: {info.get('duration', 'N/A')} 秒")
            print(f"大小: {info.get('filesize_approx', 0)/1024/1024:.1f} MB")
            
            confirm = input("\n确认下载？(y/n): ")
            if confirm.lower() != 'y':
                print("下载已取消")
                return
            
            print("\n开始下载... (如果下载中断将自动重试)")
            ydl.download([url])
            
        print(f"\n下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"\n下载出错: {str(e)}")
        retry = input("是否要重试下载？(y/n): ")
        if retry.lower() == 'y':
            print("\n重新尝试下载...")
            download_video(url, output_path, format_id)

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