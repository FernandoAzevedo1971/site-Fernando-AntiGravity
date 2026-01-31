import os
import time
import threading
import queue
import datetime
import json
from pathlib import Path
from dotenv import load_dotenv
from tkinter import filedialog

import customtkinter as ctk
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tkinterdnd2 import TkinterDnD, DND_FILES

import httpx
from deepgram import DeepgramClient

# Load environment variables
load_dotenv(override=True)
print("DEBUG: Environment loaded")

# Configuration
# Allow WATCH_DIRECTORY to be configured via .env file
# Default fallback is the developer's path
WATCH_DIRECTORY = os.getenv("WATCH_DIRECTORY", r"C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free")
print(f"DEBUG: Watch directory: {WATCH_DIRECTORY}")

# Fallback if directory doesn't exist (for testing)
if not os.path.exists(WATCH_DIRECTORY):
    print(f"Warning: Directory {WATCH_DIRECTORY} does not exist. Please check the path.")

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Configuration file to store last used directory
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".audio_transcriber_config.json")

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class TranscriptionApp(Tk):
    def __init__(self):
        super().__init__()
        
        # Set light theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Audio Transcriber (Deepgram Nova-3)")
        self.geometry("800x600")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Monitor de Transcrição", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left", padx=10, pady=10)

        self.usage_label = ctk.CTkLabel(self.header_frame, text="Uso: 0 arquivos", font=ctk.CTkFont(size=11), text_color="#0066CC")
        self.usage_label.pack(side="right", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self.header_frame, text="Arraste arquivos aqui ou aguarde...", text_color="gray")
        self.status_label.pack(side="right", padx=10, pady=10)

        # Main Text Area
        self.textbox = ctk.CTkTextbox(self, width=760, height=400, font=ctk.CTkFont(size=14))
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox.insert("0.0", "O texto transcrito aparecerá aqui...\n\n")
        self.textbox.configure(state="disabled") # Read-only initially

        # Footer / Controls
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))

        self.copy_button = ctk.CTkButton(self.footer_frame, text="Copiar Texto", command=self.copy_to_clipboard)
        self.copy_button.pack(side="right", padx=10, pady=10)

        self.clear_button = ctk.CTkButton(self.footer_frame, text="Limpar", fg_color="gray", command=self.clear_text)
        self.clear_button.pack(side="left", padx=10, pady=10)
        
        self.select_file_button = ctk.CTkButton(self.footer_frame, text="Selecionar Arquivo", fg_color="#0066CC", command=self.select_file)
        self.select_file_button.pack(side="left", padx=10, pady=10)
        
        self.select_files_button = ctk.CTkButton(self.footer_frame, text="Selecionar Arquivos da Pasta", fg_color="#0066CC", command=self.select_multiple_files)
        self.select_files_button.pack(side="left", padx=10, pady=10)

        # Queue for thread communication
        self.queue = queue.Queue()
        
        # Usage tracking
        self.processed_files_count = 0
        self.total_audio_minutes = 0.0
        
        # Load last used directory
        self.last_directory = self.load_last_directory()

        # Drag and Drop Setup
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)
        
        # Deepgram Client with extended timeout for large files
        # Default is 60 seconds, but large files (100+ MB) need more time for upload
        # Custom timeouts: 15 min for write (upload), 10 min for read (processing)
        # This allows files up to 200MB to be uploaded and processed
        timeout_config = httpx.Timeout(
            timeout=600.0,      # Total timeout: 10 minutes
            connect=30.0,       # Connection timeout: 30 seconds
            read=600.0,         # Read timeout: 10 minutes
            write=900.0,        # Write timeout: 15 minutes (for large file uploads)
            pool=None
        )
        self.deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY, timeout=timeout_config)

        # Start checking queue
        self.after(100, self.check_queue)

        # Start Monitor
        self.start_monitor()
        
        # Try to update balance display (will fallback to usage counter if no permissions)
        self.after(2000, self.try_update_balance)

    def start_monitor(self):
        if not DEEPGRAM_API_KEY:
             self.update_status("ERRO: API Key não encontrada no .env", error=True)
             return

        if not os.path.exists(WATCH_DIRECTORY):
             self.update_status(f"ERRO: Pasta não encontrada: {WATCH_DIRECTORY}", error=True)
             return

        self.event_handler = AudioFileHandler(self.queue, self.process_file_thread)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, WATCH_DIRECTORY, recursive=False)
        self.observer_thread = threading.Thread(target=self.observer.start)
        self.observer_thread.daemon = True 
        self.observer_thread.start()
        
        self.update_status(f"Monitorando: {WATCH_DIRECTORY}")

    def on_drop(self, event):
        filepath = event.data
        # Handle curly braces if path has spaces (tkinter behavior)
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
            
        print(f"DEBUG: File dropped: {filepath}")
        self.process_file_thread(filepath)

    def format_diarized_transcript(self, response):
        """Format the transcript with speaker diarization"""
        try:
            print("DEBUG: Starting format_diarized_transcript")
            # Get the paragraphs with speaker information
            paragraphs = response.results.channels[0].alternatives[0].paragraphs
            print(f"DEBUG: Got paragraphs: {paragraphs}")
            
            if not paragraphs or not hasattr(paragraphs, 'paragraphs'):
                # Fallback to simple transcript if diarization not available
                print("DEBUG: No paragraphs found, using fallback transcript")
                fallback = response.results.channels[0].alternatives[0].transcript
                print(f"DEBUG: Fallback transcript length: {len(fallback)}")
                return fallback
            
            print(f"DEBUG: Processing {len(paragraphs.paragraphs)} paragraphs")
            formatted_text = ""
            for idx, para in enumerate(paragraphs.paragraphs):
                speaker = para.speaker
                print(f"DEBUG: Paragraph {idx}, Speaker {speaker}")
                
                # Extract text from sentences (paragraphs don't have a direct 'text' attribute)
                if hasattr(para, 'sentences') and para.sentences:
                    text = " ".join([s.text for s in para.sentences if hasattr(s, 'text')])
                    print(f"DEBUG: Extracted text from {len(para.sentences)} sentences: {text[:100]}...")
                else:
                    # Fallback: reconstruct from words if sentences are not available
                    text = "[no text available]"
                    print("DEBUG: No sentences found in paragraph")
                
                # Format: "Speaker 0: [text]"
                formatted_text += f"Speaker {int(speaker)}: {text}\n\n"
            
            print(f"DEBUG: Final formatted text length: {len(formatted_text)}")
            return formatted_text.strip()
        
        except Exception as e:
            print(f"ERROR in format_diarized_transcript: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to simple transcript
            try:
                fallback = response.results.channels[0].alternatives[0].transcript
                print(f"DEBUG: Using fallback transcript, length: {len(fallback)}")
                return fallback
            except Exception as e2:
                print(f"ERROR: Even fallback failed: {e2}")
                traceback.print_exc()
                return "Erro ao processar transcrição"
    
    def process_file_thread(self, filepath):
        # Start processing in a separate thread to avoid freezing GUI
        threading.Thread(target=self.process_file, args=(filepath,), daemon=True).start()

    def process_file(self, filepath):
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext not in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
            self.queue.put(("error", f"Arquivo não suportado: {filename}"))
            return

        self.queue.put(("status", f"Processando: {filename}..."))
        
        try:
            with open(filepath, "rb") as file:
                buffer_data = file.read()

            options = {
                "model": "nova-3",
                "smart_format": True,
                "diarize": True,
                "paragraphs": True,
                "language": "pt-BR",
            }

            # Use self.deepgram client - pass raw bytes directly
            print(f"DEBUG: Sending file to Deepgram API, size: {len(buffer_data)} bytes")
            response = self.deepgram.listen.v1.media.transcribe_file(request=buffer_data, **options)
            print("DEBUG: API call successful, formatting transcript...")
            
            # Extract diarization information
            formatted_transcript = self.format_diarized_transcript(response)
            print(f"DEBUG: Formatted transcript ready, length: {len(formatted_transcript)} chars")
            print(f"DEBUG: First 200 chars: {formatted_transcript[:200]}")
            
            # Get audio duration from response metadata if available
            try:
                if hasattr(response, 'metadata') and hasattr(response.metadata, 'duration'):
                    duration_seconds = response.metadata.duration
                    self.total_audio_minutes += duration_seconds / 60.0
            except:
                pass  # If duration not available, just skip it
            
            # Update usage counter
            self.processed_files_count += 1
            self.queue.put(("update_usage", None))
            
            print(f"DEBUG: Sending transcription to queue...")
            self.queue.put(("transcription", formatted_transcript))
            self.queue.put(("status", "Pronto! Aguardando novos arquivos..."))

        except TimeoutError as e:
            error_msg = f"Timeout ao processar {filename}. Arquivo muito grande? Tente novamente."
            print(f"TIMEOUT ERROR in process_file: {error_msg}")
            import traceback
            traceback.print_exc()
            self.queue.put(("error", error_msg))
        except Exception as e:
            error_type = type(e).__name__
            
            # More specific error messages
            if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                error_msg = f"Timeout ao processar {filename}. O arquivo pode ser muito grande (tamanho: {len(buffer_data) / (1024*1024):.1f}MB). Tente com um arquivo menor."
            elif "unauthorized" in str(e).lower() or "401" in str(e):
                error_msg = f"Erro de autenticação. Verifique sua API key do Deepgram."
            elif "network" in str(e).lower() or "connection" in str(e).lower():
                error_msg = f"Erro de conexão. Verifique sua internet."
            else:
                error_msg = f"Erro ao transcrever ({error_type}): {str(e)}"
            
            print(f"ERROR in process_file: {error_msg}")
            import traceback
            traceback.print_exc()
            self.queue.put(("error", error_msg))

    def check_queue(self):
        try:
            while True:
                msg_type, data = self.queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.configure(text=data, text_color="gray")
                elif msg_type == "error":
                    self.status_label.configure(text=data, text_color="red")
                elif msg_type == "transcription":
                    self.append_text(data)
                elif msg_type == "update_usage":
                    self.update_usage_display()
                elif msg_type == "update_balance":
                    # Update with real balance from API
                    self.usage_label.configure(text=data, text_color="#00AA00")
                
                self.queue.task_done()
        except queue.Empty:
            pass
        
        self.after(100, self.check_queue)
    
    def update_usage_display(self):
        """Update the usage counter display"""
        if self.total_audio_minutes > 0:
            usage_text = f"Uso: {self.processed_files_count} arquivos ({self.total_audio_minutes:.1f} min)"
        else:
            usage_text = f"Uso: {self.processed_files_count} arquivos"
        self.usage_label.configure(text=usage_text)
    
    def try_update_balance(self):
        """Try to get real balance from API, fallback to usage counter"""
        def fetch_balance():
            try:
                # Try to get real balance from API
                projects = self.deepgram.manage.v1.projects.list()
                project_id = projects.projects[0].project_id
                balances = self.deepgram.manage.v1.projects.billing.balances.list(project_id=project_id)
                
                if balances and hasattr(balances, 'balances') and balances.balances:
                    total = sum(b.amount for b in balances.balances if hasattr(b, 'amount'))
                    self.queue.put(("update_balance", f"Saldo: ${total:.2f}"))
                    return True
            except Exception as e:
                # If API call fails (no permissions), just use usage counter
                print(f"Could not fetch balance (using usage counter): {e}")
                return False
        
        # Run in background thread
        threading.Thread(target=fetch_balance, daemon=True).start()
        
        # Update again in 60 seconds
        self.after(60000, self.try_update_balance)

    def update_status(self, text, error=False):
        color = "red" if error else "gray"
        self.status_label.configure(text=text, text_color=color)

    def append_text(self, text):
        print(f"DEBUG: append_text called with text length: {len(text) if text else 0}")
        print(f"DEBUG: Text content (first 200 chars): {text[:200] if text else 'EMPTY'}")
        
        self.textbox.configure(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.textbox.insert("end", f"[{timestamp}] Novo arquivo processado:\n")
        
        if text:
            self.textbox.insert("end", text + "\n\n" + "-"*50 + "\n\n")
        else:
            self.textbox.insert("end", "[AVISO: Transcrição vazia]\n\n" + "-"*50 + "\n\n")
            print("WARNING: Transcription text is empty!")
        
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear_text(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        text = self.textbox.get("0.0", "end")
        pyperclip.copy(text)
        original_text = self.copy_button.cget("text")
        self.copy_button.configure(text="Copiado!")
        self.after(2000, lambda: self.copy_button.configure(text=original_text))
    
    def load_last_directory(self):
        """Load the last used directory from config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('last_directory', os.path.expanduser('~'))
        except Exception as e:
            print(f"Error loading config: {e}")
        return os.path.expanduser('~')
    
    def save_last_directory(self, directory):
        """Save the last used directory to config file"""
        try:
            config = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            
            config['last_directory'] = directory
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def select_file(self):
        """Open file dialog to select an audio file"""
        filetypes = [
            ("Arquivos de Áudio", "*.mp3 *.wav *.m4a *.flac *.ogg"),
            ("Todos os arquivos", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo de áudio",
            initialdir=self.last_directory,
            filetypes=filetypes
        )
        
        if filepath:
            # Save the directory for next time
            directory = os.path.dirname(filepath)
            self.last_directory = directory
            self.save_last_directory(directory)
            
            # Process the selected file
            print(f"DEBUG: File selected: {filepath}")
            self.process_file_thread(filepath)
    
    def select_multiple_files(self):
        """Open file dialog to select multiple audio files"""
        filetypes = [
            ("Arquivos de Áudio", "*.mp3 *.wav *.m4a *.flac *.ogg"),
            ("Todos os arquivos", "*.*")
        ]
        
        filepaths = filedialog.askopenfilenames(
            title="Selecione arquivos de áudio",
            initialdir=self.last_directory,
            filetypes=filetypes
        )
        
        if filepaths:
            # Save the directory for next time
            directory = os.path.dirname(filepaths[0])
            self.last_directory = directory
            self.save_last_directory(directory)
            
            # Process all selected files
            print(f"DEBUG: {len(filepaths)} file(s) selected")
            for filepath in filepaths:
                print(f"DEBUG: Processing file: {filepath}")
                self.process_file_thread(filepath)

class AudioFileHandler(FileSystemEventHandler):
    def __init__(self, queue_ref, process_callback):
        self.queue = queue_ref
        self.process_callback = process_callback

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_event(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self.handle_event(event.dest_path)

    def handle_event(self, filepath):
        print(f"DEBUG: Event detected for {filepath}")
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
            print(f"File qualified: {filepath}")
            # Wait a moment for file write/move to complete
            time.sleep(5) 
            self.process_callback(filepath)


if __name__ == "__main__":
    print("DEBUG: Starting main...")
    
    print("DEBUG: Initializing app...")
    app = TranscriptionApp()
    print("DEBUG: Entering mainloop...")
    app.mainloop()
    print("DEBUG: Exited mainloop")
