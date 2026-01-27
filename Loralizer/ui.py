import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from normalizerC import NormalizerC
from file_utils import FileUtils
from lora_utils import LoraUtils
from lora import Lora
import os

# Configuración global de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """
    Aplicación para preparar datasets de entrenamiento de LoRA.
    Incluye normalización de imágenes, cálculo de parámetros de entrenamiento
    y creación de estructuras de carpetas.
    """
    
    # Constantes de diseño
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 650
    SIDEBAR_WIDTH = 180
    PADDING = 20
    SMALL_PADDING = 10
    BUTTON_HEIGHT = 32
    
    def __init__(self):
        super().__init__()
        
        # Variables de estado
        self.lora_name = ""
        self.lora_version = ""
        self.lora_name_version = ""
        self.normalizer_path = ""
        self.source_path = ""
        
        # Inicializar componentes
        self._initialize_data()
        self._configure_window()
        self._create_layout()
        
    def _initialize_data(self):
        """Inicializa datos desde FileUtils con manejo de errores."""
        try:
            self.lora_version = str(FileUtils.get_last_lora_version())
        except Exception as e:
            print(f"Warning: Could not retrieve LoRA version: {e}")
            self.lora_version = "1"
        
        try:
            self.training_folder = str(FileUtils.get_lora_training_folder())
        except Exception as e:
            print(f"Warning: Could not retrieve training folder: {e}")
            self.training_folder = os.path.expanduser("~/lora_training")
        
        self.lora_name = f"model{self.lora_version}"
    
    def _configure_window(self):
        """Configura las propiedades de la ventana principal."""
        self.title("Loralizer13")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        
        # Configurar grid responsivo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def _create_layout(self):
        """Crea el layout principal de la aplicación."""
        self._create_sidebar()
        self._create_main_content()
    
    # ==================== SIDEBAR ====================
    
    def _create_sidebar(self):
        """Crea la barra lateral con herramientas de preparación."""
        self.sidebar = ctk.CTkFrame(self, width=self.SIDEBAR_WIDTH, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Título de la sección
        title = ctk.CTkLabel(
            self.sidebar,
            text="Preparation Tools",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, padx=self.PADDING, pady=(self.PADDING, 5))
        
        # Campo de nombre de LoRA
        ctk.CTkLabel(
            self.sidebar,
            text="LoRA Name:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=self.PADDING, pady=(15, 5), sticky="w")
        
        # Placeholder dinámico
        placeholder_text = f"xx_part_{self.lora_version}"
        
        self.lora_name_entry = ctk.CTkEntry(
            self.sidebar,
            height=35
        )
        self.lora_name_entry.grid(row=2, column=0, padx=self.PADDING, pady=5, sticky="ew")
        
        # Configurar comportamiento del placeholder
        self.lora_name_entry.insert(0, placeholder_text)
        default_text_color = self.lora_name_entry.cget("text_color")
        self.lora_name_entry.configure(text_color="gray")
        
        def on_focus_in(event):
            if self.lora_name_entry.get() == placeholder_text:
                self.lora_name_entry.delete(0, tk.END)
                self.lora_name_entry.configure(text_color=default_text_color)
                
        def on_focus_out(event):
            if not self.lora_name_entry.get():
                self.lora_name_entry.insert(0, placeholder_text)
                self.lora_name_entry.configure(text_color="gray")
                
        self.lora_name_entry.bind("<FocusIn>", on_focus_in)
        self.lora_name_entry.bind("<FocusOut>", on_focus_out)
        
        # Separador
        ctk.CTkLabel(self.sidebar, text="").grid(row=3, column=0, pady=5)
        
        # Botones de herramientas
        self.btn_normalize = ctk.CTkButton(
            self.sidebar,
            text="📐 Normalize",
            command=self._run_normalizer,
            height=self.BUTTON_HEIGHT,
            font=ctk.CTkFont(size=12)
        )
        self.btn_normalize.grid(row=4, column=0, padx=self.PADDING, pady=5, sticky="ew")

        # Resolution Selector
        ctk.CTkLabel(
            self.sidebar,
            text="Resolution:",
            font=ctk.CTkFont(size=12)
        ).grid(row=5, column=0, padx=self.PADDING, pady=(5, 0), sticky="w")

        self.resolution_var = ctk.StringVar(value="1024")
        self.resolution_combo = ctk.CTkComboBox(
            self.sidebar,
            values=["1024", "1280", "1536"],
            variable=self.resolution_var,
            height=self.BUTTON_HEIGHT,
            font=ctk.CTkFont(size=12)
        )
        self.resolution_combo.grid(row=6, column=0, padx=self.PADDING, pady=(0, 5), sticky="ew")
        
        self.btn_augment = ctk.CTkButton(
            self.sidebar,
            text="🔄 Data Augmentation",
            command=self._run_augmentation,
            height=self.BUTTON_HEIGHT,
            font=ctk.CTkFont(size=12),
            state="disabled"  # Placeholder para futura implementación
        )
        self.btn_augment.grid(row=7, column=0, padx=self.PADDING, pady=5, sticky="ew")
        
        # Información de versión
        version_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Version: {self.lora_version}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        version_label.grid(row=11, column=0, padx=self.PADDING, pady=(0, self.PADDING), sticky="s")
    
    # ==================== MAIN CONTENT ====================
    
    def _create_main_content(self):
        """Crea el contenido principal con configuración de entrenamiento."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Título dinámico
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Training Configuration",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=self.PADDING, pady=(self.PADDING, 10))
        
        # Frame de configuración
        self.config_frame = ctk.CTkFrame(self.main_frame)
        self.config_frame.grid(row=1, column=0, padx=self.PADDING, pady=10, sticky="ew")
        self.config_frame.grid_columnconfigure(1, weight=1)
        
        # Crear campos de entrada
        self._create_input_fields()
        
        # Frame de botones de acción
        self.action_frame = ctk.CTkFrame(self.main_frame)
        self.action_frame.grid(row=2, column=0, padx=self.PADDING, pady=10, sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1), weight=1)
        
        self._create_action_buttons()
        
        # Frame de información adicional
        self._create_info_panel()
    
    def _create_input_fields(self):
        """Crea los campos de entrada para configuración de entrenamiento."""
        fields = [
            ("Source Folder:", "source", True),
            ("Total Images:", "total_files", False),
            ("Repeats:", "total_repeats", False),
            ("Epochs:", "total_epochs", False),
            ("Batch Size:", "total_batch", False),
            ("Training Steps:", "total_steps", False),
        ]
        
        self.entries = {}
        
        for idx, (label_text, field_name, is_button) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                self.config_frame,
                text=label_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            label.grid(row=idx, column=0, padx=(self.PADDING, 10), pady=8, sticky="w")
            
            if is_button:
                # Botón para seleccionar carpeta
                btn_frame = ctk.CTkFrame(self.config_frame)
                btn_frame.grid(row=idx, column=1, padx=(0, self.PADDING), pady=8, sticky="ew")
                btn_frame.grid_columnconfigure(0, weight=1)
                
                entry = ctk.CTkEntry(btn_frame, placeholder_text="No folder selected")
                entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
                
                btn = ctk.CTkButton(
                    btn_frame,
                    text="Browse",
                    command=self._select_source_folder,
                    width=80
                )
                btn.grid(row=0, column=1)
                
                self.entries[field_name] = entry
            else:
                # Entry normal
                entry = ctk.CTkEntry(
                    self.config_frame,
                    placeholder_text=f"Enter {label_text.lower().replace(':', '')}"
                )
                entry.grid(row=idx, column=1, padx=(0, self.PADDING), pady=8, sticky="ew")
                self.entries[field_name] = entry
    
    def _create_action_buttons(self):
        """Crea los botones de acción principales."""
        self.btn_calculate = ctk.CTkButton(
            self.action_frame,
            text="🔢 Calculate Steps",
            command=self._calculate_training_steps,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1f6aa5"
        )
        self.btn_calculate.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.btn_create = ctk.CTkButton(
            self.action_frame,
            text="✅ Create Structure",
            command=self._create_training_structure,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2fa572"
        )
        self.btn_create.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.btn_clear = ctk.CTkButton(
            self.action_frame,
            text="🗑️ Clear All",
            command=self._clear_all_fields,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#c42b1c"
        )
        self.btn_clear.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    
    def _create_info_panel(self):
        """Crea el botón de ayuda que abre un modal."""
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.grid(row=3, column=0, padx=self.PADDING, pady=10, sticky="ew")
        
        # Botón de ayuda centrado con icono
        self.btn_help = ctk.CTkButton(
            info_frame,
            text="ℹ️  Quick Guide & Help",
            command=self._show_help_modal,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#6b6b6b",
            hover_color="#525252"
        )
        self.btn_help.pack(pady=10, padx=10, fill="x")
    
    # ==================== EVENT HANDLERS ====================
    
    def _run_normalizer(self):
        """Ejecuta el normalizador de imágenes."""
        if not self._validate_lora_name():
            return
        
        input_dir = filedialog.askdirectory(title="Select Source Images Folder")
        if not input_dir:
            return
        
        # Crear carpeta de salida
        self.normalizer_path = input_dir + '_normalized'
        os.makedirs(self.normalizer_path, exist_ok=True)
        
        try:
            # Mostrar ventana de progreso
            progress_window = self._show_progress_window("Normalizing images...")
            
            # Get selected resolution
            try:
                target_res = int(self.resolution_var.get())
            except ValueError:
                target_res = 1024

            NormalizerC(input_dir, self.normalizer_path, self.lora_name, target_size=target_res)
            
            progress_window.destroy()
            
            messagebox.showinfo(
                "Success",
                f"Normalization complete!\n\nOutput folder:\n{self.normalizer_path}"
            )
            
            # Auto-rellenar la ruta de origen si está vacía
            if not self.entries["source"].get():
                self.entries["source"].delete(0, tk.END)
                self.entries["source"].insert(0, self.normalizer_path)
                self._update_file_count(self.normalizer_path)
                
        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            messagebox.showerror("Error", f"Normalization failed:\n{str(e)}")
    
    def _run_augmentation(self):
        """Placeholder para futura implementación de data augmentation."""
        messagebox.showinfo("Coming Soon", "Data augmentation feature is under development!")
    
    def _select_source_folder(self):
        """Permite al usuario seleccionar la carpeta de origen."""
        if not self._validate_lora_name():
            return
        
        dir_path = filedialog.askdirectory(title="Select Dataset Folder")
        if not dir_path:
            return
        
        # Actualizar UI
        self.entries["source"].delete(0, tk.END)
        self.entries["source"].insert(0, dir_path)
        
        # Actualizar título
        folder_name = os.path.basename(dir_path)
        self.title_label.configure(text=f"Dataset: {folder_name}")
        
        # Contar archivos y actualizar campos
        self._update_file_count(dir_path)
        self._set_default_training_params()
    
    def _update_file_count(self, dir_path):
        """Actualiza el conteo de archivos en el directorio."""
        try:
            total_files = FileUtils.count_files(dir_path)
            # Dividir por 2 asumiendo que hay pares de imagen + caption
            total_images = int(total_files / 2)
            
            if total_images <= 0:
                messagebox.showwarning("Warning", "The selected folder appears to be empty!")
                return
            
            self.entries["total_files"].delete(0, tk.END)
            self.entries["total_files"].insert(0, str(total_images))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not count files:\n{str(e)}")
    
    def _set_default_training_params(self):
        """Establece parámetros predeterminados de entrenamiento."""
        defaults = {
            "total_repeats": "20",
            "total_epochs": "1",
            "total_batch": "1"
        }
        
        for field, value in defaults.items():
            if not self.entries[field].get():  # Solo si está vacío
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, value)
        
        # Calcular steps automáticamente
        self._calculate_training_steps()
    
    def _calculate_training_steps(self):
        """Calcula los pasos totales de entrenamiento."""
        try:
            # Limpiar campo de steps
            self.entries["total_steps"].delete(0, tk.END)
            
            # Obtener valores
            total_files = float(self.entries["total_files"].get())
            epochs = int(self.entries["total_epochs"].get())
            repeats = int(self.entries["total_repeats"].get())
            batch_size = int(self.entries["total_batch"].get())
            
            # Validar batch size
            if batch_size == 0:
                messagebox.showerror("Error", "Batch size cannot be zero!")
                return
            
            # Calcular steps
            total_steps = int((total_files * epochs * repeats) / batch_size)
            
            # Actualizar UI
            self.entries["total_steps"].insert(0, str(total_steps))
            
            messagebox.showinfo(
                "Calculation Complete",
                f"Training steps calculated: {total_steps}\n\n"
                f"Configuration:\n"
                f"• Images: {int(total_files)}\n"
                f"• Epochs: {epochs}\n"
                f"• Repeats: {repeats}\n"
                f"• Batch size: {batch_size}"
            )
            
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers in all fields before calculating."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed:\n{str(e)}")
    
    def _create_training_structure(self):
        """Crea la estructura de carpetas para entrenamiento."""
        if not self._validate_all_fields():
            return
        
        try:
            # Crear objeto Lora
            lora_structure = Lora(
                self.training_folder,
                self.lora_name,
                self.lora_name_version,
                self.lora_version,
                self.entries["source"].get(),
                self.entries["total_repeats"].get(),
                self.entries["total_files"].get(),
                self.entries["total_epochs"].get(),
                self.entries["total_batch"].get(),
                self.entries["total_steps"].get()
            )
            
            # Crear estructura
            lora_utils = LoraUtils(lora_structure)
            lora_utils.create_lora_structure()
            
            messagebox.showinfo(
                "Success",
                f"Training structure created successfully!\n\n"
                f"LoRA: {self.lora_name_version}\n"
                f"Location: {self.training_folder}"
            )
            
            # Preguntar si quiere limpiar los campos
            if messagebox.askyesno("Clear Fields?", "Do you want to clear all fields for a new project?"):
                self._clear_all_fields()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create structure:\n{str(e)}")
    
    def _clear_all_fields(self):
        """Limpia todos los campos de entrada."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        self.title_label.configure(text="Training Configuration")
        messagebox.showinfo("Cleared", "All fields have been cleared.")
    
    # ==================== VALIDATION ====================
    
    def _validate_lora_name(self):
        """Valida que se haya ingresado un nombre para el LoRA."""
        lora_input = self.lora_name_entry.get().strip()
        
        if not lora_input:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a name for your LoRA model in the sidebar."
            )
            return False
        
        self.lora_name = lora_input
        self.lora_name_version = f"{lora_input}_v{self.lora_version}"
        return True
    
    def _validate_all_fields(self):
        """Valida que todos los campos requeridos estén completos."""
        if not self._validate_lora_name():
            return False
        
        required_fields = {
            "source": "Source folder",
            "total_files": "Total images",
            "total_repeats": "Repeats",
            "total_epochs": "Epochs",
            "total_batch": "Batch size",
            "total_steps": "Training steps"
        }
        
        for field, name in required_fields.items():
            if not self.entries[field].get():
                messagebox.showwarning(
                    "Incomplete Form",
                    f"Please fill in the '{name}' field."
                )
                return False
        
        return True
    
    # ==================== UTILITIES ====================
    
    def _show_progress_window(self, message):
        """Muestra una ventana de progreso simple."""
        progress = ctk.CTkToplevel(self)
        progress.title("Processing")
        progress.geometry("300x100")
        progress.transient(self)
        progress.grab_set()
        
        label = ctk.CTkLabel(
            progress,
            text=message,
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=30)
        
        progress.update()
        return progress
    
    def _show_help_modal(self):
        """Muestra un modal con la guía paso a paso y ayuda."""
        # Crear ventana modal
        help_modal = ctk.CTkToplevel(self)
        help_modal.title("Quick Guide & Help")
        help_modal.geometry("600x550")
        help_modal.transient(self)
        help_modal.grab_set()
        
        # Centrar ventana
        help_modal.update_idletasks()
        x = (help_modal.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_modal.winfo_screenheight() // 2) - (550 // 2)
        help_modal.geometry(f"+{x}+{y}")
        
        # Frame principal con scroll
        main_frame = ctk.CTkFrame(help_modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="📖 LoRA Dataset Helper - Quick Guide",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(0, 15))
        
        # ScrollableFrame para el contenido
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=380)
        scroll_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Contenido de ayuda
        help_sections = [
            {
                "title": "🎯 Getting Started",
                "content": "This tool helps you prepare image datasets for training LoRA (Low-Rank Adaptation) models. Follow these steps to create a properly formatted dataset."
            },
            {
                "title": "📝 Step-by-Step Guide",
                "content": """1. Enter LoRA Name
   • Type a unique name for your model in the sidebar
   • Example: "character_style" or "my_avatar"

