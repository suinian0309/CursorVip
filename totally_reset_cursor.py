import os
import shutil
import platform
import time
import sys
import glob
import json
import uuid
import random
import string
import re
from datetime import datetime
import subprocess
from colorama import Fore, Style, init
from main import translator
from main import EMOJI

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
    "STOP": "🛑",
    "DISCLAIMER": "⚠️",
    "WARNING": "⚠️"
}

def display_banner():
    """Displays a stylized banner for the tool."""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['STOP']} {translator.get('totally_reset.title')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

def display_features():
    """Displays the features of the Cursor AI Reset Tool."""
    print(f"\n{Fore.CYAN}{EMOJI['MENU']} {translator.get('totally_reset.feature_title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_1')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_2')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_3')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_4')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_5')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_6')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_7')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_8')} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.feature_9')} {Style.RESET_ALL}\n")

def display_disclaimer():
    """Displays a disclaimer for the user."""
    print(f"\n{Fore.RED}{EMOJI['DISCLAIMER']}  {translator.get('totally_reset.disclaimer_title')}{Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_1')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_2')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_3')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_4')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_5')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_6')} {Style.RESET_ALL}")
    print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.disclaimer_7')} {Style.RESET_ALL} \n")

def get_confirmation():
    """Gets confirmation from the user to proceed."""
    while True:
        choice = input(f"{Fore.RED}{EMOJI['WARNING']}  {translator.get('totally_reset.confirm_title')} (Y/n): ").strip().lower()
        if choice == "y" or choice == "":
            return True
        elif choice == "n":
            return False
        else:
            print(f"{EMOJI['ERROR']} {translator.get('totally_reset.invalid_choice')}")

def remove_dir(path):
    """Removes a directory if it exists and logs the action."""
    # Safety check to ensure we're only deleting Cursor-related directories
    if not is_cursor_related(path):
        print(f"{Fore.RED}{EMOJI['WARNING']} {translator.get('totally_reset.skipped_for_safety', path=path)} {Style.RESET_ALL}")
        return
        
    if os.path.exists(path):
        try:
            shutil.rmtree(path, ignore_errors=True)
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.deleted', path=path)} {Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.error_deleting', path=path, error=str(e))} {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.not_found', path=path)} {Style.RESET_ALL}")

def remove_file(path):
    """Removes a file if it exists and logs the action."""
    # Safety check to ensure we're only deleting Cursor-related files
    if not is_cursor_related(path):
        print(f"{Fore.RED}{EMOJI['WARNING']} {translator.get('totally_reset.skipped_for_safety', path=path)} {Style.RESET_ALL}")
        return
        
    if os.path.isfile(path):
        try:
            os.remove(path)
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.deleted', path=path)} {Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.error_deleting', path=path, error=str(e))} {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.not_found', path=path)} {Style.RESET_ALL}")

def is_cursor_related(path):
    """
    Safety function to verify a path is related to Cursor before deletion.
    Returns True if the path appears to be related to Cursor AI.
    """
    # Skip .vscode check as it's shared with VS Code
    if path.endswith(".vscode"):
        return False
        
    # Check if path contains cursor-related terms
    cursor_terms = ["cursor", "cursorai", "cursor-electron"]
    
    # Convert path to lowercase for case-insensitive matching
    lower_path = path.lower()
    
    # Return True if any cursor term is present in the path
    for term in cursor_terms:
        if term in lower_path:
            return True
            
    # Check specific known Cursor file patterns
    cursor_patterns = [
        r"\.cursor_.*$",
        r"cursor-.*\.json$",
        r"cursor_.*\.json$",
        r"cursor-machine-id$",
        r"trial_info\.json$",
        r"license\.json$"
    ]
    
    for pattern in cursor_patterns:
        if re.search(pattern, lower_path):
            return True
            
    # If it's a specific file that we know is only for Cursor
    if os.path.basename(lower_path) in [
        "cursor_trial_data", 
        "cursor-state.json", 
        "cursor-machine-id", 
        "ai-settings.json",
        "cursor.desktop"
    ]:
        return True
        
    return False

def find_cursor_license_files(base_path, pattern):
    """Finds files matching a pattern that might contain license information."""
    try:
        matches = []
        for root, dirnames, filenames in os.walk(base_path):
            for filename in filenames:
                # Check if filename matches any pattern before adding to matches
                if any(p.lower() in filename.lower() for p in pattern):
                    full_path = os.path.join(root, filename)
                    # Extra safety check to ensure it's cursor-related
                    if is_cursor_related(full_path):
                        matches.append(full_path)
        return matches
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.error_searching', path=base_path, error=str(e))} {Style.RESET_ALL}")
        return []

def generate_new_machine_id():
    """Generates a new random machine ID."""
    return str(uuid.uuid4())

def create_fake_machine_id(path):
    """Creates a new machine ID file with random ID."""
    if not is_cursor_related(path):
        return
        
    try:
        new_id = generate_new_machine_id()
        directory = os.path.dirname(path)
        
        # Ensure directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w') as f:
            f.write(new_id)
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.created_machine_id', path=path)} {Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.error_creating_machine_id', path=path, error=str(e))} {Style.RESET_ALL}")

