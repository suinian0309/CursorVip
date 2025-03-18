# show_wechat_group.py
import os
import sys
import platform
import webbrowser
from colorama import Fore, Style, init

# 初始化 colorama
init()

# 定义GitHub上交流群二维码的URL
GITHUB_GROUP_QR_URL = "https://github.com/suinian0309/CursorVip/blob/main/images/wechat_group.jpg?raw=true"

def is_frozen():
    """检查是否是打包后的程序"""
    return getattr(sys, 'frozen', False)

def get_resource_path(relative_path):
    """获取资源文件的路径，无论是打包后还是开发模式"""
    if is_frozen():
        # 如果是打包后的程序
        base_path = os.path.dirname(sys.executable)
        return os.path.join(base_path, relative_path)
    else:
        # 如果是开发模式
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def show(translator):
    """显示微信群信息并尝试打开浏览器"""
    print(f"\n{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{translator.get('join_group.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
    
    try:
        # 尝试打开浏览器
        print(f"{Fore.YELLOW}{translator.get('join_group.opening_browser')}{Style.RESET_ALL}")
        webbrowser.open(GITHUB_GROUP_QR_URL)
        print(f"{Fore.GREEN}{translator.get('join_group.browser_opened')}{Style.RESET_ALL}")
    except Exception as e:
        # 如果打开浏览器失败，输出错误信息
        print(f"{Fore.RED}{translator.get('join_group.browser_error')}: {str(e)}{Style.RESET_ALL}")
    
    # 无论是否成功打开浏览器，都显示链接和说明
    print(f"\n{Fore.CYAN}{translator.get('join_group.group_description')}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}{translator.get('join_group.manual_link')}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{GITHUB_GROUP_QR_URL}{Style.RESET_ALL}")
    
    # 等待用户按任意键继续
    input(f"\n{Fore.GREEN}{translator.get('join_group.press_any_key')}{Style.RESET_ALL}")

def get_ascii_qrcode():
    """返回预定义的 ASCII 二维码"""
    # 这里是一个简单的 ASCII 二维码示例
    # 实际使用时，您可以使用更复杂的方法生成真实的二维码
    return """
██████████████      ████  ██████████████
██          ██  ██  ████  ██          ██
██  ██████  ██    ██████  ██  ██████  ██
██  ██████  ██  ██    ██  ██  ██████  ██
██  ██████  ██  ██  ████  ██  ██████  ██
██          ██  ██  ████  ██          ██
██████████████  ██  ██  ██████████████
                ████████              
██  ██████████  ██  ██  ██████  ██████
██  ██      ██████    ██████  ████    
████  ██  ██████  ██████  ██  ██  ████
██  ██  ██  ██  ██  ██  ██████  ██  ██
██  ██████  ██████  ██  ██  ██  ██████
██      ██████  ██████  ██  ██████    
██████████████  ██  ██  ██  ██  ██████
                ██████              ██
██████████████  ██  ██  ██████████  ██
██          ██  ████    ██  ██  ██████
██  ██████  ██  ██  ██████  ██  ██    
██  ██████  ██  ██████  ██████  ██████
██  ██████  ██  ██  ██████  ██  ██  ██
██          ██  ██████  ██  ██████  ██
██████████████  ██████  ██  ██  ██████
"""

# 取消注释下面的函数并安装必要的库
# 需要安装: pip install qrcode pillow

def generate_qr_ascii():
    """生成真实的二维码并转换为 ASCII"""
    try:
        from PIL import Image
        import os
        
        # 获取微信群二维码图片的路径
        image_path = get_resource_path(os.path.join('images', 'wechat_group.jpg'))
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"找不到微信群二维码图片: {image_path}")
        
        # 打开并处理图片
        img = Image.open(image_path)
        
        # 转换为 ASCII
        width, height = img.size
        aspect_ratio = height/width
        new_width = 40
        new_height = int(aspect_ratio * new_width * 0.5)
        img = img.resize((new_width, new_height))
        
        # 转换为灰度图
        img = img.convert('L')
        
        chars = ["██", "  "]
        
        # 生成 ASCII 艺术
        ascii_art = ""
        pixels = list(img.getdata())
        for i in range(new_height):
            for j in range(new_width):
                ascii_art += chars[0] if pixels[i*new_width + j] < 128 else chars[1]
            ascii_art += "\n"
        
        return ascii_art
        
    except Exception as e:
        # 如果出现任何错误，返回预定义的 ASCII 二维码
        print(f"生成二维码时出错: {str(e)}")
        return get_ascii_qrcode() 