import os
import sys
import time
import json
import random
from colorama import Fore, Style, init
from DrissionPage import ChromiumPage, ChromiumOptions
from cursor_auth import CursorAuth
from utils import get_random_wait_time
from config import get_config
from quit_cursor import quit_cursor

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'START': '🚀',
    'DELETE': '🗑️',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'WAIT': '⏳',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'KEY': '🔐'
}

class CursorOnlineAccountDeleter:
    """用于删除Cursor官网账户的类"""
    
    def __init__(self, translator=None):
        self.translator = translator
        self.config = get_config(translator)
        self.browser = None
        self.auth_manager = CursorAuth(translator=translator)
        
    def setup_browser(self):
        """设置浏览器"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.initializing_browser')}{Style.RESET_ALL}")
            
            # 获取Chrome路径
            chrome_path = None
            if self.config.has_section('Chrome') and self.config.has_option('Chrome', 'chromepath'):
                chrome_path = self.config.get('Chrome', 'chromepath')
                if os.path.exists(chrome_path):
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.using_chrome_path')}: {chrome_path}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.chrome_path_not_exist')}: {chrome_path}{Style.RESET_ALL}")
                    chrome_path = None
            
            # 如果配置中没有Chrome路径或路径不存在，尝试自动检测
            if not chrome_path:
                try:
                    from utils import get_default_chrome_path
                    chrome_path = get_default_chrome_path()
                    if chrome_path and os.path.exists(chrome_path):
                        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.auto_detected_chrome')}: {chrome_path}{Style.RESET_ALL}")
                    else:
                        raise Exception("Chrome not found")
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.chrome_detection_failed')}: {str(e)}{Style.RESET_ALL}")
                    return False
            
            # 配置浏览器选项
            co = ChromiumOptions()
            co.set_paths(browser_path=chrome_path)
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-gpu')
            co.set_argument('--disable-dev-shm-usage')
            co.set_argument('--no-first-run')
            co.set_argument('--no-default-browser-check')
            
            # 初始化浏览器
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.starting_browser')}{Style.RESET_ALL}")
            self.browser = ChromiumPage(co)
            
            if not self.browser:
                raise Exception("Browser initialization failed")
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.browser_initialized')}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.browser_setup_failed')}: {str(e)}{Style.RESET_ALL}")
            return False
    
    def login_to_cursor(self):
        """登录到Cursor官网"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.logging_in')}{Style.RESET_ALL}")
            
            # 获取当前的认证信息
            auth_info = self.auth_manager.get_auth()
            if not auth_info or not auth_info.get('email') or not auth_info.get('access_token'):
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.no_auth_info')}{Style.RESET_ALL}")
                return False
                
            email = auth_info.get('email')
            token = auth_info.get('access_token')
            
            # 打开Cursor官网
            self.browser.get("https://www.cursor.com")
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 设置认证Cookie
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.setting_auth_cookie')}{Style.RESET_ALL}")
            self.browser.set_cookies([{
                'name': 'WorkosCursorSessionToken',
                'value': f'SESSION_TOKEN::{token}',
                'domain': 'cursor.com',
                'path': '/'
            }])
            
            # 刷新页面
            self.browser.refresh()
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 导航到设置页面
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.navigating_to_settings')}{Style.RESET_ALL}")
            self.browser.get("https://www.cursor.com/settings")
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 检查是否成功登录（通过查找页面上的电子邮件地址）
            try:
                email_element = self.browser.ele("css:div[class='flex w-full flex-col gap-2'] div:nth-child(2) p:nth-child(2)", timeout=5)
                if email_element and email_element.is_displayed():
                    found_email = email_element.text
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.login_successful')}: {found_email}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.email_not_found')}{Style.RESET_ALL}")
                    
                    # 尝试检查是否在设置页面
                    if "settings" in self.browser.url:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.on_settings_but_no_email')}{Style.RESET_ALL}")
                        # 可能已登录但布局不同，尝试继续
                        return True
                    return False
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.email_check_failed')}: {str(e)}{Style.RESET_ALL}")
                
                # 尝试检查是否在设置页面
                if "settings" in self.browser.url:
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.on_settings_but_error')}{Style.RESET_ALL}")
                    # 可能已登录但出现其他错误，尝试继续
                    return True
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.login_failed')}: {str(e)}{Style.RESET_ALL}")
            return False
    
    def delete_account(self):
        """删除Cursor官网账户"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.deleting_account')}{Style.RESET_ALL}")
            
            # 先尝试通过API直接删除
            api_delete_success = self._delete_account_api()
            
            # 如果API删除成功，验证删除结果
            if api_delete_success:
                if self.verify_account_deletion():
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.api_delete_success')}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.api_delete_unverified')}{Style.RESET_ALL}")
            
            # 如果API删除失败或验证失败，尝试通过UI删除
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.api_delete_failed')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.trying_ui_delete')}{Style.RESET_ALL}")
            
            # 确保在设置页面
            if "settings" not in self.browser.url:
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.navigating_to_settings')}{Style.RESET_ALL}")
                self.browser.get("https://www.cursor.com/settings")
                time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 查找"删除账户"按钮
            delete_account_selectors = [
                "//button[contains(text(), 'Delete Account')]",
                "//button[contains(text(), 'delete account')]",
                "//button[contains(text(), 'Delete account')]",
                "//button[contains(text(), 'Delete my account')]",
                "//button[contains(@class, 'delete') or contains(@class, 'danger')]",
                "//div[contains(@class, 'danger-zone')]//button"
            ]
            
            delete_btn = None
            for selector in delete_account_selectors:
                try:
                    delete_btn = self.browser.ele(f"xpath:{selector}", timeout=2)
                    if delete_btn and delete_btn.is_displayed():
                        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.found_delete_button')}{Style.RESET_ALL}")
                        break
                except:
                    continue
            
            if not delete_btn:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.delete_button_not_found')}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.trying_javascript')}{Style.RESET_ALL}")
                
                # 尝试使用JavaScript创建删除按钮
                js_create_button = """
                document.body.insertAdjacentHTML('beforeend', '<button id="cursor-delete-account-btn" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: red; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; z-index: 9999;">Delete Cursor Account</button>');
                document.getElementById('cursor-delete-account-btn').addEventListener('click', function() {
                    fetch('https://www.cursor.com/api/dashboard/delete-account', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'include'
                    }).then(response => {
                        if (response.status === 200) {
                            alert('Account deleted successfully!');
                        } else {
                            alert('Failed to delete account: ' + response.status);
                        }
                    }).catch(error => {
                        alert('Error deleting account: ' + error);
                    });
                });
                return 'Button created';
                """
                
                try:
                    result = self.browser.run_js(js_create_button)
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.js_button_result')}: {result}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.click_js_button')}{Style.RESET_ALL}")
                    
                    # 点击创建的按钮
                    js_click_button = "document.getElementById('cursor-delete-account-btn').click(); return 'Button clicked';"
                    click_result = self.browser.run_js(js_click_button)
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.js_click_result')}: {click_result}{Style.RESET_ALL}")
                    
                    # 等待JS删除操作完成
                    time.sleep(3)
                    
                    # 验证删除结果
                    if self.verify_account_deletion():
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.js_delete_success')}{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.js_delete_unverified')}{Style.RESET_ALL}")
                        return False
                    
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.js_delete_failed')}: {str(e)}{Style.RESET_ALL}")
                    return False
            
            # 找到删除按钮后点击
            try:
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.clicking_delete_button')}{Style.RESET_ALL}")
                delete_btn.click()
                time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                
                # 查找并点击确认删除的按钮
                confirm_selectors = [
                    "//button[contains(text(), 'Confirm deletion')]",
                    "//button[contains(text(), 'Confirm delete')]",
                    "//button[contains(text(), 'Delete')]",
                    "//button[contains(text(), 'Yes')]",
                    "//button[contains(@class, 'confirm') or contains(@class, 'danger')]",
                    "//div[contains(@class, 'modal')]//button[last()]"
                ]
                
                confirm_btn = None
                for selector in confirm_selectors:
                    try:
                        confirm_btn = self.browser.ele(f"xpath:{selector}", timeout=2)
                        if confirm_btn and confirm_btn.is_displayed():
                            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.found_confirm_button')}{Style.RESET_ALL}")
                            break
                    except:
                        continue
                
                if confirm_btn:
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.clicking_confirm_button')}{Style.RESET_ALL}")
                    confirm_btn.click()
                    time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                    
                    # 验证删除结果
                    if self.verify_account_deletion():
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.ui_delete_success')}{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.ui_delete_unverified')}{Style.RESET_ALL}")
                        return False
                    
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.confirm_button_not_found')}{Style.RESET_ALL}")
                    # 虽然没找到确认按钮，但可能初次点击就已经删除了，尝试验证
                    if self.verify_account_deletion():
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.ui_delete_success')}{Style.RESET_ALL}")
                        return True
                    return False
                    
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.ui_delete_failed')}: {str(e)}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.delete_process_failed')}: {str(e)}{Style.RESET_ALL}")
            return False
            
    def _delete_account_api(self):
        """通过API删除账户"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.using_api')}{Style.RESET_ALL}")
            
            # 获取认证令牌
            auth_info = self.auth_manager.get_auth()
            if not auth_info or not auth_info.get('access_token'):
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.no_auth_token')}{Style.RESET_ALL}")
                return False
            
            token = auth_info.get('access_token')
            
            # 使用JavaScript来发送删除账户的API请求
            delete_js = f"""
            function deleteAccount() {{
                return new Promise((resolve, reject) => {{
                    fetch('https://www.cursor.com/api/dashboard/delete-account', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer {token}'
                        }},
                        credentials: 'include'
                    }})
                    .then(response => {{
                        if (response.status === 200) {{
                            resolve('Account deleted successfully');
                        }} else {{
                            reject('Failed to delete account: ' + response.status);
                        }}
                    }})
                    .catch(error => {{
                        reject('Error: ' + error);
                    }});
                }});
            }}
            return deleteAccount();
            """
            
            result = self.browser.run_js(delete_js)
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.api_result')}: {result}{Style.RESET_ALL}")
            
            # 验证API是否成功
            if "success" in str(result).lower():
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.api_success')}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.api_unexpected_result')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.api_failed')}: {str(e)}{Style.RESET_ALL}")
            return False
            
    def cleanup_local(self):
        """清理本地Cursor认证信息"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.cleaning_local')}{Style.RESET_ALL}")
            
            # 关闭Cursor应用程序
            quit_cursor(self.translator)
            time.sleep(2)
            
            # 清除认证信息
            if self.auth_manager.update_auth(email=None, access_token=None, refresh_token=None):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.local_auth_cleared')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.local_auth_clear_failed')}{Style.RESET_ALL}")
                
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.local_cleanup_failed')}: {str(e)}{Style.RESET_ALL}")
            return False
    
    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            try:
                self.browser.quit()
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.browser_closed')}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.browser_close_failed')}: {str(e)}{Style.RESET_ALL}")
            self.browser = None

    def verify_account_deletion(self):
        """验证账户是否已被删除"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.verifying_deletion')}{Style.RESET_ALL}")
            
            # 尝试访问需要认证的页面
            self.browser.get('https://www.cursor.com/dashboard')
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 检查是否被重定向到登录页面
            if "login" in self.browser.url or "sign" in self.browser.url:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.verification_success')}{Style.RESET_ALL}")
                return True
            
            # 检查页面内容
            page_text = self.browser.text.lower()
            if "login" in page_text or "sign in" in page_text or "register" in page_text:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.verification_success')}{Style.RESET_ALL}")
                return True
            
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.verification_inconclusive')}{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.verification_failed')}: {str(e)}{Style.RESET_ALL}")
            return False

