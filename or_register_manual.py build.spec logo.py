warning: in the working copy of 'cursor_register_manual.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/cursor_register_manual.py b/cursor_register_manual.py[m
[1mindex 353958b..35718c8 100644[m
[1m--- a/cursor_register_manual.py[m
[1m+++ b/cursor_register_manual.py[m
[36m@@ -253,13 +253,19 @@[m [mclass CursorRegistration:[m
         auth_manager = CursorAuth(translator=self.translator)[m
         return auth_manager.update_auth(email, access_token, refresh_token)[m
 [m
[31m-def main(translator=None):[m
[32m+[m[32mdef main(translator=None, email=None, password=None):[m
     """Main function to be called from main.py"""[m
     print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
     print(f"{Fore.CYAN}{EMOJI['START']} {translator.get('register.title')}{Style.RESET_ALL}")[m
     print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
 [m
     registration = CursorRegistration(translator)[m
[32m+[m[41m    [m
[32m+[m[32m    # 如果提供了邮箱和密码，则直接使用[m
[32m+[m[32m    if email and password:[m
[32m+[m[32m        registration.email_address = email[m
[32m+[m[32m        registration.password = password[m
[32m+[m[41m    [m
     registration.start()[m
 [m
     print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
[1mdiff --git a/delete_account.py b/delete_account.py[m
[1mindex 7fb7b09..0ed9f8b 100644[m
[1m--- a/delete_account.py[m
[1m+++ b/delete_account.py[m
[36m@@ -150,6 +150,33 @@[m [mdef run(translator=None):[m
     print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account.warning')}{Style.RESET_ALL}")[m
     print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account.warning_details')}{Style.RESET_ALL}")[m
     [m
[32m+[m[32m    # 获取当前认证信息[m
[32m+[m[32m    auth_manager = CursorAuth(translator=translator)[m
[32m+[m[32m    current_auth = auth_manager.get_auth()[m
[32m+[m[32m    current_email = current_auth.get('email') if current_auth else None[m
[32m+[m[41m    [m
[32m+[m[32m    # 要求用户输入邮箱[m
[32m+[m[32m    print(f"\n{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.email_input_prompt')}{Style.RESET_ALL}")[m
[32m+[m[32m    if current_email:[m
[32m+[m[32m        print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.current_email')}: {current_email}{Style.RESET_ALL}")[m
[32m+[m[41m    [m
[32m+[m[32m    email_input = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.enter_email')}: {Style.RESET_ALL}").strip()[m
[32m+[m[41m    [m
[32m+[m[32m    # 检查输入是否为空[m
[32m+[m[32m    if not email_input:[m
[32m+[m[32m        print(f"\n{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.email_empty')}{Style.RESET_ALL}")[m
[32m+[m[32m        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
[32m+[m[32m        input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")[m
[32m+[m[32m        return[m
[32m+[m[41m    [m
[32m+[m[32m    # 检查输入的邮箱与当前邮箱是否匹配[m
[32m+[m[32m    if current_email and current_email.lower() != email_input.lower():[m
[32m+[m[32m        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.email_mismatch')}{Style.RESET_ALL}")[m
[32m+[m[32m        print(f"{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('delete_account.login_with_correct_email')}{Style.RESET_ALL}")[m
[32m+[m[32m        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
[32m+[m[32m        input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")[m
[32m+[m[32m        return[m
[32m+[m[41m    [m
     # 确认是否继续[m
     choice = input(f"\n{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.confirm', choices='Y/n')}: {Style.RESET_ALL}").lower()[m
     if choice not in ['', 'y', 'yes']:[m
[36m@@ -167,8 +194,29 @@[m [mdef run(translator=None):[m
         [m
         if choice in ['', 'y', 'yes']:[m
             print(f"\n{Fore.CYAN}{EMOJI['START']} {translator.get('delete_account.starting_registration')}{Style.RESET_ALL}")[m
[31m-            # 调用注册功能[m
[31m-            cursor_register_manual.main(translator)[m
[32m+[m[41m            [m
[32m+[m[32m            # 询问是否使用刚才的邮箱[m
[32m+[m[32m            print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.use_previous_email_prompt', email=email_input)}{Style.RESET_ALL}")[m
[32m+[m[32m            use_previous_email = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.use_previous_email', choices='Y/n')}: {Style.RESET_ALL}").lower()[m
[32m+[m[41m            [m
[32m+[m[32m            if use_previous_email in ['', 'y', 'yes']:[m
[32m+[m[32m                # 请求用户输入密码[m
[32m+[m[32m                print(f"{Fore.CYAN}{EMOJI['INFO']} {translator.get('delete_account.enter_password_prompt')}{Style.RESET_ALL}")[m
[32m+[m[32m                password = input(f"{EMOJI['INFO']} {Fore.CYAN}{translator.get('delete_account.password')}: {Style.RESET_ALL}").strip()[m
[32m+[m[41m                [m
[32m+[m[32m                # 检查密码是否为空或太短[m
[32m+[m[32m                if not password or len(password) < 8:[m
[32m+[m[32m                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('delete_account.password_too_short')}{Style.RESET_ALL}")[m
[32m+[m[32m                    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")[m
[32m+[m[32m                    input(f"{EMOJI['INFO']} {translator.get('delete_account.press_enter')}...")[m
[32m+[m[32m                    return[m
[32m+[m[41m                [m
[32m+[m[32m                # 调用注册功能，传递邮箱和密码[m
[32m+[m[32m                import cursor_register_manual[m
[32m+[m[32m                cursor_register_manual.main(translator, email=email_input, password=password)[m
[32m+[m[32m            else:[m
[32m+[m[32m                # 使用原始注册流程[m
[32m+[m[32m                cursor_register_manual.main(translator)[m
         else:[m
             print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('delete_account.registration_skipped')}{Style.RESET_ALL}")[m
     [m
