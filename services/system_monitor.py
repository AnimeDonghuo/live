import psutil
import shutil
import platform
import asyncio
import os

class SystemMonitor:
    @staticmethod
    def get_system_stats():
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = shutil.disk_usage("/")
        
        return {
            "os": f"{platform.system()} {platform.release()}",
            "cpu_model": platform.processor(),
            "cpu_usage": f"{cpu_usage}%",
            "ram_usage": f"{ram.percent}% ({ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB)",
            "disk_usage": f"{(disk.used/disk.total)*100:.1f}% ({disk.free // (1024**3)}GB Free)",
            "python": platform.python_version()
        }

    @staticmethod
    async def run_preflight_checks():
        errors = []
        # Check FFmpeg
        if not shutil.which("ffmpeg"): errors.append("FFmpeg Missing")
        if not shutil.which("ffprobe"): errors.append("FFprobe Missing")
        
        # Check Write Perms
        if not os.access(".", os.W_OK): errors.append("Current directory not writable")
        
        # Check Mongo (simple ping)
        from database.mongo import db
        try:
            await db.client.admin.command('ping')
        except:
            errors.append("MongoDB Connection Failed")

        return errors
