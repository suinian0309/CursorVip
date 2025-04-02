import os
import sys
import time
import shutil
import platform
from colorama import Fore, Style, init
from cursor_auth import CursorAuth
from quit_cursor import quit_cursor
from reset_machine_manual import MachineIDResetter
import cursor_register_manual

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'START': '🚀',
    'RESET': '🔄',
    'DELETE': '🗑️',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'KEY': '🔐'
}

class CursorAccountDeleter:
    def __init__(self, translator=None):
        self.translator = translator
        
        # 获取操作系统类型
        self.system = platform.system()
        self.home = os.path.expanduser("~")
        
        # 确定SQLite数据库路径
        try:
            if self.system == "Windows":
                self.db_dir = os.path.join(self.home, "AppData", "Roaming", "Cursor")
                self.sqlite_path = os.path.join(self.db_dir, "Local Storage", "leveldb", "LOCK")
            elif self.system == "Darwin":  # macOS
                self.db_dir = os.path.join(self.home, "Library", "Application Support", "Cursor")
                self.sqlite_path = os.path.join(self.db_dir, "Local Storage", "leveldb", "LOCK")
            elif self.system == "Linux":
                self.db_dir = os.path.join(self.home, ".config", "Cursor")
                self.sqlite_path = os.path.join(self.db_dir, "Local Storage", "leveldb", "LOCK")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.unsupported_platform')}{Style.RESET_ALL}")
                sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.error_getting_paths', error=str(e))}{Style.RESET_ALL}")
            sys.exit(1)
    
    def delete_cursor_account(self):
        """删除Cursor账号相关数据"""
        try:
            # 首先关闭Cursor应用程序
            print(f"{Fore.CYAN}{EMOJI['WAIT']} {self.translator.get('delete_account.closing_cursor')}{Style.RESET_ALL}")
            quit_cursor(self.translator)
            time.sleep(2)
            
            # 提示用户手动删除账户
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('delete_account.manual_delete_prompt')}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} {self.translator.get('delete_account.manual_delete_instructions')}{Style.RESET_ALL}")
            
            # 等待用户确认
            input(f"\n{EMOJI['INFO']} {Fore.CYAN}{self.translator.get('delete_account.press_enter_to_continue')}{Style.RESET_ALL}")
            
            # 清理本地认证信息
            print(f"{Fore.CYAN}{EMOJI['DELETE']} {self.translator.get('delete_account_online.deleting_auth')}...{Style.RESET_ALL}")
            auth_manager = CursorAuth(translator=self.translator)
            if not auth_manager.delete_auth():
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.auth_deletion_failed')}{Style.RESET_ALL}")
                return False
                
            # 删除认证相关文件
            print(f"{Fore.CYAN}{EMOJI['DELETE']} {self.translator.get('delete_account_online.deleting_auth_files')}...{Style.RESET_ALL}")
            self._delete_auth_files()
            
            # 重置机器ID
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('delete_account_online.resetting_machine_id')}...{Style.RESET_ALL}")
            resetter = MachineIDResetter(self.translator)
            if not resetter.reset_machine_ids():
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account_online.machine_id_reset_failed')}{Style.RESET_ALL}")
                return False
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account_online.completed')}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.deletion_process_error', error=str(e))}{Style.RESET_ALL}")
            return False
    
    def _delete_auth_files(self):
        """删除认证相关文件"""
        try:
            print(f"{Fore.CYAN}{EMOJI['DELETE']} {self.translator.get('delete_account.removing_auth_files')}{Style.RESET_ALL}")
            
            # 定义需要删除的文件列表
            auth_files = []
            
            if self.system == "Windows":
                auth_files = [
                    os.path.join(self.home, "AppData", "Roaming", "Cursor", "Cookies"),
                    os.path.join(self.home, "AppData", "Roaming", "Cursor", "Cookies-journal"),
                    os.path.join(self.home, "AppData", "Roaming", "Cursor", "Network Persistent State"),
                    os.path.join(self.home, "AppData", "Roaming", "Cursor", "Session Storage"),
                    os.path.join(self.db_dir, "Local Storage", "leveldb"),
                ]
            elif self.system == "Darwin":  # macOS
                auth_files = [
                    os.path.join(self.db_dir, "Cookies"),
                    os.path.join(self.db_dir, "Cookies-journal"),
                    os.path.join(self.db_dir, "Network Persistent State"),
                    os.path.join(self.db_dir, "Session Storage"),
                    os.path.join(self.db_dir, "Local Storage", "leveldb"),
                ]
            elif self.system == "Linux":
                auth_files = [
                    os.path.join(self.db_dir, "Cookies"),
                    os.path.join(self.db_dir, "Cookies-journal"),
                    os.path.join(self.db_dir, "Network Persistent State"),
                    os.path.join(self.db_dir, "Session Storage"),
                    os.path.join(self.db_dir, "Local Storage", "leveldb"),
                ]
            
            # 删除认证文件
            for file_path in auth_files:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        try:
                            shutil.rmtree(file_path)
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account.removed_directory')}: {file_path}{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.remove_directory_failed', error=str(e))}: {file_path}{Style.RESET_ALL}")
                    else:
                        try:
                            os.remove(file_path)
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('delete_account.removed_file')}: {file_path}{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.remove_file_failed', error=str(e))}: {file_path}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('delete_account.auth_files_deletion_error', error=str(e))}{Style.RESET_ALL}")

def run(translator=None):
    """主函数，从main.py调用"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('delete_account.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # 显示警告并获取确认
    print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account.warning')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account.warning_details')}{Style.RESET_ALL}")
    
    # 获取当前认证信息
    auth_manager = CursorAuth(translator=translator)
    current_auth = auth_manager.get_auth()
    current_email = current_auth.get('email') if current_auth else None
    
    # 要求用户输入邮箱
    print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.email_input_prompt')}{Style.RESET_ALL}")
    if current_email:
        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.current_email')}: {current_email}{Style.RESET_ALL}")
    
    email_input = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.enter_email')}: {Style.RESET_ALL}").strip()
    
    # 检查输入是否为空
    if not email_input:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.email_empty')}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")
        return
    
    # 检查输入的邮箱与当前邮箱是否匹配
    if current_email and current_email.lower() != email_input.lower():
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.email_mismatch')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account.login_with_correct_email')}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")
        return
    
    # 确认是否继续
    choice = input(f"\n{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()
    if choice not in ['', 'y', 'yes']:
        print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account.operation_cancelled')}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")
        return
    
    # 删除账号
    deleter = CursorAccountDeleter(translator)
    if deleter.delete_cursor_account():
        # 询问是否要立即重新注册
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.register_prompt')}{Style.RESET_ALL}")
        choice = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.register_confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()
        
        if choice in ['', 'y', 'yes']:
            print(f"\n{Fore.CYAN}{EMOJI['START']} {translator.get('delete_account.starting_registration')}{Style.RESET_ALL}")
            
            # 询问是否使用刚才的邮箱
            print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.use_previous_email_prompt', email=email_input)}{Style.RESET_ALL}")
            use_previous_email = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.use_previous_email', choices='Y/n')}: {Style.RESET_ALL}").lower()
            
            if use_previous_email in ['', 'y', 'yes']:
                # 请求用户输入密码
                print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.enter_password_prompt')}{Style.RESET_ALL}")
                password = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.password')}: {Style.RESET_ALL}").strip()
                
                # 检查密码是否为空或太短
                if not password or len(password) < 8:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.password_too_short')}{Style.RESET_ALL}")
                    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                    input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")
                    return
                
                # 调用注册功能，传递邮箱和密码
                cursor_register_manual.main(translator, email=email_input, password=password)
            else:
                # 使用原始注册流程
                cursor_register_manual.main(translator)
        else:
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account.registration_skipped')}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")

if __name__ == "__main__":
    # 如果直接运行此脚本，使用main.py中的翻译器
    from main import translator as main_translator
    run(main_translator) 