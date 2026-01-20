from pynput import keyboard
from pynput.keyboard import Key
from collections import defaultdict
import time

class KeyboardMonitor:
    def __init__(self):
        """初始化键盘监听器"""
        self.pressed_keys = defaultdict(bool)
        
        # 预定义映射表 - 只包含我们允许的键
        self.allowed_keys = self._create_key_mapping()
        
        # 启动监听器
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            suppress=False
        )
        self.listener.daemon = True
        self.listener.start()
    
    def _create_key_mapping(self):
        """创建完整的键映射表，只包含允许的键"""
        mapping = {}
        
        # 1. 字母键 (a-z)
        for char in 'abcdefghijklmnopqrstuvwxyz':
            # 这些字符将在get_pressed_keys中根据shift状态处理大小写
            mapping[char] = char.lower()
        
        # 2. 数字键 (0-9)
        for char in '0123456789':
            mapping[char] = char
        
        # 3. 符号键 (需要处理shift状态)
        symbols = {
            '`': '`', '~': '~',
            '-': '-', '_': '_',
            '=': '=', '+': '+',
            '[': '[', '{': '{',
            ']': ']', '}': '}',
            '\\': '\\', '|': '|',
            ';': ';', ':': ':',
            "'": "'", '"': '"',
            ',': ',', '<': '<',
            '.': '.', '>': '>',
            '/': '/', '?': '?',
            '!': '!', '@': '@',
            '#': '#', '$': '$',
            '%': '%', '^': '^',
            '&': '&', '*': '*',
            '(': '(', ')': ')',
        }
        mapping.update(symbols)
        
        # 4. 特殊功能键映射 (pynput的Key对象到字符串)
        key_mappings = {
            # 常用键
            Key.space: "space",
            Key.enter: "enter",
            Key.tab: "tab",
            Key.backspace: "backspace",
            Key.delete: "delete",
            Key.insert: "insert",
            Key.home: "home",
            Key.end: "end",
            Key.page_up: "page up",
            Key.page_down: "page down",
            Key.esc: "esc",
            Key.caps_lock: "caps lock",
            Key.num_lock: "num lock",
            Key.scroll_lock: "scroll lock",
            Key.print_screen: "print screen",
            Key.pause: "pause",
            
            # 方向键
            Key.left: "left",
            Key.right: "right",
            Key.up: "up",
            Key.down: "down",
            
            # 修饰键
            Key.shift: "shift",
            Key.shift_l: "shift",
            Key.shift_r: "shift",
            Key.ctrl: "ctrl",
            Key.ctrl_l: "ctrl",
            Key.ctrl_r: "ctrl",
            Key.alt: "alt",
            Key.alt_l: "alt",
            Key.alt_r: "alt",
            Key.alt_gr: "alt gr",
            Key.cmd: "windows",
            Key.cmd_l: "windows",
            Key.cmd_r: "windows",
            Key.menu: "menu",
        }
        
        # 5. 功能键 F1-F12
        for i in range(1, 13):
            f_key = getattr(Key, f'f{i}', None)
            if f_key is not None:
                key_mappings[f_key] = f'f{i}'
        
        # 6. 小键盘数字键 (需要特殊处理，pynput通常用普通数字表示)
        # 注意：小键盘数字和普通数字在pynput中可能相同
        
        # 将key_mappings添加到mapping中
        # 注意：这里键是Key对象，值是字符串
        self._key_to_str = key_mappings
        self._char_to_str = mapping
        
        # 创建反向查找表，用于快速判断是否允许
        self._allowed_set = set(mapping.values()) | set(key_mappings.values())
        
        return mapping
    
    def _on_press(self, key):
        """按键按下时的回调函数"""
        self.pressed_keys[key] = True
    
    def _on_release(self, key):
        """按键释放时的回调函数"""
        self.pressed_keys[key] = False
    
    def _key_to_string(self, key):
        """将key对象转换为字符串，只返回映射表中允许的键"""
        try:
            # 1. 如果是普通字符键
            if hasattr(key, 'char') and key.char is not None:
                char = key.char
                if isinstance(char, str):
                    # 检查是否在允许的字符映射中
                    if char in self._char_to_str:
                        return self._char_to_str[char]
                    # 如果是字母，转换为小写检查
                    elif len(char) == 1 and char.isalpha():
                        return char.lower()
                    # 如果是数字
                    elif len(char) == 1 and char.isdigit():
                        return char
            # 2. 如果是特殊键，从特殊键映射表中查找
            if key in self._key_to_str:
                return self._key_to_str[key]
            
            # 3. 尝试获取键名并检查是否在允许的集合中
            try:
                name = str(key)
                if name.startswith('Key.'):
                    name = name[4:]
                name = name.replace('_', ' ').lower()
                
                # 检查这个名称是否在允许的集合中
                if name in self._allowed_set:
                    return name
            except:
                pass
        except Exception as e:
            pass
        
        # 不在映射表中的键返回None
        return None
    
    def get_pressed_keys(self):
        """
        获取当前按下的所有按键的实际意义字符串列表
        只包含预定义映射表中的键
        """
        pressed_keys_list = []
        shift_pressed = False
        caps_lock_active = False
        
        # 1. 先检查修饰键状态
        for key, pressed in list(self.pressed_keys.items()):
            if pressed:
                key_str = self._key_to_string(key)
                if key_str == "shift":
                    shift_pressed = True
                elif key_str == "caps lock":
                    # 注意：需要额外逻辑检测caps lock状态，这里简化处理
                    caps_lock_active = True
        
        # 2. 收集所有按下的键
        for key, pressed in list(self.pressed_keys.items()):
            if pressed:
                key_str = self._key_to_string(key)
                
                # 跳过不在映射表中的键
                if key_str is None:
                    continue
                
                # 处理字母键的大小写
                if key_str and len(key_str) == 1 and key_str.isalpha():
                    # 如果shift被按下或者caps lock被激活（但不是同时）
                    if (shift_pressed and not caps_lock_active) or \
                       (not shift_pressed and caps_lock_active):
                        key_str = key_str.upper()
                    else:
                        key_str = key_str.lower()
                
                # 处理数字键上的符号（需要shift）
                elif key_str in '`-=[]\\;\',./':
                    if shift_pressed:
                        # 数字键上方的符号
                        shift_symbols = {
                            '`': '~', '-': '_', '=': '+',
                            '[': '{', ']': '}', '\\': '|',
                            ';': ':', "'": '"', ',': '<',
                            '.': '>', '/': '?'
                        }
                        if key_str in shift_symbols:
                            key_str = shift_symbols[key_str]
                
                # 确保按键在列表中只出现一次
                if key_str and key_str not in pressed_keys_list:
                    pressed_keys_list.append(key_str)
        
        return pressed_keys_list
    
    def cleanup(self):
        """清理资源"""
        if self.listener and self.listener.running:
            self.listener.stop()