# main.py
# This script allows the user to choose which script to run.
import os
import sys
import json
from logo import print_logo, version
from colorama import Fore, Style, init
import locale
import platform
import requests
import subprocess
from config import get_config  
import time
import shutil

# Only import windll on Windows systems
if platform.system() == 'Windows':
    import ctypes
    # 只在 Windows 上导入 windll
    from ctypes import windll

# Initialize colorama
init()

# Define emoji and color constants
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "MENU": "📋",
    "ARROW": "➜",
    "LANG": "🌐",
    "UPDATE": "🔄",
    "ADMIN": "🔐",
    "GROUP": "🤖",
    "DELETE": "🗑️",
    "LIFETIME": "🔥",
}

# Function to check if running as frozen executable
def is_frozen():
    """Check if the script is running as a frozen executable."""
    return getattr(sys, 'frozen', False)

# Function to check admin privileges (Windows only)
def is_admin():
    """Check if the script is running with admin privileges (Windows only)."""
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    # Always return True for non-Windows to avoid changing behavior
    return True

# Function to restart with admin privileges
def run_as_admin():
    """Restart the current script with admin privileges (Windows only)."""
    if platform.system() != 'Windows':
        return False
        
    try:
        args = [sys.executable] + sys.argv
        
        # Request elevation via ShellExecute
        print(f"{Fore.YELLOW}{EMOJI['ADMIN']} Requesting administrator privileges...{Style.RESET_ALL}")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", args[0], " ".join('"' + arg + '"' for arg in args[1:]), None, 1)
        return True
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to restart with admin privileges: {e}{Style.RESET_ALL}")
        return False

