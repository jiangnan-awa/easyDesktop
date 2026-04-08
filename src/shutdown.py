import win32api
import win32con
import time

class ShutdownHandler:
    """处理Windows关机信号的类"""
    def __init__(self, window):
        self.window = window
        self.shutdown_occurred = False
        # 注册关机回调
        self._register_handler()
    
    def _register_handler(self):
        """注册控制台控制处理器"""
        # 设置回调函数，返回True表示消息已被处理
        win32api.SetConsoleCtrlHandler(self._console_handler, True)
    
    def _console_handler(self, ctrl_type):
        if ctrl_type == win32con.CTRL_SHUTDOWN_EVENT:
            print("检测到系统关机信号，正在清理资源...")
            self._cleanup_and_exit()
            return True  # 表示消息已被处理
        elif ctrl_type == win32con.CTRL_CLOSE_EVENT:
            print("检测到控制台关闭信号，正在清理资源...")
            self._cleanup_and_exit()
            return True
        elif ctrl_type in (win32con.CTRL_LOGOFF_EVENT,):
            print("检测到用户注销信号，正在清理资源...")
            self._cleanup_and_exit()
            return True
        return False  # 未处理，交给系统默认处理
    
    def _cleanup_and_exit(self):
        """执行清理工作并退出"""
        if self.shutdown_occurred:
            return  # 避免重复执行
        
        self.shutdown_occurred = True
        if self.window:
            try:
                self.window.destroy()
            except Exception as e:
                print(f"关闭窗口时出错: {e}")
        
        # 这里可以添加其他清理工作，如保存配置、关闭文件等
        # 注意：关机时系统可能只给你几秒的时间，所以清理工作要快
        
        # 给系统一点时间处理清理操作
        time.sleep(0.5)
        
        # 退出程序
        import os
        os._exit(0)  # 强制退出，因为系统正在关机