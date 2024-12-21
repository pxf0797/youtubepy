import yt_dlp
import os

def download_video(url, output_path='downloads'):
    try:
        # 创建输出目录
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 配置下载选项
        ydl_opts = {
            'format': 'best',  # 下载最好的质量
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # 输出模板
            'progress_hooks': [lambda d: print(f"下载进度: {d['_percent_str']}" if '_percent_str' in d else "")],
        }
        
        # 创建下载器对象并下载
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info = ydl.extract_info(url, download=False)
            print(f"标题: {info.get('title', 'N/A')}")
            print(f"时长: {info.get('duration', 'N/A')} 秒")
            print(f"观看次数: {info.get('view_count', 'N/A')}")
            
            # 开始下载
            print("开始下载...")
            ydl.download([url])
            
        print(f"下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"下载出错: {str(e)}")

if __name__ == "__main__":
    video_url = "https://youtube.com/watch?v=6JXB4BErigQ"  # 您的视频URL
    download_video(video_url)