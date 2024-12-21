from pytube import YouTube
import os

def download_video(url, output_path='downloads'):
    try:
        # 创建输出目录（如果不存在）
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        # 创建YouTube对象
        yt = YouTube(url)
        
        # 获取视频信息
        print(f"标题: {yt.title}")
        print(f"时长: {yt.length} 秒")
        print(f"评分: {yt.rating}")
        print(f"观看次数: {yt.views}")
        
        # 获取最高质量的视频流
        video = yt.streams.get_highest_resolution()
        
        # 开始下载
        print("正在下载...")
        video.download(output_path)
        
        print(f"下载完成！视频保存在: {output_path}")
        
    except Exception as e:
        print(f"下载出错: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 替换为你想下载的YouTube视频URL
    video_url = "https://youtu.be/6JXB4BErigQ"
    download_video(video_url)