def reset_machine_id(system, home):
    """Resets machine ID in all possible locations."""
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.resetting_machine_id')} {Style.RESET_ALL}")
    
    # Common machine ID locations based on OS
    if system == "Windows":
        machine_id_paths = [
            os.path.join(home, "AppData", "Roaming", "Cursor", "cursor-machine-id"),
            os.path.join(home, "AppData", "Local", "Cursor", "cursor-machine-id"),
            os.path.join(home, "AppData", "Roaming", "cursor-electron", "cursor-machine-id"),
            os.path.join(home, "AppData", "Local", "cursor-electron", "cursor-machine-id"),
            os.path.join(home, ".cursor-machine-id"),
        ]
    elif system == "Darwin":  # macOS
        machine_id_paths = [
            os.path.join(home, "Library", "Application Support", "Cursor", "cursor-machine-id"),
            os.path.join(home, "Library", "Application Support", "cursor-electron", "cursor-machine-id"),
            os.path.join(home, ".cursor-machine-id"),
        ]
    elif system == "Linux":
        machine_id_paths = [
            os.path.join(home, ".config", "Cursor", "cursor-machine-id"),
            os.path.join(home, ".config", "cursor-electron", "cursor-machine-id"),
            os.path.join(home, ".cursor-machine-id"),
        ]
    
    # First remove existing machine IDs
    for path in machine_id_paths:
        remove_file(path)
    
    # Then create new randomized IDs
    for path in machine_id_paths:
        create_fake_machine_id(path)
    
    # Try to reset system machine ID if possible (with appropriate permissions)
    if system == "Windows":
        try:
            # Windows: Create a temporary VBS script to reset machine GUID
            print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.note_complete_machine_id_reset_may_require_running_as_administrator')} {Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.windows_machine_id_modification_skipped', error=str(e))} {Style.RESET_ALL}")
    
    elif system == "Linux":
        try:
            # Linux: Create a random machine-id in /etc/ (needs sudo)
            print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.note_complete_system_machine_id_reset_may_require_sudo_privileges')} {Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.linux_machine_id_modification_skipped', error=str(e))} {Style.RESET_ALL}")

def create_fake_trial_info(path, system, home):
    """Creates fake trial information to extend trial period."""
    if not is_cursor_related(path):
        return
        
    try:
        # Generate future expiry date (90 days from now)
        future_date = (datetime.now().timestamp() + (90 * 24 * 60 * 60)) * 1000  # milliseconds
        
        # Create fake trial info
        fake_trial = {
            "trialStartTimestamp": datetime.now().timestamp() * 1000,
            "trialEndTimestamp": future_date,
            "hasUsedTrial": False,
            "machineId": generate_new_machine_id()
        }
        
        directory = os.path.dirname(path)
        
        # Ensure directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w') as f:
            json.dump(fake_trial, f)
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.created_extended_trial_info', path=path)} {Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.error_creating_trial_info', path=path, error=str(e))} {Style.RESET_ALL}")

