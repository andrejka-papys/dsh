
import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path
from datetime import datetime

# Заменяем readline на кроссплатформенное решение
try:
    import readline  # Для Linux/macOS
except ImportError:
    # Для Windows используем pyreadline
    try:
        import pyreadline as readline
    except ImportError:
        # Если pyreadline не установлен, создаем заглушку
        class ReadlineStub:
            def read_history_file(self, file): pass
            def write_history_file(self, file): pass
        readline = ReadlineStub()

class DoyarkaTerminal:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.username = "doyarka"
        self.hostname = "terminal"
        self.running = True
        self.command_history = []
        
        # Настройка истории команд
        self.history_file = os.path.join(Path.home(), '.doyarka_history')
        self.load_history()
    
    def load_history(self):
        """Загрузка истории команд из файла"""
        try:
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
        except Exception:
            # Резервное сохранение/загрузка истории
            try:
                if os.path.exists(self.history_file):
                    with open(self.history_file, 'r', encoding='utf-8') as f:
                        self.command_history = [line.strip() for line in f.readlines()]
            except Exception:
                pass
    
    def save_history(self):
        """Сохранение истории команд в файл"""
        try:
            readline.write_history_file(self.history_file)
        except Exception:
            # Резервное сохранение истории
            try:
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    for cmd in self.command_history:
                        f.write(cmd + '\n')
            except Exception:
                pass
    
    def display_prompt(self):
        """Отображение приглашения командной строки"""
        path = self.current_dir
        home = str(Path.home())
        if path.startswith(home):
            path = "~" + path[len(home):]
            
        return f"\033[92m{self.username}@{self.hostname}\033[0m:\033[94m{path}\033[0m$ "
    
    def run_command(self, command):
        """Обработка и выполнение команд"""
        if not command.strip():
            return
            
        # Добавляем команду в историю
        self.command_history.append(command)
        
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        
        try:
            if cmd == "exit":
                self.running = False
                
            elif cmd == "pwd":
                print(self.current_dir)
                
            elif cmd == "ls":
                self.list_files(args)
                
            elif cmd == "cd":
                self.change_directory(args)
                
            elif cmd == "cat":
                self.cat_file(args)
                
            elif cmd == "mkdir":
                self.make_directory(args)
                
            elif cmd == "rm":
                self.remove_file(args)
                
            elif cmd == "cp":
                self.copy_file(args)
                
            elif cmd == "mv":
                self.move_file(args)
                
            elif cmd == "touch":
                self.touch_file(args)
                
            elif cmd == "echo":
                self.echo_text(args)
                
            elif cmd == "clear":
                os.system('clear' if os.name == 'posix' else 'cls')
                
            elif cmd == "whoami":
                print(self.username)
                
            elif cmd == "history":
                self.show_history()
                
            elif cmd == "find":
                self.find_files(args)
                
            elif cmd == "grep":
                self.grep_text(args)
                
            elif cmd == "neofetch":
                self.neofetch()
                
            elif cmd == "nano":
                self.nano_editor(args)
                
            elif cmd == "help":
                self.show_help()
                
            else:
                self.execute_system_command(parts)
                
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def neofetch(self):
        """Реализация neofetch - отображение системной информации"""
        system_info = {
            "OS": platform.system(),
            "Hostname": platform.node(),
            "Kernel": platform.release(),
            "Uptime": self.get_uptime(),
            "Shell": os.path.basename(os.getenv('SHELL', 'doyarka-terminal')),
            "CPU": self.get_cpu_info(),
            "Memory": self.get_memory_info(),
            "Terminal": "DoyarkaTerminal",
            "User": self.username
        }
        
        # ASCII арт логотип
        logo = [
            "╔═══════════════════╗",
            "║    DOYARKA OS     ║",
            "║    ██████╗ ██████╗║",
            "║   ██╔═══██╗╚════██║║",
            "║   ██║   ██║ █████╔╝║",
            "║   ██║   ██║██╔═══╝ ║",
            "║   ╚██████╔╝███████╗║",
            "║    ╚═════╝ ╚══════╝║",
            "╚═══════════════════╝"
        ]
        
        # Вывод информации в стиле neofetch
        print("\033[1;36m")  # Голубой цвет
        for i, line in enumerate(logo):
            if i < len(logo):
                info_line = ""
                if i == 1:
                    info_line = f"OS: {system_info['OS']}"
                elif i == 2:
                    info_line = f"Host: {system_info['Hostname']}"
                elif i == 3:
                    info_line = f"Kernel: {system_info['Kernel']}"
                elif i == 4:
                    info_line = f"Uptime: {system_info['Uptime']}"
                elif i == 5:
                    info_line = f"Shell: {system_info['Shell']}"
                elif i == 6:
                    info_line = f"CPU: {system_info['CPU']}"
                elif i == 7:
                    info_line = f"Memory: {system_info['Memory']}"
                elif i == 8:
                    info_line = f"User: {system_info['User']}"
                
                print(f"{line}    \033[0m{info_line}")
        
        print("\033[0m")  # Сброс цвета
    
    def get_uptime(self):
        """Получить время работы системы"""
        try:
            if os.name == 'posix':
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                return f"{hours}h {minutes}m"
            else:
                return "N/A"
        except:
            return "N/A"
    
    def get_cpu_info(self):
        """Получить информацию о CPU"""
        try:
            if os.name == 'posix':
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            return line.split(':')[1].strip()
            return platform.processor()
        except:
            return "Unknown"
    
    def get_memory_info(self):
        """Получить информацию о памяти"""
        try:
            if os.name == 'posix':
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            mem_kb = int(line.split()[1])
                            mem_gb = mem_kb / 1024 / 1024
                            return f"{mem_gb:.1f} GB"
            return "Unknown"
        except:
            return "Unknown"
    
    def nano_editor(self, args):
        """Простой текстовый редактор в стиле nano"""
        if not args:
            print("nano: отсутствует операнд")
            print("Использование: nano <filename>")
            return
        
        filename = args[0]
        filepath = os.path.join(self.current_dir, filename)
        
        # Проверяем, существует ли файл
        content = ""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                print(f"Ошибка: невозможно прочитать файл {filename}")
                return
        else:
            # Создаем новый файл
            try:
                open(filepath, 'w').close()
            except:
                print(f"Ошибка: невозможно создать файл {filename}")
                return
        
        print(f"\nРедактирование файла: {filename}")
        print("Команды: Ctrl+S - Сохранить, Ctrl+X - Выход, Ctrl+G - Помощь")
        print("─" * 50)
        
        # Отображаем текущее содержимое
        lines = content.split('\n') if content else [""]
        current_line = 0
        
        while True:
            # Очищаем экран и показываем содержимое
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"DOYARKA NANO - {filename}")
            print("Команды: Ctrl+S - Сохранить, Ctrl+X - Выход, Ctrl+G - Помощь")
            print("─" * 50)
            
            # Показываем содержимое вокруг текущей строки
            start = max(0, current_line - 5)
            end = min(len(lines), current_line + 10)
            
            for i in range(start, end):
                marker = ">" if i == current_line else " "
                print(f"{marker} {i+1:3d}: {lines[i]}")
            
            print("─" * 50)
            print(f"Строка {current_line + 1}/{len(lines)}")
            
            try:
                user_input = input("Введите текст или команду: ")
            except KeyboardInterrupt:
                # Обработка Ctrl+C как выхода с подтверждением
                confirm = input("\nВыйти без сохранения? (y/N): ")
                if confirm.lower() == 'y':
                    return
                continue
            
            # Обработка специальных команд
            if user_input == '\x18':  # Ctrl+X
                confirm = input("Сохранить изменения? (Y/n): ")
                if confirm.lower() != 'n':
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"Сохранено: {filename}")
                    except Exception as e:
                        print(f"Ошибка сохранения: {e}")
                return
            
            elif user_input == '\x13':  # Ctrl+S
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    print(f"Сохранено: {filename}")
                except Exception as e:
                    print(f"Ошибка сохранения: {e}")
                input("Нажмите Enter для продолжения...")
                continue
            
            elif user_input == '\x07':  # Ctrl+G
                self.show_nano_help()
                input("Нажмите Enter для продолжения...")
                continue
            
            elif user_input.startswith('/'):  # Поиск
                search_term = user_input[1:]
                found = False
                for i in range(current_line + 1, len(lines)):
                    if search_term in lines[i]:
                        current_line = i
                        found = True
                        break
                if not found:
                    print(f"Текст '{search_term}' не найден")
                    input("Нажмите Enter для продолжения...")
                continue
            
            # Навигация
            elif user_input == 'j' and current_line < len(lines) - 1:
                current_line += 1
            elif user_input == 'k' and current_line > 0:
                current_line -= 1
            elif user_input == 'g':
                current_line = 0
            elif user_input == 'G':
                current_line = len(lines) - 1
            
            # Редактирование
            elif user_input == 'i':  # Вставка
                new_text = input("Введите текст: ")
                lines[current_line] = new_text
            elif user_input == 'a':  # Добавление в конец
                append_text = input("Добавить текст: ")
                lines[current_line] += append_text
            elif user_input == 'o':  # Новая строка после
                new_line = input("Новая строка: ")
                lines.insert(current_line + 1, new_line)
                current_line += 1
            elif user_input == 'O':  # Новая строка перед
                new_line = input("Новая строка: ")
                lines.insert(current_line, new_line)
                current_line += 1
            elif user_input == 'd':  # Удалить строку
                if len(lines) > 1:
                    lines.pop(current_line)
                    if current_line >= len(lines):
                        current_line = len(lines) - 1
                else:
                    lines[current_line] = ""
            else:
                # Если введен обычный текст, заменяем текущую строку
                lines[current_line] = user_input
    
    def show_nano_help(self):
        """Показать справку по nano"""
        help_text = """
┌───────────────── НАНО РЕДАКТОР ─────────────────┐
│                 Основные команды:               │
│                                                 │
│  Ctrl+S    - Сохранить файл                     │
│  Ctrl+X    - Выйти из редактора                 │
│  Ctrl+G    - Показать эту справку               │
│                                                 │
│  i         - Редактировать текущую строку       │
│  a         - Добавить текст в конец строки      │
│  o         - Вставить строку после текущей      │
│  O         - Вставить строку перед текущей      │
│  d         - Удалить текущую строку             │
│                                                 │
│  j         - Перейти на строку вниз             │
│  k         - Перейти на строку вверх            │
│  g         - Перейти к первой строке            │
│  G         - Перейти к последней строке         │
│                                                 │
│  /текст    - Поиск текста                       │
│                                                 │
│  Enter     - Подтвердить ввод                   │
│  Ctrl+C    - Отмена/Выход                       │
└─────────────────────────────────────────────────┘
"""
        print(help_text)
    
    def list_files(self, args):
        """Реализация команды ls"""
        long_format = '-l' in args
        show_all = '-a' in args
        
        path_args = [arg for arg in args if not arg.startswith('-')]
        
        path = self.current_dir
        if path_args:
            path = os.path.join(self.current_dir, path_args[0])
            
        try:
            files = os.listdir(path)
            if not show_all:
                files = [f for f in files if not f.startswith('.')]
                
            for file in files:
                file_path = os.path.join(path, file)
                if long_format:
                    stat = os.stat(file_path)
                    size = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    permissions = self.get_permissions(file_path)
                    print(f"{permissions} {size:8d} {mtime} {file}")
                else:
                    if os.path.isdir(file_path):
                        print(f"\033[94m{file}/\033[0m")
                    elif os.access(file_path, os.X_OK):
                        print(f"\033[92m{file}\033[0m")
                    else:
                        print(file)
        except FileNotFoundError:
            print(f"ls: невозможно получить доступ к '{args[0]}': Нет такого файла или каталога")
    
    def get_permissions(self, path):
        """Получить строку прав доступа в UNIX-стиле"""
        try:
            stat = os.stat(path)
            permissions = []
            
            if os.path.isdir(path):
                permissions.append('d')
            else:
                permissions.append('-')
            
            permissions.append('r' if stat.st_mode & 0o400 else '-')
            permissions.append('w' if stat.st_mode & 0o200 else '-')
            permissions.append('x' if stat.st_mode & 0o100 else '-')
            permissions.append('r' if stat.st_mode & 0o040 else '-')
            permissions.append('w' if stat.st_mode & 0o020 else '-')
            permissions.append('x' if stat.st_mode & 0o010 else '-')
            permissions.append('r' if stat.st_mode & 0o004 else '-')
            permissions.append('w' if stat.st_mode & 0o002 else '-')
            permissions.append('x' if stat.st_mode & 0o001 else '-')
            
            return ''.join(permissions)
        except:
            return '??????????'
    
    def change_directory(self, args):
        """Реализация команды cd"""
        if not args:
            new_dir = str(Path.home())
        else:
            new_dir = args[0]
            
        if new_dir == "~":
            new_dir = str(Path.home())
        elif new_dir.startswith("~/"):
            new_dir = str(Path.home()) + new_dir[1:]
        else:
            new_dir = os.path.join(self.current_dir, new_dir)
            
        try:
            os.chdir(new_dir)
            self.current_dir = os.getcwd()
        except FileNotFoundError:
            print(f"cd: {args[0]}: Нет такого файла или каталога")
        except PermissionError:
            print(f"cd: {args[0]}: Отказано в доступе")
    
    def cat_file(self, args):
        """Реализация команды cat"""
        if not args:
            print("cat: отсутствует операнд")
            return
            
        try:
            with open(os.path.join(self.current_dir, args[0]), 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"cat: {args[0]}: Нет такого файла или каталога")
        except IsADirectoryError:
            print(f"cat: {args[0]}: Это каталог")
        except UnicodeDecodeError:
            print(f"cat: {args[0]}: Невозможно прочитать файл (возможно, бинарный)")
    
    def make_directory(self, args):
        """Реализация команды mkdir"""
        if not args:
            print("mkdir: отсутствует операнд")
            return
            
        try:
            os.makedirs(os.path.join(self.current_dir, args[0]), exist_ok=True)
        except PermissionError:
            print(f"mkdir: невозможно создать каталог '{args[0]}': Отказано в доступе")
    
    def remove_file(self, args):
        """Реализация команды rm"""
        if not args:
            print("rm: отсутствует операнд")
            return
            
        recursive = '-r' in args
        force = '-f' in args
        
        file_args = [arg for arg in args if not arg.startswith('-')]
        
        if not file_args:
            print("rm: отсутствует операнд")
            return
            
        path = os.path.join(self.current_dir, file_args[0])
        try:
            if os.path.isdir(path):
                if recursive:
                    shutil.rmtree(path)
                else:
                    print(f"rm: невозможно удалить '{file_args[0]}': Это каталог")
            else:
                os.remove(path)
        except FileNotFoundError:
            if not force:
                print(f"rm: невозможно удалить '{file_args[0]}': Нет такого файла или каталога")
        except PermissionError:
            print(f"rm: невозможно удалить '{file_args[0]}': Отказано в доступе")
    
    def copy_file(self, args):
        """Реализация команды cp"""
        if len(args) < 2:
            print("cp: отсутствует операнд")
            return
            
        src = os.path.join(self.current_dir, args[0])
        dst = os.path.join(self.current_dir, args[1])
        
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except FileNotFoundError:
            print(f"cp: невозможно выполнить stat для '{args[0]}': Нет такого файла или каталога")
    
    def move_file(self, args):
        """Реализация команды mv"""
        if len(args) < 2:
            print("mv: отсутствует операнд")
            return
            
        src = os.path.join(self.current_dir, args[0])
        dst = os.path.join(self.current_dir, args[1])
        
        try:
            shutil.move(src, dst)
        except FileNotFoundError:
            print(f"mv: невозможно выполнить stat для '{args[0]}': Нет такого файла или каталога")
    
    def touch_file(self, args):
        """Реализация команды touch"""
        if not args:
            print("touch: отсутствует операнд")
            return
            
        try:
            with open(os.path.join(self.current_dir, args[0]), 'a'):
                os.utime(os.path.join(self.current_dir, args[0]), None)
        except PermissionError:
            print(f"touch: невозможно создать файл '{args[0]}': Отказано в доступе")
    
    def echo_text(self, args):
        """Реализация команды echo"""
        print(' '.join(args))
    
    def show_history(self):
        """Показать историю команд"""
        for i, cmd in enumerate(self.command_history[-20:], 1):
            print(f"{i:4d}  {cmd}")
    
    def find_files(self, args):
        """Простая реализация команды find"""
        if len(args) < 2:
            print("Использование: find <путь> -name <шаблон>")
            return
            
        path = args[0]
        pattern = args[2] if '-name' in args else '*'
        
        try:
            for root, dirs, files in os.walk(os.path.join(self.current_dir, path)):
                for file in files:
                    if pattern in file or pattern == '*':
                        print(os.path.join(root, file))
        except FileNotFoundError:
            print(f"find: '{path}': Нет такого файла или каталога")
    
    def grep_text(self, args):
        """Простая реализация команды grep"""
        if len(args) < 2:
            print("Использование: grep <шаблон> <файл>")
            return
            
        pattern = args[0]
        filename = args[1]
        
        try:
            with open(os.path.join(self.current_dir, filename), 'r') as f:
                for i, line in enumerate(f, 1):
                    if pattern in line:
                        print(f"{filename}:{i}: {line.strip()}")
        except FileNotFoundError:
            print(f"grep: {filename}: Нет такого файла или каталога")
    
    def execute_system_command(self, parts):
        """Выполнение системных команд"""
        try:
            result = subprocess.run(parts, cwd=self.current_dir, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        except FileNotFoundError:
            print(f"{parts[0]}: команда не найдена")
    
    def show_help(self):
        """Показать справку по командам"""
        help_text = """
Доступные команды:
  ls [опции] [dir] - список файлов (опции: -l подробно, -a все файлы)
  cd [dir]         - сменить директорию
  pwd              - показать текущую директорию
  cat <file>       - показать содержимое файла
  mkdir <dir>      - создать директорию
  rm [опции] <file> - удалить файл (опции: -r рекурсивно, -f принудительно)
  cp <src> <dst>   - копировать файл/директорию
  mv <src> <dst>   - переместить файл/директорию
  touch <file>     - создать файл
  echo <text>      - вывести текст
  clear            - очистить экран
  whoami           - показать имя пользователя
  history          - показать историю команд
  find <path> -name <pattern> - найти файлы
  grep <pattern> <file> - поиск текста в файле
  neofetch         - показать информацию о системе
  nano <file>      - текстовый редактор
  exit             - выйти из терминала
  help             - показать эту справку
  
Также поддерживаются системные команды (python, pip, etc.)
"""
        print(help_text)
    
    def run(self):
        """Основной цикл терминала"""
        print("Добро пожаловать в DoyarkaTerminal!")
        print("Введите 'help' для списка команд, 'exit' для выхода\n")
        
        while self.running:
            try:
                command = input(self.display_prompt())
                self.run_command(command)
            except KeyboardInterrupt:
                print("\nИспользуйте 'exit' для выхода")
            except EOFError:
                print("\nВыход...")
                break
        
        self.save_history()

if __name__ == "__main__":
    terminal = DoyarkaTerminal()
    terminal.run()