class Translator:
    def __init__(self):
        self.translations = {}
        self.current_language = self.detect_system_language()  # Use correct method name
        self.fallback_language = 'en'  # Fallback language if translation is missing
        self.load_translations()
    
    def detect_system_language(self):
        """Detect system language and return corresponding language code"""
        try:
            system = platform.system()
            
            if system == 'Windows':
                return self._detect_windows_language()
            else:
                return self._detect_unix_language()
                
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Failed to detect system language: {e}{Style.RESET_ALL}")
            return 'en'
    
    def _detect_windows_language(self):
        """Detect language on Windows systems"""
        try:
            # Ensure we are on Windows
            if platform.system() != 'Windows':
                return 'en'
                
            # Get keyboard layout
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            threadid = user32.GetWindowThreadProcessId(hwnd, 0)
            layout_id = user32.GetKeyboardLayout(threadid) & 0xFFFF
            
            # Map language ID to our language codes
            language_map = {
                0x0409: 'en',      # English
                0x0404: 'zh_tw',   # Traditional Chinese
                0x0804: 'zh_cn',   # Simplified Chinese
                0x0422: 'vi',      # Vietnamese
            }
            
            return language_map.get(layout_id, 'en')
        except:
            return self._detect_unix_language()
    
    def _detect_unix_language(self):
        """Detect language on Unix-like systems (Linux, macOS)"""
        try:
            # Get the system locale
            system_locale = locale.getdefaultlocale()[0]
            if not system_locale:
                return 'en'
            
            system_locale = system_locale.lower()
            
            # Map locale to our language codes
            if system_locale.startswith('zh_tw') or system_locale.startswith('zh_hk'):
                return 'zh_tw'
            elif system_locale.startswith('zh_cn'):
                return 'zh_cn'
            elif system_locale.startswith('en'):
                return 'en'
            elif system_locale.startswith('vi'):
                return 'vi'
            

            # Try to get language from LANG environment variable as fallback
            env_lang = os.getenv('LANG', '').lower()
            if 'tw' in env_lang or 'hk' in env_lang:
                return 'zh_tw'
            elif 'cn' in env_lang:
                return 'zh_cn'
            elif 'vi' in env_lang:
                return 'vi'
            

            return 'en'
        except:
            return 'en'
    
    def load_translations(self):
        """Load all available translations"""
        try:
            locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
            if hasattr(sys, '_MEIPASS'):
                locales_dir = os.path.join(sys._MEIPASS, 'locales')
            
            if not os.path.exists(locales_dir):
                print(f"{Fore.RED}{EMOJI['ERROR']} Locales directory not found{Style.RESET_ALL}")
                return

            for file in os.listdir(locales_dir):
                if file.endswith('.json'):
                    lang_code = file[:-5]  # Remove .json
                    try:
                        with open(os.path.join(locales_dir, file), 'r', encoding='utf-8') as f:
                            self.translations[lang_code] = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        print(f"{Fore.RED}{EMOJI['ERROR']} Error loading {file}: {e}{Style.RESET_ALL}")
                        continue
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to load translations: {e}{Style.RESET_ALL}")
    
    def get(self, key, **kwargs):
        """Get translated text with fallback support"""
        try:
            # Try current language
            result = self._get_translation(self.current_language, key)
            if result == key and self.current_language != self.fallback_language:
                # Try fallback language if translation not found
                result = self._get_translation(self.fallback_language, key)
            return result.format(**kwargs) if kwargs else result
        except Exception:
            return key
    
    def _get_translation(self, lang_code, key):
        """Get translation for a specific language"""
        try:
            keys = key.split('.')
            value = self.translations.get(lang_code, {})
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, key)
                else:
                    return key
            return value
        except Exception:
            return key
    
    def set_language(self, lang_code):
        """Set current language with validation"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())

# Create translator instance
translator = Translator()

def print_menu():
    """Print menu options"""
    print(f"\n{Fore.CYAN}{EMOJI['MENU']} {translator.get('menu.title')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}0{Style.RESET_ALL}. {EMOJI['ERROR']} {translator.get('menu.exit')}")
    print(f"{Fore.GREEN}1{Style.RESET_ALL}. {EMOJI['RESET']} {translator.get('menu.reset')}")
    print(f"{Fore.GREEN}2{Style.RESET_ALL}. {EMOJI['LIFETIME']} {translator.get('menu.delete_and_register')}")
    print(f"{Fore.GREEN}3{Style.RESET_ALL}. 🌟 {translator.get('menu.register_google')}")
    print(f"{Fore.YELLOW}   ┗━━ 🔥 {translator.get('menu.lifetime_access_enabled')} 🔥{Style.RESET_ALL}")
    print(f"{Fore.GREEN}4{Style.RESET_ALL}. ⭐ {translator.get('menu.register_github')}")
    print(f"{Fore.YELLOW}   ┗━━ 🚀 {translator.get('menu.lifetime_access_enabled')} 🚀{Style.RESET_ALL}")
    print(f"{Fore.GREEN}5{Style.RESET_ALL}. {EMOJI['SUCCESS']} {translator.get('menu.register_manual')}")
    print(f"{Fore.GREEN}6{Style.RESET_ALL}. {EMOJI['ERROR']} {translator.get('menu.quit')}")
    print(f"{Fore.GREEN}7{Style.RESET_ALL}. {EMOJI['LANG']} {translator.get('menu.select_language')}")
    print(f"{Fore.GREEN}8{Style.RESET_ALL}. {EMOJI['UPDATE']} {translator.get('menu.disable_auto_update')}")
    print(f"{Fore.GREEN}9{Style.RESET_ALL}. {EMOJI['RESET']} {translator.get('menu.totally_reset')}")
    print(f"{Fore.GREEN}10{Style.RESET_ALL}. {EMOJI['GROUP']} {translator.get('menu.join_group')}")
    print(f"{Fore.GREEN}11{Style.RESET_ALL}. {EMOJI['DELETE']} {translator.get('menu.delete_account_online')}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")

def select_language():
    """Language selection menu"""
    print(f"\n{Fore.CYAN}{EMOJI['LANG']} {translator.get('menu.select_language')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")
    
    languages = translator.get_available_languages()
    for i, lang in enumerate(languages):
        lang_name = translator.get(f"languages.{lang}")
        print(f"{Fore.GREEN}{i}{Style.RESET_ALL}. {lang_name}")
    
    try:
        choice = input(f"\n{EMOJI['ARROW']} {Fore.CYAN}{translator.get('menu.input_choice', choices=f'0-{len(languages)-1}')}: {Style.RESET_ALL}")
        if choice.isdigit() and 0 <= int(choice) < len(languages):
            translator.set_language(languages[int(choice)])
            return True
        else:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
            return False
    except (ValueError, IndexError):
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
        return False

def check_latest_version(force_update=True):
    """Check if current version matches the latest release version and update automatically if needed"""
    try:
        print(f"\n{Fore.CYAN}{EMOJI['UPDATE']} {translator.get('updater.checking')}{Style.RESET_ALL}")
        
        # Get latest version from GitHub API with timeout and proper headers
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'CursorVIP-Updater'
        }
        response = requests.get(
            "https://api.github.com/repos/suinian0309/CursorVip/releases/latest",        
            headers=headers,
            timeout=10
        )
        
        # Check if response is successful
        if response.status_code != 200:
            raise Exception(f"GitHub API returned status code {response.status_code}")
            
        response_data = response.json()
        if "tag_name" not in response_data:
            raise Exception("No version tag found in GitHub response")
            
        latest_version = response_data["tag_name"].lstrip('v')
        
        # Validate version format
        if not latest_version:
            raise Exception("Invalid version format received")
        
        # Parse versions for proper comparison
        def parse_version(version_str):
            """Parse version string into tuple for proper comparison"""
            try:
                return tuple(map(int, version_str.split('.')))
            except ValueError:
                # Fallback to string comparison if parsing fails
                return version_str
                
        current_version_tuple = parse_version(version)
        latest_version_tuple = parse_version(latest_version)
        
        # Compare versions properly
        is_newer_version_available = False
        if isinstance(current_version_tuple, tuple) and isinstance(latest_version_tuple, tuple):
            is_newer_version_available = current_version_tuple < latest_version_tuple
        else:
            # Fallback to string comparison
            is_newer_version_available = version != latest_version
        
        if is_newer_version_available:
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.new_version_available', current=version, latest=latest_version)}{Style.RESET_ALL}")
            
            # Force update without asking user
            print(f"\n{Fore.GREEN}{EMOJI['UPDATE']} {translator.get('updater.auto_updating')}{Style.RESET_ALL}")
            
            try:
                # Create progress bar
                print(f"{Fore.CYAN}{translator.get('updater.preparing_download')}{Style.RESET_ALL}")
                
                # Execute update command based on platform
                if platform.system() == 'Windows':
                    update_command = 'irm https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/install.ps1 | iex'
                    print(f"{Fore.CYAN}{translator.get('updater.downloading')}{Style.RESET_ALL}")
                    
                    # Create a dynamic progress bar
                    for i in range(10):
                        progress = "■" * i + "□" * (10 - i)
                        sys.stdout.write(f"\r{Fore.CYAN}{translator.get('updater.download_progress', progress=progress, percent=i*10)}%{Style.RESET_ALL}")
                        sys.stdout.flush()
                        time.sleep(0.3)
                    print(f"\r{Fore.CYAN}{translator.get('updater.download_progress', progress='■■■■■■■■■■', percent=100)}%{Style.RESET_ALL}")
                    
                    print(f"{Fore.CYAN}{translator.get('updater.installing')}{Style.RESET_ALL}")
                    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', update_command], check=True)
                else:
                    # For Linux/Mac, download and execute the install script
                    install_script_url = 'https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/install.sh' 
                    
                    # First verify the script exists
                    script_response = requests.get(install_script_url, timeout=5)
                    if script_response.status_code != 200:
                        raise Exception("Installation script not found")
                    
                    print(f"{Fore.CYAN}{translator.get('updater.downloading')}{Style.RESET_ALL}")
                    
                    # Create a dynamic progress bar
                    for i in range(10):
                        progress = "■" * i + "□" * (10 - i)
                        sys.stdout.write(f"\r{Fore.CYAN}{translator.get('updater.download_progress', progress=progress, percent=i*10)}%{Style.RESET_ALL}")
                        sys.stdout.flush()
                        time.sleep(0.3)
                    print(f"\r{Fore.CYAN}{translator.get('updater.download_progress', progress='■■■■■■■■■■', percent=100)}%{Style.RESET_ALL}")
                    
                    print(f"{Fore.CYAN}{translator.get('updater.installing')}{Style.RESET_ALL}")
                    
                    # Save and execute the script
                    with open('install.sh', 'wb') as f:
                        f.write(script_response.content)
                    
                    os.chmod('install.sh', 0o755)  # Make executable
                    subprocess.run(['./install.sh'], check=True)
                    
                    # Clean up
                    if os.path.exists('install.sh'):
                        os.remove('install.sh')
                
                print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.updating')}{Style.RESET_ALL}")
                sys.exit(0)
                
            except Exception as update_error:
                print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.update_failed', error=str(update_error))}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.recovery_attempt')}{Style.RESET_ALL}")
                
                # Try a recovery method
                try:
                    recovery_successful = False
                    
                    # Check if there's a cached installer and try to run it directly
                    if platform.system() == 'Windows':
                        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
                        cached_installer = os.path.join(downloads_path, f"CursorVIP_{latest_version}_windows.exe")
                        
                        if os.path.exists(cached_installer):
                            print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('updater.found_cached_installer')}{Style.RESET_ALL}")
                            subprocess.Popen(cached_installer)
                            recovery_successful = True
                            sys.exit(0)
                    
                    if not recovery_successful:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.manual_update_required')}{Style.RESET_ALL}")
                        return
                        
                except Exception as recovery_error:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.recovery_failed', error=str(recovery_error))}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.manual_update_required')}{Style.RESET_ALL}")
                    return
        else:
            # If current version is newer or equal to latest version
            if current_version_tuple > latest_version_tuple:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.development_version', current=version, latest=latest_version)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.up_to_date')}{Style.RESET_ALL}")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.network_error', error=str(e))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.continue_anyway')}{Style.RESET_ALL}")
        return
        
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.check_failed', error=str(e))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.continue_anyway')}{Style.RESET_ALL}")
        return

def check_and_remove_old_versions():
    """Check for and remove old versions of the application in the same directory"""
    try:
        # Get current executable path
        if getattr(sys, 'frozen', False):
            # Running as executable
            current_exe_path = sys.executable
        else:
            # Running in development mode, use a placeholder
            current_exe_path = os.path.abspath(__file__)
            print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.dev_mode_no_uninstall')}{Style.RESET_ALL}")
            return False
            
        # Extract current version from filename
        current_filename = os.path.basename(current_exe_path)
        if 'CursorVIP_' not in current_filename:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.non_standard_filename')}{Style.RESET_ALL}")
            return False
            
        # Notify user about automatic uninstallation
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('updater.old_version_cleanup')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{translator.get('updater.uninstall_countdown')}{Style.RESET_ALL}")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"{Fore.YELLOW}{translator.get('updater.countdown_timer', seconds=i)}{Style.RESET_ALL}")
            time.sleep(1)
            
        # Get current directory
        current_dir = os.path.dirname(current_exe_path)
        current_version = version  # Use global version
        
        # List of files that cannot be deleted immediately
        delayed_delete_files = []
        
        # Scan for old versions in the same directory
        old_versions_found = False
        for filename in os.listdir(current_dir):
            if filename.startswith("CursorVIP_") and filename.endswith(".exe") and filename != os.path.basename(current_exe_path):
                old_versions_found = True
                try:
                    file_path = os.path.join(current_dir, filename)
                    print(f"{Fore.CYAN}{EMOJI['DELETE']} {translator.get('updater.removing_file', file=filename)}{Style.RESET_ALL}")
                    os.remove(file_path)
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.file_removed')}{Style.RESET_ALL}")
                except PermissionError:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.file_in_use', file=filename)}{Style.RESET_ALL}")
                    delayed_delete_files.append(file_path)
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.remove_failed', file=filename, error=str(e))}{Style.RESET_ALL}")
        
        # Create bat script for delayed deletion if there are files that couldn't be deleted
        if delayed_delete_files:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('updater.creating_delayed_delete')}{Style.RESET_ALL}")
            
            # Create a batch file for Windows to delete files after reboot
            if platform.system() == 'Windows':
                bat_path = os.path.join(current_dir, "cleanup_old_versions.bat")
                
                with open(bat_path, 'w') as f:
                    f.write('@echo off\n')
                    f.write('echo Cleaning up old CursorVIP versions...\n')
                    f.write(':check\n')
                    
                    for file_path in delayed_delete_files:
                        f.write(f'del /f /q "{file_path}"\n')
                        f.write(f'if exist "{file_path}" (\n')
                        f.write('  echo Waiting for files to be released...\n')
                        f.write('  timeout /t 2\n')
                        f.write('  goto check\n')
                        f.write(')\n')
                        
                    f.write('echo Cleanup completed.\n')
                    f.write(f'del /f /q "{bat_path}"\n')
                
                # Make the batch file run on startup
                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                if os.path.exists(startup_folder):
                    try:
                        # Create a shortcut to the batch file
                        import win32com.client
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut_path = os.path.join(startup_folder, "CursorVIP_Cleanup.lnk")
                        shortcut = shell.CreateShortCut(shortcut_path)
                        shortcut.Targetpath = bat_path
                        shortcut.WorkingDirectory = current_dir
                        shortcut.WindowStyle = 7  # Minimized
                        shortcut.save()
                        
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.delayed_delete_created')}{Style.RESET_ALL}")
                    except Exception as sc_error:
                        # If creating the shortcut fails, try direct file copy
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.using_alternative_method')}{Style.RESET_ALL}")
                        try:
                            shutil.copy(bat_path, os.path.join(startup_folder, os.path.basename(bat_path)))
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.alternative_method_success')}{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.delayed_delete_failed', error=str(e))}{Style.RESET_ALL}")
            else:
                # For Unix-based systems
                sh_path = os.path.join(current_dir, "cleanup_old_versions.sh")
                
                with open(sh_path, 'w') as f:
                    f.write('#!/bin/bash\n')
                    f.write('echo "Cleaning up old CursorVIP versions..."\n')
                    
                    for file_path in delayed_delete_files:
                        f.write(f'while [ -f "{file_path}" ]; do\n')
                        f.write(f'  rm -f "{file_path}"\n')
                        f.write('  if [ -f "{file_path}" ]; then\n')
                        f.write('    echo "Waiting for files to be released..."\n')
                        f.write('    sleep 2\n')
                        f.write('  fi\n')
                        f.write('done\n')
                        
                    f.write('echo "Cleanup completed."\n')
                    f.write(f'rm -f "{sh_path}"\n')
                
                # Make executable
                os.chmod(sh_path, 0o755)
                
                # Try to add to user's crontab if possible
                try:
                    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('updater.adding_to_startup')}{Style.RESET_ALL}")
                    if platform.system() == "Darwin":  # macOS
                        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.cursorvip.cleanup.plist")
                        with open(plist_path, 'w') as f:
                            f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cursorvip.cleanup</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sh_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>''')
                        subprocess.run(['launchctl', 'load', plist_path])
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.startup_task_created')}{Style.RESET_ALL}")
                    else:  # Linux
                        # Get the current user's crontab
                        crontab_content = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
                        # Add our script to run at startup
                        if sh_path not in crontab_content:
                            new_crontab = crontab_content + f"\n@reboot {sh_path}\n"
                            # Write to a temporary file
                            temp_file = os.path.join(current_dir, "temp_crontab")
                            with open(temp_file, 'w') as f:
                                f.write(new_crontab)
                            # Install the new crontab
                            subprocess.run(['crontab', temp_file])
                            # Remove the temporary file
                            os.remove(temp_file)
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.startup_task_created')}{Style.RESET_ALL}")
                except Exception as cron_error:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.manual_cleanup_needed')}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('updater.cleanup_script_location', path=sh_path)}{Style.RESET_ALL}")
        
        if not old_versions_found:
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('updater.no_old_versions')}{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('updater.cleanup_error', error=str(e))}{Style.RESET_ALL}")
        return False

def main():
    # Check for admin privileges if running as executable on Windows only
    if platform.system() == 'Windows' and is_frozen() and not is_admin():
        print(f"{Fore.YELLOW}{EMOJI['ADMIN']} Running as executable, administrator privileges required.{Style.RESET_ALL}")
        if run_as_admin():
            sys.exit(0)  # Exit after requesting admin privileges
        else:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Continuing without administrator privileges.{Style.RESET_ALL}")
    
    print_logo()
    
    # Check if this is first run after update
    is_first_run = False
    first_run_marker = ".first_run"
    if os.path.exists(first_run_marker):
        is_first_run = True
        try:
            os.remove(first_run_marker)
        except:
            pass
    else:
        # Create first run marker for next time
        try:
            with open(first_run_marker, 'w') as f:
                f.write("1")
        except:
            pass
    
    # Initialize configuration
    config = get_config(translator)
    if not config:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.config_init_failed')}{Style.RESET_ALL}")
        return
    
    # If this is first run after update, check for old versions
    if is_first_run:
        check_and_remove_old_versions()
    
    # Force check latest version
    check_latest_version(force_update=True)
    
    # Print menu and continue with normal operation
    print_menu()
    
    while True:
        try:
            choice = input(f"\n{EMOJI['ARROW']} {Fore.CYAN}{translator.get('menu.input_choice', choices='0-11')}: {Style.RESET_ALL}")

            if choice == "0":
                print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('menu.exit')}...{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
                return
            elif choice == "1":
                import reset_machine_manual
                reset_machine_manual.run(translator)
                print_menu()
            elif choice == "2":
                import delete_account
                delete_account.run(translator)
                print_menu()
            elif choice == "3":
                import cursor_register_google
                cursor_register_google.main(translator)
                print_menu()
            elif choice == "4":
                import cursor_register_github
                cursor_register_github.main(translator)
                print_menu()
            elif choice == "5":
                import cursor_register_manual
                cursor_register_manual.main(translator)
                print_menu()
            elif choice == "6":
                import quit_cursor
                quit_cursor.quit_cursor(translator)
                print_menu()
            elif choice == "7":
                if select_language():
                    print_menu()
                continue
            elif choice == "8":
                import disable_auto_update
                disable_auto_update.run(translator)
                print_menu()
            elif choice == "9":
                import totally_reset_cursor
                totally_reset_cursor.run(translator)
                print_menu()
            elif choice == "10":
                import show_wechat_group
                show_wechat_group.show(translator)
                print_menu()
            elif choice == "11":
                import cursor_delete_account
                cursor_delete_account.run(translator)
                print_menu()
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
                print_menu()

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('menu.program_terminated')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
            return
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.error_occurred', error=str(e))}{Style.RESET_ALL}")
            print_menu()

if __name__ == "__main__":
    main()