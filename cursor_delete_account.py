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
            self.browser.cookies.add({
                'name': 'WorkosCursorSessionToken',
                'value': f'SESSION_TOKEN::{token}',
                'domain': 'cursor.com',
                'path': '/'
            })
            
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
                return False
            
            # 点击删除按钮
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.clicking_delete_button')}{Style.RESET_ALL}")
            delete_btn.click()
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 查找确认输入框
            confirm_input_selectors = [
                "//input[contains(@placeholder, 'delete')]",
                "//input[contains(@placeholder, 'confirm')]",
                "//div[contains(@class, 'modal')]//input"
            ]
            
            confirm_input = None
            for selector in confirm_input_selectors:
                try:
                    confirm_input = self.browser.ele(f"xpath:{selector}", timeout=2)
                    if confirm_input and confirm_input.is_displayed():
                        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.found_confirm_input')}{Style.RESET_ALL}")
                        break
                except:
                    continue
            
            if confirm_input:
                # 输入 "delete" 确认
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.entering_delete_confirmation')}{Style.RESET_ALL}")
                confirm_input.click()
                time.sleep(get_random_wait_time(self.config, 'user_action_wait', default=0.5))
                confirm_input.input("delete")
                time.sleep(get_random_wait_time(self.config, 'user_action_wait', default=0.5))
                
                # 查找并点击最终确认按钮
                confirm_button_selectors = [
                    "//button[contains(text(), 'Confirm')]",
                    "//button[contains(text(), 'Delete')]",
                    "//div[contains(@class, 'modal')]//button[last()]"
                ]
                
                confirm_btn = None
                for selector in confirm_button_selectors:
                    try:
                        confirm_btn = self.browser.ele(f"xpath:{selector}", timeout=2)
                        if confirm_btn and confirm_btn.is_displayed():
                            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.found_final_confirm_button')}{Style.RESET_ALL}")
                            break
                    except:
                        continue
                
                if confirm_btn:
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.clicking_final_confirm')}{Style.RESET_ALL}")
                    confirm_btn.click()
                    time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
                    
                    # 验证删除结果
                    if self.verify_account_deletion():
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.ui_delete_success')}{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.ui_delete_unverified')}{Style.RESET_ALL}")
                        # 尝试使用API作为备选方案
                        return self._delete_account_api()
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.final_confirm_button_not_found')}{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.confirm_input_not_found')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.delete_process_failed')}: {str(e)}{Style.RESET_ALL}")
            # 如果UI删除失败,尝试使用API作为备选方案
            return self._delete_account_api()
            
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
            email = auth_info.get('email', '')
            
            # 验证令牌有效性 - 先尝试获取用户信息
            validate_js = f"""
            function validateToken() {{
                return new Promise((resolve, reject) => {{
                    fetch('https://www.cursor.com/api/dashboard/user', {{
                        method: 'GET',
                        headers: {{
                            'Authorization': 'Bearer {token}',
                            'Content-Type': 'application/json'
                        }},
                        credentials: 'include'
                    }})
                    .then(response => {{
                        if (response.status === 200) {{
                            resolve('Token valid');
                        }} else {{
                            reject('Token invalid or expired: ' + response.status);
                        }}
                    }})
                    .catch(error => {{
                        reject('Error validating token: ' + error);
                    }});
                }});
            }}
            return validateToken();
            """
            
            try:
                validate_result = self.browser.run_js(validate_js)
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.token_validation')}: {validate_result}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.token_validation_failed')}: {str(e)}{Style.RESET_ALL}")
                # 继续尝试删除，即使验证失败
            
            # 进行预检请求，确认CORS和权限
            preflight_js = f"""
            function checkDeleteEndpoint() {{
                return new Promise((resolve, reject) => {{
                    fetch('https://www.cursor.com/api/dashboard/delete-account', {{
                        method: 'OPTIONS',
                        headers: {{
                            'Origin': 'https://www.cursor.com',
                            'Access-Control-Request-Method': 'POST',
                            'Access-Control-Request-Headers': 'Content-Type, Authorization'
                        }}
                    }})
                    .then(response => {{
                        if (response.ok) {{
                            resolve('Preflight successful');
                        }} else {{
                            resolve('Preflight response: ' + response.status);
                        }}
                    }})
                    .catch(error => {{
                        resolve('Preflight error: ' + error);
                    }});
                }});
            }}
            return checkDeleteEndpoint();
            """
            
            try:
                preflight_result = self.browser.run_js(preflight_js)
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.preflight_check')}: {preflight_result}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.preflight_check_failed')}: {str(e)}{Style.RESET_ALL}")
                # 继续尝试删除，即使预检失败
            
            # 先访问设置页面，确保cookies和会话状态正确
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.preparing_session')}{Style.RESET_ALL}")
            self.browser.get("https://www.cursor.com/settings")
            time.sleep(get_random_wait_time(self.config, 'page_load_wait'))
            
            # 模拟用户浏览行为
            scroll_js = "window.scrollTo(0, document.body.scrollHeight/2); return 'Scrolled';"
            self.browser.run_js(scroll_js)
            time.sleep(get_random_wait_time(self.config, 'user_action_wait', default=1.5))
            
            # 获取当前页面的cookies和CSRF令牌（如果有）
            csrf_token_js = """
            function getCSRFToken() {
                // 从meta标签获取
                const metaToken = document.querySelector('meta[name="csrf-token"]');
                if (metaToken) return metaToken.getAttribute('content');
                
                // 从cookie获取
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith('XSRF-TOKEN=')) {
                        return decodeURIComponent(cookie.substring(11));
                    }
                }
                return null;
            }
            return getCSRFToken();
            """
            
            csrf_token = None
            try:
                csrf_token = self.browser.run_js(csrf_token_js)
                if csrf_token and csrf_token != "null":
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.csrf_token_found')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.no_csrf_token')}{Style.RESET_ALL}")
                    csrf_token = None
            except Exception as e:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.csrf_token_error')}: {str(e)}{Style.RESET_ALL}")
            
            # 构建完整的删除请求
            csrf_header = f"'X-CSRF-TOKEN': '{csrf_token}'," if csrf_token else ""
            
            # 使用JavaScript来发送删除账户的API请求，添加多种认证方式和头部
            delete_js = f"""
            function deleteAccount() {{
                return new Promise((resolve, reject) => {{
                    // 随机延时，模拟真实用户行为
                    setTimeout(() => {{
                        // 构建请求体，可能需要额外确认参数
                        const requestBody = JSON.stringify({{
                            confirm: true,
                            email: '{email}'
                        }});
                        
                        fetch('https://www.cursor.com/api/dashboard/delete-account', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {token}',
                                {csrf_header}
                                'Accept': 'application/json',
                                'Origin': 'https://www.cursor.com',
                                'Referer': 'https://www.cursor.com/settings',
                                'User-Agent': navigator.userAgent,
                                'Sec-Fetch-Site': 'same-origin',
                                'Sec-Fetch-Mode': 'cors'
                            }},
                            body: requestBody,
                            credentials: 'include'
                        }})
                        .then(response => {{
                            if (response.status === 200 || response.status === 204) {{
                                resolve('Account deleted successfully (Status: ' + response.status + ')');
                            }} else {{
                                // 尝试解析响应内容
                                response.text().then(text => {{
                                    try {{
                                        const json = JSON.parse(text);
                                        reject('Failed to delete account: ' + response.status + ' - ' + JSON.stringify(json));
                                    }} catch (e) {{
                                        reject('Failed to delete account: ' + response.status + ' - ' + text);
                                    }}
                                }}).catch(error => {{
                                    reject('Failed to delete account: ' + response.status);
                                }});
                            }}
                        }})
                        .catch(error => {{
                            reject('Error: ' + error);
                        }});
                    }}, Math.floor(Math.random() * 500) + 200); // 随机延时200-700ms
                }});
            }}
            return deleteAccount();
            """
            
            # 设置超时和重试机制
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    retry_count += 1
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.api_attempt', attempt=retry_count, max=max_retries)}{Style.RESET_ALL}")
                    
                    result = self.browser.run_js(delete_js)
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.api_result')}: {result}{Style.RESET_ALL}")
                    
                    # 验证API是否成功
                    if "success" in str(result).lower() or "deleted" in str(result).lower() or "200" in str(result) or "204" in str(result):
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.api_success')}{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {self.translator.get('delete_account_online.api_unexpected_result')}{Style.RESET_ALL}")
                        # 如果不是最后一次尝试，等待后重试
                        if retry_count < max_retries:
                            wait_time = retry_count * 2  # 递增等待时间
                            print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('delete_account_online.retrying', seconds=wait_time)}{Style.RESET_ALL}")
                            time.sleep(wait_time)
                        else:
                            return False
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.api_attempt_failed')}: {str(e)}{Style.RESET_ALL}")
                    # 如果不是最后一次尝试，等待后重试
                    if retry_count < max_retries:
                        wait_time = retry_count * 2  # 递增等待时间
                        print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('delete_account_online.retrying', seconds=wait_time)}{Style.RESET_ALL}")
                        time.sleep(wait_time)
                    else:
                        return False
            
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
    """运行删除账户流程"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('delete_account_online.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 获取当前认证信息
    auth_manager = CursorAuth(translator)
    auth_info = auth_manager.get_auth()
    
    if not auth_info or not auth_info.get('email'):
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.no_auth_info')}{Style.RESET_ALL}")
        return False
        
    current_email = auth_info.get('email')
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account_online.current_email')}: {current_email}{Style.RESET_ALL}")
    
    # 确认用户输入
    confirm_email = input(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account_online.confirm_email')}: {Style.RESET_ALL}")
    
    if confirm_email.lower() != current_email.lower():
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.email_mismatch')}{Style.RESET_ALL}")
        return False
        
    # 确认操作
    confirm = input(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account_online.confirm_delete')} (Y/n): {Style.RESET_ALL}")
    if confirm.lower() != 'y':
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account_online.operation_cancelled')}{Style.RESET_ALL}")
        return False
        
    # 关闭Cursor应用
    print(f"{Fore.CYAN}{EMOJI['WAIT']} {translator.get('delete_account_online.closing_cursor')}...{Style.RESET_ALL}")
    quit_cursor(translator)
    
    # 创建删除器实例
    deleter = CursorOnlineAccountDeleter(translator)
    
    try:
        # 初始化浏览器
        if not deleter.setup_browser():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.browser_setup_failed')}{Style.RESET_ALL}")
            return False
            
        # 登录到Cursor
        if not deleter.login_to_cursor():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.login_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            return False
            
        # 删除账户
        if not deleter.delete_account():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.account_delete_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            return False
            
        # 清理本地认证信息
        print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('delete_account_online.deleting_auth')}...{Style.RESET_ALL}")
        if not auth_manager.delete_auth():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.auth_deletion_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            return False
            
        # 删除认证相关文件
        print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('delete_account_online.deleting_auth_files')}...{Style.RESET_ALL}")
        if not deleter.cleanup_local():
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.file_deletion_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            return False
            
        # 重置机器ID
        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account_online.resetting_machine_id')}...{Style.RESET_ALL}")
        from reset_machine_manual import run as reset_machine
        if not reset_machine(translator):
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.machine_id_reset_failed')}{Style.RESET_ALL}")
            deleter.close_browser()
            return False
            
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('delete_account_online.completed')}{Style.RESET_ALL}")
        
        # 询问是否立即注册新账户
        register_new = input(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account_online.register_new')} (Y/n): {Style.RESET_ALL}")
        if register_new.lower() == 'y':
            from new_signup import new_signup_main
            new_signup_main(translator)
            
        return True
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account_online.unexpected_error')}: {str(e)}{Style.RESET_ALL}")
        return False
    finally:
        # 确保浏览器被关闭
        if hasattr(deleter, 'browser') and deleter.browser:
            deleter.close_browser()

if __name__ == "__main__":
    # 如果直接运行此脚本，使用main.py中的翻译器
    from main import translator as main_translator
    run(main_translator)