def run(translator=None):
    """主函数，从main.py调用"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('delete_account_online.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 显示警告并获取确认
    print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account_online.warning')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account_online.warning_details')}{Style.RESET_ALL}")
    
    # 确认是否继续
    choice = input(f"\n{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account_online.confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()
    if choice not in ['', 'y', 'yes']:
        print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account_online.operation_cancelled')}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        input(f"{EMOJI['INFO']} {translator.get('delete_account_online.press_enter')}...")
        return
    
    # 创建删除器实例
    deleter = CursorOnlineAccountDeleter(translator)
    
    try:
        # 初始化浏览器
        if not deleter.setup_browser():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.browser_setup_failed')}{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            input(f"{EMOJI['INFO']} {translator.get('delete_account_online.press_enter')}...")
            return
        
        # 登录到Cursor
        if not deleter.login_to_cursor():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.login_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            input(f"{EMOJI['INFO']} {translator.get('delete_account_online.press_enter')}...")
            return
        
        # 删除账户
        delete_success = deleter.delete_account()
        
        # 清理本地Cursor认证信息
        local_cleanup_success = deleter.cleanup_local()
        
        # 关闭浏览器
        deleter.close_browser()
        
        # 询问是否要立即重新注册
        if delete_success:
            print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('delete_account_online.account_deleted')}{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account_online.register_prompt')}{Style.RESET_ALL}")
            choice = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account_online.register_confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()
            
            if choice in ['', 'y', 'yes']:
                print(f"\n{Fore.CYAN}{EMOJI['START']} {translator.get('delete_account_online.starting_registration')}{Style.RESET_ALL}")
                # 调用注册功能
                import cursor_register_manual
                cursor_register_manual.main(translator)
            else:
                print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account_online.registration_skipped')}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.account_delete_failed')}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.unexpected_error')}: {str(e)}{Style.RESET_ALL}")
        # 尝试关闭浏览器
        deleter.close_browser()
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('delete_account_online.press_enter')}...")

if __name__ == "__main__":
    # 如果直接运行此脚本，使用main.py中的翻译器
    from main import translator as main_translator
    run(main_translator)
