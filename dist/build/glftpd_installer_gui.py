import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import paramiko
import os
import threading
import json
from pathlib import Path
import time
import random

# Import mock classes for testing
try:
    from test_mocks import MockStringVar
except ImportError:
    # Not in testing mode, ignore the import error
    pass

class GlftpdInstallerGUI:
    def __init__(self, root, testing=False):
        self.root = root
        self.testing = testing
        
        # Define modern cyberpunk colors
        self.bg_color = "#0A0A0F"  # Darker background
        self.fg_color = "#00FF9D"  # Bright cyan-green
        self.accent_color = "#00FF9D"
        self.error_color = "#FF2D55"  # Modern red
        self.success_color = "#00FF9D"
        self.warning_color = "#FFD700"  # Gold
        self.text_color = "#E0E0E0"  # Light gray for regular text
        self.highlight_color = "#00FF9D"  # For highlighting important elements
        
        # Initialize variables first
        self.init_variables()
        
        if not testing:
            # Set up the main window
            self.root.title("[GLFTPD INSTALLER]")
            self.root.geometry("900x700")  # Slightly larger window
            self.root.configure(bg=self.bg_color)
            
            # Configure modern dark theme
            self.style = ttk.Style()
            self.style.theme_use("clam")
            
            # Configure modern styles
            self.style.configure("TFrame", background=self.bg_color)
            self.style.configure("TLabel", 
                               background=self.bg_color, 
                               foreground=self.text_color,
                               font=('Consolas', 10))
            self.style.configure("TEntry", 
                               fieldbackground="#1A1A1F", 
                               foreground=self.fg_color,
                               insertcolor=self.fg_color)
            self.style.configure("TButton", 
                               background="#1A1A1F", 
                               foreground=self.fg_color,
                               font=('Consolas', 10, 'bold'))
            self.style.configure("TNotebook", 
                               background=self.bg_color,
                               tabmargins=[2, 5, 2, 0])
            self.style.configure("TNotebook.Tab", 
                               background="#1A1A1F",
                               foreground=self.text_color,
                               padding=[10, 5],
                               font=('Consolas', 10, 'bold'))
            self.style.map("TNotebook.Tab",
                          background=[("selected", self.bg_color)],
                          foreground=[("selected", self.fg_color)])
            self.style.configure("TLabelframe", 
                               background=self.bg_color,
                               foreground=self.fg_color)
            self.style.configure("TLabelframe.Label", 
                               background=self.bg_color,
                               foreground=self.fg_color,
                               font=('Consolas', 10, 'bold'))
            self.style.configure("Horizontal.TProgressbar",
                               background=self.fg_color,
                               troughcolor="#1A1A1F")
            
            # Create and set up GUI elements
            self.setup_gui()
            
            # Start matrix effect
            self.start_matrix_effect()

    def init_variables(self):
        """Initialize variables used by the GUI"""
        # SSH Connection Variables
        if self.testing:
            # Use mock variables for testing
            self.ssh_host = MockStringVar(self.root)
            self.ssh_port = MockStringVar(self.root, value="22")
            self.ssh_username = MockStringVar(self.root)
            self.ssh_password = MockStringVar(self.root)
            self.installation_status = MockStringVar(self.root, value="Not Started")
            
            # Installation Variables
            self.sitename = MockStringVar(self.root)
            self.port = MockStringVar(self.root, value="2010")
            self.device = MockStringVar(self.root, value="/dev/sda1")
            
            # Router Configuration
            self.router = MockStringVar(self.root, value="n")
            self.pasv_addr = MockStringVar(self.root, value="")
            self.pasv_ports = MockStringVar(self.root, value="6000-7000")
            
            # Channel Configuration
            self.channelnr = MockStringVar(self.root, value="2")
            self.channame1 = MockStringVar(self.root, value="#main n nopass")
            self.channame2 = MockStringVar(self.root, value="#flood y testing")
            self.announcechannels = MockStringVar(self.root, value="#main #flood")
            self.channelops = MockStringVar(self.root, value="#main")
            
            # Channel Passwords
            self.chanpass1 = MockStringVar(self.root)
            self.chanpass2 = MockStringVar(self.root)
            
            # IRC Configuration
            self.ircnickname = MockStringVar(self.root, value="l337")
            self.ircserver = MockStringVar(self.root, value="irc.example.com")
            self.ircport = MockStringVar(self.root, value="6667")
            self.ircident = MockStringVar(self.root, value="glftpd")
            self.ircrealname = MockStringVar(self.root, value="glFTPd Site Bot")
            self.ircpass = MockStringVar(self.root)
            self.ircssl = MockStringVar(self.root, value="0")
            
            # Section Configuration
            self.sections = MockStringVar(self.root, value="3")
            self.section1 = MockStringVar(self.root, value="MP3")
            self.section2 = MockStringVar(self.root, value="0DAY")
            self.section3 = MockStringVar(self.root, value="TV")
            self.sectionpath1 = MockStringVar(self.root, value="/site/MP3")
            self.sectionpath2 = MockStringVar(self.root, value="/site/0DAY")
            self.sectionpath3 = MockStringVar(self.root, value="/site/TV")
            self.section1dated = MockStringVar(self.root, value="n")
            self.section2dated = MockStringVar(self.root, value="n")
            self.section3dated = MockStringVar(self.root, value="n")
            
            # Optional Scripts Installation
            self.eur0presystem = MockStringVar(self.root, value="n")
            self.slvprebw = MockStringVar(self.root, value="n")
            self.ircadmin = MockStringVar(self.root, value="n")
            self.request = MockStringVar(self.root, value="n")
            self.trial = MockStringVar(self.root, value="n")
            self.vacation = MockStringVar(self.root, value="n")
            self.whereami = MockStringVar(self.root, value="n")
            self.precheck = MockStringVar(self.root, value="n")
            self.autonuke = MockStringVar(self.root, value="n")
            self.psxcimdb = MockStringVar(self.root, value="n")
            self.psxcimdbchan = MockStringVar(self.root, value="#main")
            self.addip = MockStringVar(self.root, value="n")
            self.top = MockStringVar(self.root, value="n")
            self.ircnick = MockStringVar(self.root, value="n")
            self.archiver = MockStringVar(self.root, value="n")
            self.section_traffic = MockStringVar(self.root, value="n")
            
            # Administrator Account
            self.admin_username = MockStringVar(self.root, value="admin")
            self.admin_password = MockStringVar(self.root, value="password")
            self.admin_ip = MockStringVar(self.root, value="*@192.168.1.*")
        else:
            # Use real Tkinter variables
            self.ssh_host = tk.StringVar(self.root)
            self.ssh_port = tk.StringVar(self.root, value="22")
            self.ssh_username = tk.StringVar(self.root)
            self.ssh_password = tk.StringVar(self.root)
            self.installation_status = tk.StringVar(self.root, value="Not Started")
            
            # Installation Variables
            self.sitename = tk.StringVar(self.root)
            self.port = tk.StringVar(self.root, value="2010")
            self.device = tk.StringVar(self.root, value="/dev/sda1")
            
            # Router Configuration
            self.router = tk.StringVar(self.root, value="n")
            self.pasv_addr = tk.StringVar(self.root, value="")
            self.pasv_ports = tk.StringVar(self.root, value="6000-7000")
            
            # Channel Configuration
            self.channelnr = tk.StringVar(self.root, value="2")
            self.channame1 = tk.StringVar(self.root, value="#main n nopass")
            self.channame2 = tk.StringVar(self.root, value="#flood y testing")
            self.announcechannels = tk.StringVar(self.root, value="#main #flood")
            self.channelops = tk.StringVar(self.root, value="#main")
            
            # Channel Passwords
            self.chanpass1 = tk.StringVar(self.root)
            self.chanpass2 = tk.StringVar(self.root)
            
            # IRC Configuration
            self.ircnickname = tk.StringVar(self.root, value="l337")
            self.ircserver = tk.StringVar(self.root, value="irc.example.com")
            self.ircport = tk.StringVar(self.root, value="6667")
            self.ircident = tk.StringVar(self.root, value="glftpd")
            self.ircrealname = tk.StringVar(self.root, value="glFTPd Site Bot")
            self.ircpass = tk.StringVar(self.root)
            self.ircssl = tk.StringVar(self.root, value="0")
            
            # Section Configuration
            self.sections = tk.StringVar(self.root, value="3")
            self.section1 = tk.StringVar(self.root, value="MP3")
            self.section2 = tk.StringVar(self.root, value="0DAY")
            self.section3 = tk.StringVar(self.root, value="TV")
            self.sectionpath1 = tk.StringVar(self.root, value="/site/MP3")
            self.sectionpath2 = tk.StringVar(self.root, value="/site/0DAY")
            self.sectionpath3 = tk.StringVar(self.root, value="/site/TV")
            self.section1dated = tk.StringVar(self.root, value="n")
            self.section2dated = tk.StringVar(self.root, value="n")
            self.section3dated = tk.StringVar(self.root, value="n")
            
            # Optional Scripts Installation
            self.eur0presystem = tk.StringVar(self.root, value="n")
            self.slvprebw = tk.StringVar(self.root, value="n")
            self.ircadmin = tk.StringVar(self.root, value="n")
            self.request = tk.StringVar(self.root, value="n")
            self.trial = tk.StringVar(self.root, value="n")
            self.vacation = tk.StringVar(self.root, value="n")
            self.whereami = tk.StringVar(self.root, value="n")
            self.precheck = tk.StringVar(self.root, value="n")
            self.autonuke = tk.StringVar(self.root, value="n")
            self.psxcimdb = tk.StringVar(self.root, value="n")
            self.psxcimdbchan = tk.StringVar(self.root, value="#main")
            self.addip = tk.StringVar(self.root, value="n")
            self.top = tk.StringVar(self.root, value="n")
            self.ircnick = tk.StringVar(self.root, value="n")
            self.archiver = tk.StringVar(self.root, value="n")
            self.section_traffic = tk.StringVar(self.root, value="n")
            
            # Administrator Account
            self.admin_username = tk.StringVar(self.root, value="admin")
            self.admin_password = tk.StringVar(self.root, value="password")
            self.admin_ip = tk.StringVar(self.root, value="*@192.168.1.*")
        
        # Progress tracking
        self.installation_running = False
        self.current_step = 0
        self.total_steps = 5
        
        # Matrix effect variables
        self.matrix_chars = "01"
        self.matrix_labels = []
        
        # SSH client
        self.ssh_client = None
        self.sftp_client = None
        
    def setup_gui(self):
        if self.testing:
            return  # Skip GUI setup in testing mode
            
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create frames
        self.connection_frame = ttk.Frame(self.notebook)
        self.installation_frame = ttk.Frame(self.notebook)
        self.log_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.connection_frame, text="[CONNECTION]")
        self.notebook.add(self.installation_frame, text="[INSTALLATION]")
        self.notebook.add(self.log_frame, text="[LOG]")
        
        # Set up connection frame
        self.setup_connection_frame()
        
        # Set up installation frame
        self.setup_installation_frame()
        
        # Set up log frame
        self.setup_log_frame()

    def start_matrix_effect(self):
        if self.testing:
            return  # Skip matrix effect in testing mode
        # Create modern matrix rain effect
        for i in range(30):  # More characters
            label = tk.Label(self.root, 
                            text="", 
                            font=('Consolas', 8), 
                            bg=self.bg_color, 
                            fg=self.accent_color)
            label.place(x=random.randint(0, 980), y=random.randint(-100, 0))
            self.matrix_labels.append(label)
        
        def update_matrix():
            for label in self.matrix_labels:
                if random.random() < 0.15:  # Slightly more frequent updates
                    # Use modern matrix characters
                    label.config(text=random.choice("01"))
                y = label.winfo_y()
                if y > 700:
                    y = -20
                    x = random.randint(0, 980)
                    label.place(x=x, y=y)
                else:
                    label.place(x=label.winfo_x(), y=y + 8)  # Slightly faster fall
            self.root.after(40, update_matrix)  # Slightly faster updates
        
        update_matrix()
        
    def setup_connection_frame(self):
        # SSH Connection Frame
        ssh_frame = ttk.LabelFrame(self.connection_frame, text="[SSH CONNECTION]", padding=10)
        ssh_frame.pack(fill='x', padx=5, pady=5)
        
        # Host
        ttk.Label(ssh_frame, text="[HOST]:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(ssh_frame, textvariable=self.ssh_host).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        # Port
        ttk.Label(ssh_frame, text="[PORT]:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(ssh_frame, textvariable=self.ssh_port).grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Username
        ttk.Label(ssh_frame, text="[USER]:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(ssh_frame, textvariable=self.ssh_username).grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        
        # Password
        ttk.Label(ssh_frame, text="[PASS]:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(ssh_frame, textvariable=self.ssh_password, show="*").grid(row=3, column=1, sticky='ew', padx=5, pady=2)
        
        # Connect Button
        connect_btn = ttk.Button(ssh_frame, text="[CONNECT]", command=self.connect_ssh)
        connect_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
    def setup_installation_frame(self):
        # Installation Options Frame with modern styling
        install_frame = ttk.LabelFrame(self.installation_frame, 
                                     text="[INSTALLATION OPTIONS]", 
                                     padding=15)
        install_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create modern scrollable frame
        canvas = tk.Canvas(install_frame, 
                          bg=self.bg_color, 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(install_frame, 
                                orient="vertical", 
                                command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add installation options with modern styling
        row = 0
        
        # Section headers with modern styling
        def add_section_header(text):
            nonlocal row
            ttk.Label(scrollable_frame, 
                     text=text, 
                     font=('Consolas', 12, 'bold'),
                     foreground=self.fg_color).grid(row=row, 
                                                 column=0, 
                                                 columnspan=2, 
                                                 pady=15)
            row += 1
        
        # Modern input field helper
        def add_input_field(label_text, variable, password=False):
            nonlocal row
            ttk.Label(scrollable_frame, 
                     text=label_text,
                     font=('Consolas', 10)).grid(row=row, 
                                              column=0, 
                                              sticky='w', 
                                              padx=5, 
                                              pady=2)
            entry = ttk.Entry(scrollable_frame, 
                             textvariable=variable,
                             show="*" if password else "")
            entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
            row += 1
        
        # Modern checkbox helper
        def add_checkbox(label_text, variable):
            nonlocal row
            frame = ttk.Frame(scrollable_frame)
            frame.grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=2)
            
            cb = ttk.Checkbutton(frame)
            cb.configure(command=lambda: variable.set("y" if variable.get() == "n" else "n"))
            # Set initial state
            cb.state(['!alternate', '!selected' if variable.get() == "n" else 'selected'])
            cb.pack(side=tk.LEFT)
            
            ttk.Label(frame, 
                     text=label_text,
                     font=('Consolas', 10)).pack(side=tk.LEFT, padx=5)
            row += 1
            return cb
        
        # Server Configuration
        add_section_header("[SERVER CONFIG]")
        add_input_field("[SITE]:", self.sitename)
        add_input_field("[FTP PORT]:", self.port)
        add_input_field("[DEVICE]:", self.device)
        
        # Router Configuration
        add_section_header("[ROUTER CONFIG]")
        add_checkbox("[BEHIND ROUTER]:", self.router)
        add_input_field("[PASSIVE ADDRESS]:", self.pasv_addr)
        add_input_field("[PASSIVE PORTS]:", self.pasv_ports)
        
        # Channel Configuration
        add_section_header("[CHANNEL CONFIG]")
        add_input_field("[CHANNELS]:", self.channelnr)
        add_input_field("[CHAN1]:", self.channame1)
        add_input_field("[CHAN1 PASS]:", self.chanpass1, True)
        add_input_field("[CHAN2]:", self.channame2)
        add_input_field("[CHAN2 PASS]:", self.chanpass2, True)
        add_input_field("[ANNOUNCE]:", self.announcechannels)
        add_input_field("[OPS]:", self.channelops)
        
        # IRC Configuration
        add_section_header("[IRC CONFIG]")
        add_input_field("[NICK]:", self.ircnickname)
        add_input_field("[IRC SERVER]:", self.ircserver)
        add_input_field("[IRC PORT]:", self.ircport)
        add_input_field("[IRC PASS]:", self.ircpass, True)
        add_input_field("[IRC SSL]:", self.ircssl)
        add_input_field("[IRC IDENT]:", self.ircident)
        add_input_field("[IRC REALNAME]:", self.ircrealname)
        
        # Section Configuration
        add_section_header("[SECTION CONFIG]")
        add_input_field("[SECTIONS]:", self.sections)
        add_input_field("[SECTION1]:", self.section1)
        add_checkbox("[SECTION1 DATED]:", self.section1dated)
        add_input_field("[SECTION1 PATH]:", self.sectionpath1)
        add_input_field("[SECTION2]:", self.section2)
        add_checkbox("[SECTION2 DATED]:", self.section2dated)
        add_input_field("[SECTION2 PATH]:", self.sectionpath2)
        add_input_field("[SECTION3]:", self.section3)
        add_checkbox("[SECTION3 DATED]:", self.section3dated)
        add_input_field("[SECTION3 PATH]:", self.sectionpath3)
        
        # Optional Scripts
        add_section_header("[OPTIONAL SCRIPTS]")
        add_checkbox("[EUR0 PRE SYSTEM]:", self.eur0presystem)
        add_checkbox("[SLV-PREBW]:", self.slvprebw)
        add_checkbox("[TUR-IRCADMIN]:", self.ircadmin)
        add_checkbox("[TUR-REQUEST]:", self.request)
        add_checkbox("[TUR-TRIAL]:", self.trial)
        add_checkbox("[TUR-VACATION]:", self.vacation)
        add_checkbox("[WHEREAMI]:", self.whereami)
        add_checkbox("[PRECHECK]:", self.precheck)
        add_checkbox("[TUR-AUTONUKE]:", self.autonuke)
        add_checkbox("[PSXC-IMDB]:", self.psxcimdb)
        add_input_field("[PSXC-IMDB CHAN]:", self.psxcimdbchan)
        add_checkbox("[TUR-ADDIP]:", self.addip)
        add_checkbox("[TOP]:", self.top)
        add_checkbox("[IRCNICK]:", self.ircnick)
        add_checkbox("[TUR-ARCHIVER]:", self.archiver)
        add_checkbox("[SECTION-TRAFFIC]:", self.section_traffic)
        
        # Administrator Account
        add_section_header("[ADMIN ACCOUNT]")
        add_input_field("[USERNAME]:", self.admin_username)
        add_input_field("[PASSWORD]:", self.admin_password, True)
        add_input_field("[IP]:", self.admin_ip)
        
        # Export Configuration Frame
        add_section_header("[EXPORT OPTIONS]")
        export_frame = ttk.Frame(scrollable_frame)
        export_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        
        export_button = ttk.Button(export_frame, 
                                 text="[EXPORT UNATTENDED CONFIG]",
                                 style="TButton",
                                 command=self.export_unattended_config)
        export_button.pack(side=tk.LEFT, padx=5)
        
        export_all_button = ttk.Button(export_frame, 
                                     text="[EXPORT OFFLINE INSTALLER]",
                                     style="TButton",
                                     command=self.export_offline_installer)
        export_all_button.pack(side=tk.RIGHT, padx=5)
        
        row += 1
        
        # Modern Install Button
        self.install_button = ttk.Button(scrollable_frame, 
                                       text="[START INSTALLATION]",
                                       style="TButton",
                                       command=self.start_installation)
        self.install_button.grid(row=row, column=0, columnspan=2, pady=15)
        
        # Pack the scrollable frame
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_log_frame(self):
        # Log Frame with modern styling
        log_frame = ttk.LabelFrame(self.log_frame, text="[INSTALLATION LOG]", padding=10)
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Progress Frame with modern styling
        progress_frame = ttk.Frame(log_frame)
        progress_frame.pack(fill='x', pady=(0, 5))
        
        # Progress Label with modern font
        self.progress_label = ttk.Label(progress_frame, 
                                       text="[READY]",
                                       font=('Consolas', 10, 'bold'))
        self.progress_label.pack(side='left', padx=5)
        
        # Modern Progress Bar
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          mode='determinate', 
                                          length=300,
                                          style="Horizontal.TProgressbar")
        self.progress_bar.pack(side='right', padx=5)
        
        # Create modern text widget for log
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=20, 
            font=('Consolas', 10),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.fg_color,
            selectbackground=self.fg_color,
            selectforeground=self.bg_color
        )
        self.log_text.pack(fill='both', expand=True)
        
        # Configure modern text tags
        self.log_text.tag_configure('timestamp', foreground="#00FF9D")
        self.log_text.tag_configure('error', foreground=self.error_color)
        self.log_text.tag_configure('success', foreground=self.success_color)
        self.log_text.tag_configure('warning', foreground=self.warning_color)
        
    def connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.ssh_client.connect(
                hostname=self.ssh_host.get(),
                port=int(self.ssh_port.get()),
                username=self.ssh_username.get(),
                password=self.ssh_password.get()
            )
            
            self.sftp_client = self.ssh_client.open_sftp()
            self.log_message("SSH connection established successfully!", 'success')
            
        except Exception as e:
            self.log_message(f"Failed to connect: {str(e)}", 'error')
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            
    def log_message(self, message, tag=None):
        if self.testing:
            return  # Skip logging in testing mode
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        
    def update_progress(self, step, message):
        if self.testing:
            return  # Skip progress update in testing mode
        self.current_step = step
        progress = (step / self.total_steps) * 100
        self.progress_bar['value'] = progress
        self.progress_label['text'] = f"[{message}]"
        self.root.update_idletasks()
        
    def start_installation(self):
        if self.testing:
            return  # Skip actual installation in testing mode
        if not self.ssh_client:
            messagebox.showerror("Error", "Please establish SSH connection first!")
            return
            
        if self.installation_running:
            return
            
        self.installation_running = True
        self.install_button['state'] = 'disabled'
        self.progress_bar['value'] = 0
        self.current_step = 0
        
        # Create installation thread
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()
        
    def run_installation(self):
        try:
            # Step 1: Create installation directory
            self.update_progress(1, "CREATING DIR")
            self.ssh_client.exec_command('mkdir -p /tmp/glftpd-installer')
            self.log_message("Created installation directory")
            
            # Step 2: Transfer installation files
            self.update_progress(2, "TRANSFERRING")
            local_path = os.path.dirname(os.path.abspath(__file__))
            remote_path = '/tmp/glftpd-installer'
            
            # Transfer main installation script
            self.sftp_client.put(os.path.join(local_path, 'install.sh'), f'{remote_path}/install.sh')
            self.log_message("Transferred installation script")
            
            # Create install.cache with current settings
            cache_content = self.generate_cache_content()
            
            # Write cache file locally and transfer it
            with open('install.cache', 'w') as f:
                f.write(cache_content)
            self.sftp_client.put('install.cache', f'{remote_path}/install.cache')
            os.remove('install.cache')
            self.log_message("Transferred configuration file")
            
            # Step 3: Make installation script executable
            self.update_progress(3, "SETTING UP")
            self.ssh_client.exec_command(f'chmod +x {remote_path}/install.sh')
            self.log_message("Made installation script executable")
            
            # Step 4: Run installation
            self.update_progress(4, "INSTALLING")
            stdin, stdout, stderr = self.ssh_client.exec_command(f'sudo -S {remote_path}/install.sh')
            stdin.write(self.ssh_password.get() + "\n")
            stdin.flush()
            
            # Read output in real-time
            for line in stdout:
                self.log_message(line.strip())
                
            # Check for errors
            errors = stderr.read().decode()
            if errors:
                self.log_message(f"Errors:\n{errors}", 'error')
                
            # Step 5: Cleanup
            self.update_progress(5, "CLEANING UP")
            self.ssh_client.exec_command(f'rm -rf {remote_path}')
            self.log_message("Installation completed successfully!", 'success')
            
            messagebox.showinfo("Success", "Installation completed!")
            
        except Exception as e:
            self.log_message(f"Error during installation: {str(e)}", 'error')
            messagebox.showerror("Error", f"Installation failed: {str(e)}")
            
        finally:
            self.installation_running = False
            self.install_button['state'] = 'normal'
            self.update_progress(0, "READY")

    def export_unattended_config(self):
        """Export the unattended installation configuration to install.cache"""
        if self.testing:
            return  # Skip in testing mode
        
        try:
            # Create a dialog to select save location
            from tkinter import filedialog
            save_path = filedialog.asksaveasfilename(
                defaultextension=".cache",
                filetypes=[("Cache files", "*.cache"), ("All files", "*.*")],
                title="Save Unattended Configuration"
            )
            
            if not save_path:
                return  # User canceled
            
            # Generate cache content
            cache_content = self.generate_cache_content()
            
            # Write cache file
            with open(save_path, 'w') as f:
                f.write(cache_content)
            
            self.log_message(f"Unattended configuration exported to {save_path}", 'success')
            
        except Exception as e:
            self.log_message(f"Error exporting configuration: {str(e)}", 'error')
            messagebox.showerror("Error", f"Failed to export configuration: {str(e)}")

    def export_offline_installer(self):
        """Export the offline installer package with install.sh and install.cache"""
        if self.testing:
            return  # Skip in testing mode
        
        try:
            # Create a dialog to select save location
            from tkinter import filedialog
            save_dir = filedialog.askdirectory(
                title="Select Directory for Offline Installer"
            )
            
            if not save_dir:
                return  # User canceled
            
            # Check if install.sh exists
            local_path = os.path.dirname(os.path.abspath(__file__))
            install_script_path = os.path.join(local_path, 'install.sh')
            
            if not os.path.exists(install_script_path):
                # If it doesn't exist locally, need to fetch it from server
                if not self.ssh_client:
                    messagebox.showerror("Error", "Please establish SSH connection first to download install.sh!")
                    return
                    
                self.log_message("Downloading install.sh from server...")
                
                # Create a temporary directory
                temp_dir = os.path.join(local_path, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                
                # Download install.sh from server
                try:
                    self.ssh_client.exec_command('mkdir -p /tmp/glftpd-installer')
                    self.sftp_client.get('/tmp/glftpd-installer/install.sh', os.path.join(temp_dir, 'install.sh'))
                    install_script_path = os.path.join(temp_dir, 'install.sh')
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to download install.sh: {str(e)}")
                    return
            
            # Generate cache content
            cache_content = self.generate_cache_content()
            
            # Create the offline installer package
            import shutil
            import zipfile
            
            # Create the zip file
            zip_path = os.path.join(save_dir, 'glftpd-offline-installer.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                # Add install.sh
                zipf.write(install_script_path, 'install.sh')
                
                # Add install.cache
                temp_cache_path = os.path.join(local_path, 'install.cache')
                with open(temp_cache_path, 'w') as f:
                    f.write(cache_content)
                zipf.write(temp_cache_path, 'install.cache')
                os.remove(temp_cache_path)
                
                # Add a README file
                readme_path = os.path.join(local_path, 'offline_readme.txt')
                with open(readme_path, 'w') as f:
                    f.write("""GLFTPD OFFLINE INSTALLER
============================

This package contains everything needed for an unattended installation of glFTPd.

Instructions:
1. Extract the contents of this zip file to the target server
2. Make install.sh executable: chmod +x install.sh
3. Run the installation as root: sudo ./install.sh

The installation will proceed unattended using the configuration in install.cache.
""")
                zipf.write(readme_path, 'README.txt')
                os.remove(readme_path)
            
            # Clean up temporary directory if it was created
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            self.log_message(f"Offline installer exported to {zip_path}", 'success')
            
        except Exception as e:
            self.log_message(f"Error exporting offline installer: {str(e)}", 'error')
            messagebox.showerror("Error", f"Failed to export offline installer: {str(e)}")

    def generate_cache_content(self):
        """Generate the content for install.cache based on current settings"""
        cache_content = f"""# GLFTPD Unattended Installation Configuration
# Generated by GLFTPD Installer GUI

sitename="{self.sitename.get()}" # Name of the site. Don't use space in sitename. 
port="{self.port.get()}" # Port for the FTP
device="{self.device.get()}" # What device to use for /site

# Router Configuration
router="{self.router.get()}" # If site is behind router
pasv_addr="{self.pasv_addr.get()}" # IP or DNS to use as passive address for glFTPd
pasv_ports="{self.pasv_ports.get()}" # Port range to use for passive mode for glFTPd

# Channel Configuration
channelnr="{self.channelnr.get()}" # How many channels the bot will be in
channame1="{self.channame1.get()}" # Channelname of 1st chan
channame2="{self.channame2.get()}" # Channelname of 2nd chan
chanpass1="{self.chanpass1.get()}" # Password for channel 1
chanpass2="{self.chanpass2.get()}" # Password for channel 2
announcechannels="{self.announcechannels.get()}" # Announce channels
channelops="{self.channelops.get()}" # Ops channel

# IRC Configuration
ircnickname="{self.ircnickname.get()}" # Irc nickname of bot owner
ircserver="{self.ircserver.get()}" # IRC server
ircport="{self.ircport.get()}" # IRC port
ircpass="{self.ircpass.get()}" # IRC password
ircssl="{self.ircssl.get()}" # IRC SSL
ircident="{self.ircident.get()}" # IRC ident
ircrealname="{self.ircrealname.get()}" # IRC realname

# Section Configuration
sections="{self.sections.get()}" # How many sections will be created, max 22 sections allowed
section1="{self.section1.get()}" # Name of section 1
section1dated="{self.section1dated.get()}" # Dated section?
section2="{self.section2.get()}" # Name of section 2
section2dated="{self.section2dated.get()}" # Dated section?
section3="{self.section3.get()}" # Name of section 3
section3dated="{self.section3dated.get()}" # Dated section?
sectionpath1="{self.sectionpath1.get()}" # Path for section 1
sectionpath2="{self.sectionpath2.get()}" # Path for section 2
sectionpath3="{self.sectionpath3.get()}" # Path for section 3

# Optional Scripts
eur0presystem="{self.eur0presystem.get()}" # Install Eur0-pre-system with foo-pre
slvprebw="{self.slvprebw.get()}" # Install Slv-PreBW
ircadmin="{self.ircadmin.get()}" # Install Tur-Ircadmin
request="{self.request.get()}" # Install Tur-Request
trial="{self.trial.get()}" # Install Tur-Trial
vacation="{self.vacation.get()}" # Install Tur-Vacation
whereami="{self.whereami.get()}" # Install Whereami
precheck="{self.precheck.get()}" # Install Precheck
autonuke="{self.autonuke.get()}" # Install Tur-Autonuke
psxcimdb="{self.psxcimdb.get()}" # Install PSXC-IMDB
psxcimdbchan="{self.psxcimdbchan.get()}" # Trigger chan for PSXC-IMDB
addip="{self.addip.get()}" # Install Tur-Addip
top="{self.top.get()}" # Install Top
ircnick="{self.ircnick.get()}" # Install Ircnick
archiver="{self.archiver.get()}" # Install Tur-Archiver
section_traffic="{self.section_traffic.get()}" # Install Section-Traffic

# Administrator Account
username="{self.admin_username.get()}" # Username for Administrator account
password="{self.admin_password.get()}" # Password for Administrator account
ip="{self.admin_ip.get()}" # IP for Administrator account
"""
        return cache_content

def main():
    root = tk.Tk()
    app = GlftpdInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
