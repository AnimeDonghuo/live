import asyncio
import subprocess
import json
import logging
import time
import psutil
from bot.config import Config

logger = logging.getLogger("streamer")

class StreamManager:
    def __init__(self):
        self.process = None
        self.current_video = None
        self.current_rtmp = None
        self.start_time = None

    async def get_video_info(self, file_path):
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', '-show_format', file_path
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        return json.loads(stdout)

    def is_compatible(self, info):
        v_codec = next((s for s in info['streams'] if s['codec_type'] == 'video'), {}).get('codec_name')
        a_codec = next((s for s in info['streams'] if s['codec_type'] == 'audio'), {}).get('codec_name')
        return v_codec == 'h264' and a_codec == 'aac'

    async def start_stream(self, video_path, rtmp_url):
        if self.process:
            await self.stop_stream()

        info = await self.get_video_info(video_path)
        use_copy = self.is_compatible(info)
        
        # Build FFmpeg Command
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1',
            '-i', video_path
        ]

        if use_copy:
            cmd += ['-c', 'copy']
        else:
            # Re-encode for low-spec VPS (720p libx264)
            cmd += [
                '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '2500k',
                '-maxrate', '2500k', '-bufsize', '5000k', '-pix_fmt', 'yuv420p',
                '-g', '50', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                '-vf', 'scale=1280:720'
            ]

        cmd += ['-f', 'flv', rtmp_url]

        logger.info(f"Starting FFmpeg: {' '.join(cmd)}")
        
        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True
            )
            self.current_video = video_path
            self.current_rtmp = rtmp_url
            self.start_time = time.time()
            return True
        except Exception as e:
            logger.error(f"FFmpeg start error: {e}")
            return False

    async def stop_stream(self):
        if self.process:
            try:
                # Kill process tree
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
            except:
                pass
            self.process = None
            self.current_video = None
            self.start_time = None
            return True
        return False

    def get_status(self):
        if not self.process or self.process.poll() is not None:
            return None
        
        try:
            p = psutil.Process(self.process.pid)
            return {
                "pid": self.process.pid,
                "uptime": time.time() - self.start_time,
                "cpu": p.cpu_percent(interval=0.1),
                "mem": p.memory_percent(),
                "video": self.current_video,
                "rtmp": self.current_rtmp
            }
        except:
            return None

stream_manager = StreamManager()
