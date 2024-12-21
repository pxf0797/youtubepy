import yt_dlp
import os

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
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                resolution = f.get('resolution', 'N/A')
                filesize = f.get('filesize', 0)
                filesize_str = f"{filesize/1024/1024:.1f}MB" if filesize else 'N/A'
                note = f.get('format_note', '')
                
                # 只显示带视频的格式
                if f.get('vcodec') != 'none':
                    print(f"{format_id:<8} {ext:<8} {resolution:<12} {filesize_str:<12} {note:<20}")
            
            return formats
    except Exception as e:
        print(f"获取格式列表失败: {str(e)}")
        return None

def download_video(url, output_path='downloads', format_id=None):
    """下载指定格式的视频"""
    try:
        # 创建输出目录
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 基础下载选项
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: print(f"下载进度: {d['_percent_str']}" if '_percent_str' in d else "")],
        }
        
        # 如果指定了格式ID，添加到选项中
        if format_id:
            ydl_opts['format'] = format_id
        
        # 创建下载器对象
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info = ydl.extract_info(url, download=False)
            print(f"\n视频信息：")
            print(f"标题: {info.get('title', 'N/A')}")
            print(f"时长: {info.get('duration', 'N/A')} 秒")
            print(f"观看次数: {info.get('view_count', 'N/A')}")
            
            # 确认下载
            confirm = input("\n确认下载？(y/n): ")
            if confirm.lower() != 'y':
                print("下载已取消")
                return
            
            # 开始下载
            print("\n开始下载...")
            ydl.download([url])
            
        print(f"\n下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"下载出错: {str(e)}")

def main():
    while True:
        # 获取视频URL
        url = input("\n请输入YouTube视频URL (输入q退出): ")
        if url.lower() == 'q':
            break
            
        # 列出可用格式
        formats = list_formats(url)
        if not formats:
            continue
            
        # 获取用户选择的格式
        format_id = input("\n请输入想要下载的格式ID (直接回车下载最佳质量): ")
        if not format_id:
            format_id = 'best'
            
        # 开始下载
        download_video(url, format_id=format_id)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    print("YouTube视频下载器")
    print("="*50)
    main()