def reset_cursor():
    """Completely resets Cursor AI by removing all settings, caches, and extensions."""
    system = platform.system()
    home = os.path.expanduser("~")

    display_banner()
    display_features()
    display_disclaimer()
    
    if not get_confirmation():
        print(f"\n{Fore.CYAN}{EMOJI['STOP']} {translator.get('totally_reset.reset_cancelled')} {Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.resetting_cursor_ai_editor')} {Style.RESET_ALL}")

    # Define paths based on OS
    if system == "Windows":
        cursor_paths = [
            os.path.join(home, "AppData", "Roaming", "Cursor"),
            os.path.join(home, "AppData", "Local", "Cursor"),
            os.path.join(home, "AppData", "Roaming", "cursor-electron"),
            os.path.join(home, "AppData", "Local", "cursor-electron"),
            os.path.join(home, "AppData", "Local", "CursorAI"),
            os.path.join(home, "AppData", "Roaming", "CursorAI"),
            # os.path.join(home, ".vscode"),  # Removed to avoid affecting VS Code
            os.path.join(home, "AppData", "Local", "Temp", "Cursor"),  # Temporary data
            os.path.join(home, "AppData", "Local", "Temp", "cursor-updater"),
            os.path.join(home, "AppData", "Local", "Programs", "cursor"),
        ]
        
        # Additional locations for license/trial files on Windows
        license_search_paths = [
            os.path.join(home, "AppData", "Roaming"),
            os.path.join(home, "AppData", "Local"),
            os.path.join(home, "AppData", "LocalLow"),
        ]
        
        # Registry instructions for Windows
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.windows_registry_instructions')} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.windows_registry_instructions_2')} {Style.RESET_ALL}")

    elif system == "Darwin":  # macOS
        cursor_paths = [
            os.path.join(home, "Library", "Application Support", "Cursor"),
            os.path.join(home, "Library", "Application Support", "cursor-electron"),
            os.path.join(home, "Library", "Caches", "Cursor"),
            os.path.join(home, "Library", "Caches", "cursor-electron"),
            os.path.join(home, "Library", "Preferences", "Cursor"),
            os.path.join(home, "Library", "Preferences", "cursor-electron"),
            os.path.join(home, "Library", "Saved Application State", "com.cursor.Cursor.savedState"),
            os.path.join(home, "Library", "HTTPStorages", "com.cursor.Cursor"),
            os.path.join(home, "Library", "WebKit", "com.cursor.Cursor"),
            # os.path.join(home, ".vscode"),  # Removed to avoid affecting VS Code
            "/Applications/Cursor.app",  # Main application location
        ]
        
        # Additional locations for license/trial files on macOS
        license_search_paths = [
            os.path.join(home, "Library", "Application Support"),
            os.path.join(home, "Library", "Preferences"),
            os.path.join(home, "Library", "Caches"),
        ]

    elif system == "Linux":
        cursor_paths = [
            os.path.join(home, ".config", "Cursor"),
            os.path.join(home, ".config", "cursor-electron"),
            os.path.join(home, ".cache", "Cursor"),
            os.path.join(home, ".cache", "cursor-electron"),
            os.path.join(home, ".local", "share", "Cursor"),
            os.path.join(home, ".local", "share", "cursor-electron"),
            # os.path.join(home, ".vscode"),  # Removed to avoid affecting VS Code
            os.path.join(home, ".local", "share", "applications", "cursor.desktop"),
            os.path.join("/usr", "share", "applications", "cursor.desktop"),
            os.path.join("/opt", "Cursor"),
        ]
        
        # Additional locations for license/trial files on Linux
        license_search_paths = [
            os.path.join(home, ".config"),
            os.path.join(home, ".local", "share"),
            os.path.join(home, ".cache"),
        ]

    else:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.unsupported_os')} {Style.RESET_ALL}")
        return

    # Remove main Cursor directories
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.removing_main_cursor_directories_and_files')} {Style.RESET_ALL}")
    for path in cursor_paths:
        remove_dir(path)

    # Reset machine identifiers (this creates new ones)
    reset_machine_id(system, home)

    # Known trial/license file patterns
    file_patterns = [
        ".cursor_trial_data",
        "trial_info.json",
        "license.json",
        "cursor-license",
        "cursor_license",
        "cursor-auth",
        "cursor_auth",
        "cursor_subscription",
        "cursor-subscription",
        "cursor-state",
        "cursorstate",
        "cursorsettings",
        "cursor-settings",
        "ai-settings.json",
        "cursor-machine-id",
        "cursor_machine_id",
        "cursor-storage"
    ]

    # Direct known trial file paths
    cursor_trial_files = [
        os.path.join(home, ".cursor_trial_data"),
        os.path.join(home, ".cursor_license"),
        os.path.join(home, ".cursor-machine-id"),
        os.path.join(home, ".cursor-state.json"),
    ]

    # OS-specific known trial/license files
    if system == "Windows":
        cursor_trial_files.extend([
            os.path.join(home, "AppData", "Local", "Cursor", "trial_info.json"),
            os.path.join(home, "AppData", "Local", "Cursor", "license.json"),
            os.path.join(home, "AppData", "Roaming", "Cursor", "trial_info.json"),
            os.path.join(home, "AppData", "Roaming", "Cursor", "license.json"),
            os.path.join(home, "AppData", "Roaming", "Cursor", "cursor-machine-id"),
            os.path.join(home, "AppData", "Local", "Cursor", "cursor-machine-id"),
            os.path.join(home, "AppData", "Local", "Cursor", "ai-settings.json"),
            os.path.join(home, "AppData", "Roaming", "Cursor", "ai-settings.json"),
        ])
    elif system == "Darwin":  # macOS
        cursor_trial_files.extend([
            os.path.join(home, "Library", "Application Support", "Cursor", "trial_info.json"),
            os.path.join(home, "Library", "Application Support", "Cursor", "license.json"),
            os.path.join(home, "Library", "Preferences", "Cursor", "trial_info.json"),
            os.path.join(home, "Library", "Preferences", "Cursor", "license.json"),
            os.path.join(home, "Library", "Application Support", "Cursor", "cursor-machine-id"),
            os.path.join(home, "Library", "Application Support", "Cursor", "ai-settings.json"),
        ])
    elif system == "Linux":
        cursor_trial_files.extend([
            os.path.join(home, ".config", "Cursor", "trial_info.json"),
            os.path.join(home, ".config", "Cursor", "license.json"),
            os.path.join(home, ".local", "share", "Cursor", "trial_info.json"),
            os.path.join(home, ".local", "share", "Cursor", "license.json"),
            os.path.join(home, ".config", "Cursor", "cursor-machine-id"),
            os.path.join(home, ".config", "Cursor", "ai-settings.json"),
        ])

    # Remove known trial/license files
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.removing_known')} {Style.RESET_ALL}")
    for path in cursor_trial_files:
        remove_file(path)

    # Deep search for additional trial/license files
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.performing_deep_scan')} {Style.RESET_ALL}")
    all_found_files = []
    for base_path in license_search_paths:
        if os.path.exists(base_path):
            found_files = find_cursor_license_files(base_path, file_patterns)
            all_found_files.extend(found_files)
    
    if all_found_files:
        print(f"\n🔎 {translator.get('totally_reset.found_additional_potential_license_trial_files', count=len(all_found_files))}\n")
        for file_path in all_found_files:
            remove_file(file_path)
    else:
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.no_additional_license_trial_files_found_in_deep_scan')} {Style.RESET_ALL}")

    # Check for and remove localStorage files that might contain settings
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.checking_for_electron_localstorage_files')} {Style.RESET_ALL}")
    if system == "Windows":
        local_storage_paths = glob.glob(os.path.join(home, "AppData", "Roaming", "*cursor*", "Local Storage", "leveldb", "*"))
        local_storage_paths += glob.glob(os.path.join(home, "AppData", "Local", "*cursor*", "Local Storage", "leveldb", "*"))
    elif system == "Darwin":
        local_storage_paths = glob.glob(os.path.join(home, "Library", "Application Support", "*cursor*", "Local Storage", "leveldb", "*"))
    elif system == "Linux":
        local_storage_paths = glob.glob(os.path.join(home, ".config", "*cursor*", "Local Storage", "leveldb", "*"))
    
    for path in local_storage_paths:
        if is_cursor_related(path):
            remove_file(path)

    # Create new trial files with extended expiration
    print(f"\n{Fore.CYAN}{EMOJI['RESET']} {translator.get('totally_reset.creating_new_trial_information_with_extended_period')} {Style.RESET_ALL}")
    if system == "Windows":
        create_fake_trial_info(os.path.join(home, "AppData", "Local", "Cursor", "trial_info.json"), system, home)
        create_fake_trial_info(os.path.join(home, "AppData", "Roaming", "Cursor", "trial_info.json"), system, home)
    elif system == "Darwin":
        create_fake_trial_info(os.path.join(home, "Library", "Application Support", "Cursor", "trial_info.json"), system, home)
    elif system == "Linux":
        create_fake_trial_info(os.path.join(home, ".config", "Cursor", "trial_info.json"), system, home)

    print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.reset_log_1')}")
    print(f"   {translator.get('totally_reset.reset_log_2')}")
    print(f"   {translator.get('totally_reset.reset_log_3')}")
    
    print(f"\n{Fore.GREEN}{EMOJI['INFO']} {translator.get('totally_reset.reset_log_4')} {Style.RESET_ALL}")
    print(f"   {translator.get('totally_reset.reset_log_5')} {Style.RESET_ALL}")
    print(f"   {translator.get('totally_reset.reset_log_6')} {Style.RESET_ALL}")
    print(f"   {translator.get('totally_reset.reset_log_7')} {Style.RESET_ALL}")
    print(f"   {translator.get('totally_reset.reset_log_8')} {Style.RESET_ALL}")
    
    print(f"\n{Fore.RED}{EMOJI['INFO']} {translator.get('totally_reset.reset_log_9')} {Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        reset_cursor()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}{EMOJI['STOP']} {translator.get('totally_reset.keyboard_interrupt')} {Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.unexpected_error', error=str(e))}{Style.RESET_ALL}")
        print(f"   {translator.get('totally_reset.report_issue')}")
        sys.exit(1)

def run(translator=None):
    """Entry point for the totally reset cursor functionality when called from the main menu."""
    try:
        reset_cursor()
        input(f"\n\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.return_to_main_menu')} {Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}{EMOJI['STOP']} {translator.get('totally_reset.process_interrupted')} {Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.unexpected_error', error=str(e))}{Style.RESET_ALL}")
        print(f"   {translator.get('totally_reset.report_issue')}")
        input(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('totally_reset.press_enter_to_return_to_main_menu')} {Style.RESET_ALL}")