2. Normalize Images (Recommended)
   • Click "Normalize" in the sidebar
   • Select folder containing your original images
   • Images will be resized and centered automatically
   • Captions will be generated using AI

3. Select Dataset Folder
   • Click "Browse" next to "Source Folder"
   • Choose your normalized images folder
   • File count will update automatically

4. Configure Training Parameters
   • Repeats: How many times each image is used (default: 20)
   • Epochs: Full passes through dataset (default: 1)
   • Batch Size: Images processed together (default: 1)

5. Calculate Training Steps
   • Click "Calculate Steps" button
   • Formula: (images × epochs × repeats) / batch_size
   • Review the calculated steps

6. Create Training Structure
   • Click "Create Structure" to finalize
   • Folder structure will be created automatically
   • You're ready to start training!"""
            },
            {
                "title": "⚙️ Understanding Parameters",
                "content": """• Total Images: Number of training images in your dataset

• Repeats: Controls how often each image appears during training
  - Higher values (20-30): Better learning, longer training
  - Lower values (10-15): Faster training, may underfit

• Epochs: Complete passes through entire dataset
  - Usually 1-3 for LoRA training
  - More epochs = more training time

• Batch Size: Number of images processed simultaneously
  - Default 1 for most setups
  - Higher values need more VRAM

• Training Steps: Total optimization iterations
  - Automatically calculated
  - Typical range: 500-3000 steps"""
            },
            {
                "title": "💡 Tips & Best Practices",
                "content": """✓ Use 15-50 high-quality images for best results
✓ Images should be diverse but consistent in style
✓ Normalize all images to 1024×1024 before training
✓ Start with default parameters (20 repeats, 1 epoch)
✓ Review generated captions and edit if needed
✓ Keep batch size at 1 unless you have 12GB+ VRAM

⚠️ Common Issues:
• Empty folder: Make sure images are in correct format
• Low quality results: Try more images or repeats
• Out of memory: Reduce batch size to 1"""
            },
            {
                "title": "📁 Output Structure",
                "content": """After clicking "Create Structure", you'll get:

training_folder/
├── model_v1/
│   ├── dataset/
│   │   ├── 20_concept/
│   │   │   ├── image1.png
│   │   │   ├── image1.txt
│   │   │   └── ...
│   ├── config.json
│   └── training_params.txt

The "20_" prefix indicates repeat count."""
            }
        ]
        
        # Crear secciones
        for section in help_sections:
            # Frame para cada sección
            section_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            section_frame.pack(fill="x", pady=(0, 15))
            
            # Título de sección
            section_title = ctk.CTkLabel(
                section_frame,
                text=section["title"],
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="w"
            )
            section_title.pack(fill="x", pady=(0, 8))
            
            # Contenido de sección
            section_content = ctk.CTkTextbox(
                section_frame,
                height=150 if "Step-by-Step" in section["title"] else 100,
                wrap="word",
                font=ctk.CTkFont(size=12)
            )
            section_content.pack(fill="x")
            section_content.insert("1.0", section["content"])
            section_content.configure(state="disabled")
        
        # Botón de cerrar
        close_btn = ctk.CTkButton(
            main_frame,
            text="Got it! Close",
            command=help_modal.destroy,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2fa572"
        )
        close_btn.pack(pady=(10, 0))


def main():
    """Punto de entrada de la aplicación."""
    app = LoraDatasetHelper()
    app.mainloop()


if __name__ == "__main__":
    main()