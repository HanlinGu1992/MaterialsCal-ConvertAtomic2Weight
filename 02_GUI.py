import sys
import json
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# ==========================================
# 1. Core Logic
# ==========================================

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # If not running in a bundle (running as .py), use current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_element_atomic_masses():
    # Use resource_path to locate the JSON file
    filename = resource_path('01_element_atomic-masses.json')
    
    # Debug code (optional): Print path to verify if needed
    # print(f"Looking for file at: {filename}") 

    if not os.path.exists(filename):
        # Fallback dictionary if JSON is not found (e.g., if forgotten during packaging)
        # Data covers H to Zn
        return {"H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078, "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Error reading data file: {e}")

# Initialize global data constant
ELEMENT_MOLAR_MASS = get_element_atomic_masses()

def check_input_composition(comp_dict, mode='wt'):
    """Ensure the input composition sums to 100% (with a small tolerance)"""
    total = sum(comp_dict.values())
    if not (abs(total-100) <= 0.01):
        raise ValueError(f"Sum is {total:.4f}, not equal to 100%. Please check your input.")

def wt_to_at(wt_dict):
    """Convert Weight Percent (Wt%) to Atomic Percent (At%)"""
    check_input_composition(wt_dict, 'wt')
    molar_amounts = {}
    for element, wt_percent in wt_dict.items():
        if element not in ELEMENT_MOLAR_MASS:
            raise ValueError(f"Element '{element}' is missing from the database.")
        molar_amounts[element] = wt_percent / ELEMENT_MOLAR_MASS[element]
    
    total_moles = sum(molar_amounts.values())
    at_dict = {elem: (val / total_moles) * 100 for elem, val in molar_amounts.items()}
    return at_dict

def at_to_wt(at_dict):
    """Convert Atomic Percent (At%) to Weight Percent (Wt%)"""
    check_input_composition(at_dict, 'at')
    masses = {}
    for element, at_percent in at_dict.items():
        if element not in ELEMENT_MOLAR_MASS:
            raise ValueError(f"Element '{element}' is missing from the database.")
        masses[element] = at_percent * ELEMENT_MOLAR_MASS[element]
    
    total_mass = sum(masses.values())
    wt_dict = {elem: (val / total_mass) * 100 for elem, val in masses.items()}
    return wt_dict

def parse_composition_input(user_str):
    """Parse input string with flexible error handling"""
    try:
        clean_str = user_str.strip()
        # Allow Python dict format
        if clean_str.startswith("{") and clean_str.endswith("}"):
            result = eval(clean_str)
            if isinstance(result, dict):
                return result
    except:
        pass
    
    # Allow formats like Element:50 or Element = 50
    pattern = r"['\"]?([A-Za-z][a-z]?)['\"]?\s*[:=]\s*(\d+\.?\d*)"
    matches = re.findall(pattern, user_str)
    if not matches:
        raise ValueError("Unrecognized format. Please use format like: Fe:50, C:50")
    
    comp_dict = {}
    for elem, val in matches:
        comp_dict[elem] = float(val)
    return comp_dict

# ==========================================
# 2. Modern GUI Class
# ==========================================

class CompositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Material Composition Converter")
        self.root.geometry("650x600") # Increased height slightly to accommodate larger output
        
        # 1. Apply Modern Theme
        self.setup_styles()
        
        # Define fonts
        self.text_font = Font(family="Segoe UI", size=10)
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Header / Title ---
        header_label = ttk.Label(
            main_frame, 
            text="Material Composition Converter", 
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50"
        )
        header_label.pack(pady=(0, 15), anchor="center")

        # --- Mode Selection ---
        mode_frame = ttk.LabelFrame(main_frame, text="Conversion Mode", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.mode_var = tk.StringVar(value="1")
        radio_frame = ttk.Frame(mode_frame)
        radio_frame.pack(fill=tk.X)
        
        # Radio buttons for Wt% -> At% and At% -> Wt%
        rb1 = ttk.Radiobutton(radio_frame, text="Wt% -> At%", variable=self.mode_var, value="1")
        rb1.pack(side=tk.LEFT, padx=20)
        
        rb2 = ttk.Radiobutton(radio_frame, text="At% -> Wt%", variable=self.mode_var, value="2")
        rb2.pack(side=tk.LEFT, padx=20)

        # --- Input Area (Reduced size) ---
        input_frame = ttk.LabelFrame(main_frame, text="Input Data (e.g., Fe:98.0, C:2.0)", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # Reduced height to 6 lines
        self.input_text = tk.Text(input_frame, height=6, font=self.text_font, 
                                  bd=1, relief="solid", highlightthickness=0, padx=5, pady=5)
        self.input_text.pack(fill=tk.X) 
        self.input_text.insert(tk.END, "Fe: 98.0, C: 2.0")

        # --- Buttons ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Convert Button
        convert_btn = ttk.Button(btn_frame, text="Convert", style="Accent.TButton", command=self.on_convert)
        convert_btn.pack(side=tk.RIGHT, padx=5)
        
        # Clear Button
        clear_btn = ttk.Button(btn_frame, text="Clear", style="Secondary.TButton", command=self.on_clear)
        clear_btn.pack(side=tk.RIGHT, padx=5)

        # --- Output Area (Increased size with Scrollbar) ---
        output_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True) # Expand to fill remaining space
        
        # Create a container for the text widget and scrollbar
        text_container = ttk.Frame(output_frame)
        text_container.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_container, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Result Text Area
        self.result_text = tk.Text(
            text_container, 
            font=self.text_font, 
            bg="#f8f9fa", 
            fg="#2c3e50", 
            bd=0, 
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set,
            padx=5, pady=5
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Link scrollbar to text
        scrollbar.config(command=self.result_text.yview)

    def setup_styles(self):
        """Configure modern styles using ttk.Style"""
        style = ttk.Style()
        # Use 'clam' as a cross-platform base for custom coloring (works better than default on Windows/Mac)
        try:
            style.theme_use('clam') 
        except:
            pass

        # Define Colors
        bg_color = "#ffffff"
        select_bg = "#3498db"
        accent_color = "#2980b9" # Dark Blue
        secondary_color = "#95a5a6" # Grey
        text_color = "#2c3e50"

        # Style configurations
        style.configure("TFrame", background=bg_color)
        style.configure("TLabelframe", background=bg_color, bordercolor="#bdc3c7", borderwidth=1)
        style.configure("TLabelframe.Label", background=bg_color, foreground=select_bg, font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("TRadiobutton", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        
        # Buttons
        # Accent Button (Primary action)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=accent_color, foreground="white", 
                        borderwidth=0, focuscolor="none", padding=10)
        style.map("Accent.TButton", background=[("active", "#1c5980")])

        # Secondary Button
        style.configure("Secondary.TButton", font=("Segoe UI", 10), background=secondary_color, foreground="white", 
                        borderwidth=0, focuscolor="none", padding=10)
        style.map("Secondary.TButton", background=[("active", "#7f8c8d")])

        self.root.configure(background=bg_color)

    def on_clear(self):
        """Clears input and output fields"""
        self.input_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    def on_convert(self):
        """Handles the conversion logic triggered by the button"""
        raw_input = self.input_text.get(1.0, tk.END).strip()
        mode = self.mode_var.get()
        
        if not raw_input:
            messagebox.showwarning("Input Error", "Please enter composition data.")
            return

        try:
            # Parse user input into a dictionary
            comp_dict = parse_composition_input(raw_input)
            
            # Choose conversion direction
            if mode == "1":
                result_dict = wt_to_at(comp_dict)
                origin_label = "Wt%"
                result_label = "At%"
            else:
                result_dict = at_to_wt(comp_dict)
                origin_label = "At%"
                result_label = "Wt%"

            # Format output
            output_lines = []
            output_lines.append(f"{'Element':<10} | {origin_label:<15} | {result_label:<15}")
            output_lines.append("-" * 45)
            
            for elem in comp_dict.keys():
                val_orig = comp_dict[elem]
                val_conv = result_dict.get(elem, 0.0)
                output_lines.append(f"{elem:<10} | {val_orig:<15.4f} | {val_conv:<15.4f}")

            # Display result
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n".join(output_lines))
            
            # Auto-scroll to top on new result
            self.result_text.see(tk.END) 
            
            self.result_text.config(state=tk.DISABLED)

        except ValueError as ve:
            messagebox.showerror("Calculation Error", str(ve))
        except Exception as e:
            messagebox.showerror("System Error", f"An unknown error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompositionApp(root)
    root.mainloop()
