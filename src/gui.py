'''
gui.py
    This module creates a GUI application for converting pseudocode to flowchart with multiple tabs,
    pseudocode editor, and interactive flowchart viewer

Author: Puttipong Srisuwantat (Non)
Date: 1 Oct 2025
'''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
try:
    from PIL import Image, ImageTk, ImageDraw
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False

class FlowchartTab:
    '''
    Individual tab for pseudocode to flowchart conversion
    Manages the state and UI of a single tab
    Arg:
        parent - parent notebook widget
        tab_name - name of the tab
    '''
    def __init__(self, parent, tab_name="New Tab"):
        self.parent = parent  # parent notebook widget
        self.tab_name = tab_name  # display name for the tab
        self.file_path = None  # path to currently loaded .psc file
        self.is_file_loaded = False  # tracks if a file has been uploaded
        
        # Create main frame for this tab
        self.main_frame = ttk.Frame(parent)
        
        # Initialize UI components
        self._create_upload_ui()
        self._create_editor_ui()
        
        # Start with upload screen
        self._show_upload_screen()
    
    '''
    Creates the upload interface UI components and instructions
    '''
    def _create_upload_ui(self):
        self.upload_frame = ttk.Frame(self.main_frame)
        
        center_container = ttk.Frame(self.upload_frame)
        center_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Load and display Upload.svg
        self._create_upload_icon(center_container)
        
        # Title
        title_label = ttk.Label(center_container, text="Upload Pseudocode File", 
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(center_container, text="Select a .psc file to start creating your flowchart",
                                  font=("Arial", 12), foreground="gray")
        subtitle_label.pack(pady=(0, 30))
        
        # Choose file button
        self.choose_file_button = ttk.Button(center_container, text="📁 Choose File", 
                                           command=self._upload_file, width=20)
        self.choose_file_button.pack(pady=(0, 20))
        
        # Supported format info
        format_label = ttk.Label(center_container, text="Supported format: .psc files only",
                                font=("Arial", 10), foreground="gray")
        format_label.pack()
    
    '''
    Creates the upload icon from SVG or fallback to canvas
    Arg:
        parent - parent container to place the icon in
    '''
    def _create_upload_icon(self, parent):
        icon_size = 85
        
        if SVG_SUPPORT:
            try:
                # Read SVG content and modify colors
                with open("Upload.svg", "r") as svg_file:
                    svg_content = svg_file.read()
                
                # Convert SVG to PNG in memory
                png_data = cairosvg.svg2png(
                    bytestring=svg_content.encode('utf-8'),
                    output_width=icon_size,
                    output_height=icon_size
                )
                
                # Load PNG data into PIL Image
                from io import BytesIO
                svg_image = Image.open(BytesIO(png_data))
                
                circle_size = icon_size + 40  # Add padding
                background = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
                
                # Draw circle
                draw = ImageDraw.Draw(background)
                draw.ellipse([0, 0, circle_size-1, circle_size-1], fill=(0, 122, 204, 255))
                
                # Calculate position to center the SVG on the circle
                x_pos = (circle_size - icon_size) // 2
                y_pos = (circle_size - icon_size) // 2
                
                # Paste the SVG image onto the circle
                background.paste(svg_image, (x_pos, y_pos), svg_image if svg_image.mode == 'RGBA' else None)
                
                # Convert to PhotoImage for Tkinter
                self.upload_photo = ImageTk.PhotoImage(background)
                
                # Create label to display the circular icon
                upload_label = tk.Label(parent, image=self.upload_photo, bg='#f7f9fc', border=0)
                upload_label.pack(pady=(0, 20))
                return  # Successfully loaded SVG
                
            except Exception as e:
                print(f"Failed to load SVG: {e}")
                print(f"SVG file exists: {os.path.exists('Upload.svg')}")
                # Fall through to canvas fallback
        
        # Fallback
        canvas_size = 140
        upload_icon_frame = tk.Frame(parent, width=canvas_size, height=canvas_size)
        upload_icon_frame.pack(pady=(0, 20))
        upload_icon_frame.pack_propagate(False)
        icon_canvas = tk.Canvas(upload_icon_frame, width=canvas_size, height=canvas_size, 
                              highlightthickness=0, bg='#f7f9fc')
        icon_canvas.pack()
        icon_canvas.create_oval(10, 10, canvas_size-10, canvas_size-10, fill="#007acc", outline="")
        icon_canvas.create_text(canvas_size//2, canvas_size//2, text="↑", font=("Arial", 40, "bold"), fill="#f7f9fc")
    
    '''
    Creates the editor interface UI components
    Contains pseudocode editor on left and flowchart display on right
    '''
    def _create_editor_ui(self):
        self.editor_frame = ttk.Frame(self.main_frame)
        
        # Create left and right panes
        paned_window = ttk.PanedWindow(self.editor_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left pane - Pseudocode editor
        left_frame = ttk.Frame(paned_window, width=400)
        paned_window.add(left_frame, weight=1)
        
        # Editor title
        editor_title = ttk.Label(left_frame, text="Pseudocode Editor", font=("Arial", 14, "bold"))
        editor_title.pack(anchor="w", pady=(0, 10))
        
        # Create frame for text editor with line numbers
        editor_container = ttk.Frame(left_frame)
        editor_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Line numbers
        self.line_numbers = tk.Text(editor_container, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none',
                                   font=("Consolas", 11), bg="#f5f5f5", fg="#888888")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Add a separator line between line numbers and text editor
        separator = tk.Frame(editor_container, width=1, bg="#d0d0d0")
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        
        # Text editor with scrolling and undo enabled
        self.text_editor = scrolledtext.ScrolledText(
            editor_container,
            wrap=tk.NONE,
            width=46,
            height=25,
            font=("Consolas", 11),
            undo=True,
            maxundo=50,
            foreground="#1f2937",      # text color
            background="#ffffff",      # editor background
            insertbackground="#007acc", # caret color
            selectbackground="#cde8ff"  # selection highlight
        )
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sync scrolling between line numbers and text editor
        self.text_editor.config(yscrollcommand=self._on_text_scroll)
        
        # Bind events for line number updates
        self.text_editor.bind('<KeyPress>', self._on_content_changed)
        self.text_editor.bind('<KeyRelease>', self._on_content_changed)
        self.text_editor.bind('<Button-1>', self._on_content_changed)
        self.text_editor.bind('<MouseWheel>', self._on_mouse_wheel)
        
        # Initialize line numbers
        self._update_line_numbers()
        
        # Bind keyboard shortcuts
        self.text_editor.bind('<Control-z>', lambda e: self._undo_action())
        self.text_editor.bind('<Control-y>', lambda e: self._redo_action())
        self.text_editor.bind('<Control-Shift-Z>', lambda e: self._redo_action())
        self.text_editor.bind('<Control-s>', lambda e: self._save_file())
        self.text_editor.bind('<Control-x>', lambda e: self._cut_text())
        self.text_editor.bind('<Control-c>', lambda e: self._copy_text())
        self.text_editor.bind('<Control-v>', lambda e: self._paste_text())
        
        # Control buttons frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_editor)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.undo_button = ttk.Button(button_frame, text="↩", command=self._undo_action, width=3)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.redo_button = ttk.Button(button_frame, text="↪", command=self._redo_action, width=3)
        self.redo_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_button = ttk.Button(button_frame, text="💾", command=self._save_file, width=3)
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.generate_button = ttk.Button(button_frame, text="Generate", command=self._generate_flowchart,
                                        style="Accent.TButton")
        self.generate_button.pack(side=tk.RIGHT)
        
        # Right pane - Flowchart display
        right_frame = ttk.Frame(paned_window, width=400)
        paned_window.add(right_frame, weight=1)
        
        # Flowchart title
        flowchart_title = ttk.Label(right_frame, text="Flowchart", font=("Arial", 14, "bold"))
        flowchart_title.pack(anchor="w", pady=(0, 10))
        
        # Flowchart canvas with scrollbars
        canvas_frame = ttk.Frame(right_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.flowchart_canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, 
                                        highlightbackground="gray")
        
        # Scrollbars for canvas
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.flowchart_canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.flowchart_canvas.xview)
        
        self.flowchart_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.flowchart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events for zoom and pan
        self.flowchart_canvas.bind("<Button-1>", self._start_pan)
        self.flowchart_canvas.bind("<B1-Motion>", self._do_pan)
        self.flowchart_canvas.bind("<MouseWheel>", self._zoom_canvas)
        self.flowchart_canvas.bind("<Button-4>", self._zoom_canvas)  # Linux
        self.flowchart_canvas.bind("<Button-5>", self._zoom_canvas)  # Linux
        
        # Initialize zoom variables
        self.zoom_scale = 1.0  # current zoom level
        self.pan_start_x = 0  # pan start x coordinate
        self.pan_start_y = 0  # pan start y coordinate
    
    '''
    Updates line numbers in the line number widget
    '''
    def _update_line_numbers(self, event=None):
        # Get the number of lines in the text editor
        line_count = int(self.text_editor.index('end-1c').split('.')[0])
        
        # Generate line numbers
        line_numbers_string = '\n'.join(f'{i:>3}' for i in range(1, line_count + 1))
        
        # Update line numbers widget
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(1.0, line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    '''
    Handles content change events to update line numbers
    Arg:
        event - the event that triggered the change
    '''
    def _on_content_changed(self, event=None):
        # Schedule line number update after the event is processed
        self.text_editor.after_idle(self._update_line_numbers)
    
    '''
    Handles text editor scrolling and syncs with line numbers
    Args:
        *args - scrollbar arguments from text widget
    '''
    def _on_text_scroll(self, *args):
        # Update the scrollbar
        if hasattr(self.text_editor, 'vbar'):
            self.text_editor.vbar.set(*args)
        
        # Sync line numbers scrolling
        self.line_numbers.yview_moveto(args[0])
    
    '''
    Handles mouse wheel events to sync scrolling
    Arg:
        event - mouse wheel event
    '''
    def _on_mouse_wheel(self, event):
        # Let the text editor handle the scroll first
        self.text_editor.after_idle(lambda: self.line_numbers.yview_moveto(self.text_editor.yview()[0]))
    
    '''
    Displays the upload interface and hides the editor interface
    '''
    def _show_upload_screen(self):
        self.editor_frame.pack_forget()
        self.upload_frame.pack(fill=tk.BOTH, expand=True)
    
    '''
    Displays the editor interface and hides the upload interface
    '''
    def _show_editor_screen(self):
        self.upload_frame.pack_forget()
        self.editor_frame.pack(fill=tk.BOTH, expand=True)
    
    '''
    Handles file upload functionality
    Opens file dialog and loads .psc file content
    '''
    def _upload_file(self):
        file_types = [("Pseudocode files", "*.psc"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select Pseudocode File", filetypes=file_types)
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()  # file content to display in editor
                
                self.file_path = file_path
                self.is_file_loaded = True
                
                # Update tab name with filename
                filename = os.path.basename(file_path)  # extract filename from path
                self.tab_name = filename
                
                # Load content into editor
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                
                # Update line numbers
                self._update_line_numbers()
                
                # Switch to editor view
                self._show_editor_screen()
                
                # Update parent tab name
                if hasattr(self, 'parent_app'):
                    self.parent_app.update_tab_name(self, self.tab_name)
                    self.parent_app._update_all_tab_display()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    '''
    Clears all content from the pseudocode editor
    '''
    def _clear_editor(self):
        self.text_editor.delete(1.0, tk.END)
        self._update_line_numbers()
    
    '''
    Performs undo action in the text editor
    '''
    def _undo_action(self):
        try:
            self.text_editor.edit_undo()
            return "break"  # Prevent default handling
        except tk.TclError:
            pass  # No more undo actions available
        return "break"
    
    '''
    Performs redo action in the text editor
    '''
    def _redo_action(self):
        try:
            self.text_editor.edit_redo()
            return "break"  # Prevent default handling
        except tk.TclError:
            pass  # No more redo actions available
        return "break"
    
    '''
    Cuts selected text to clipboard
    '''
    def _cut_text(self):
        try:
            self.text_editor.event_generate("<<Cut>>")
            self.text_editor.after_idle(self._update_line_numbers)
        except tk.TclError:
            pass
    
    '''
    Copies selected text to clipboard
    '''
    def _copy_text(self):
        try:
            self.text_editor.event_generate("<<Copy>>")
        except tk.TclError:
            pass
    
    '''
    Pastes text from clipboard
    '''
    def _paste_text(self):
        try:
            self.text_editor.event_generate("<<Paste>>")
            self.text_editor.after_idle(self._update_line_numbers)
        except tk.TclError:
            pass
    
    '''
    Saves the current editor content to file
    '''
    def _save_file(self):
        if self.file_path:
            try:
                content = self.text_editor.get(1.0, tk.END)  # get all text content
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            self._save_file_as()
    
    '''
    Saves the editor content to a new file
    '''
    def _save_file_as(self):
        file_types = [("Pseudocode files", "*.psc"), ("All files", "*.*")]
        file_path = filedialog.asksaveasfilename(title="Save Pseudocode File", 
                                               filetypes=file_types, defaultextension=".psc")
        
        if file_path:
            try:
                content = self.text_editor.get(1.0, tk.END)  # get all text content
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.file_path = file_path
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    '''
    Generates flowchart from pseudocode content
    This is a placeholder for the actual flowchart generation logic
    '''
    def _generate_flowchart(self):
        content = self.text_editor.get(1.0, tk.END).strip()  # get text content without trailing newline
        
        if not content:
            messagebox.showwarning("Warning", "Please enter some pseudocode first!")
            return
        
        # Clear previous flowchart
        self.flowchart_canvas.delete("all")
        
        # Placeholder flowchart generation
        # TODO: Implement actual pseudocode parsing and flowchart generation
        self._draw_sample_flowchart()
        
        messagebox.showinfo("Generated", "Flowchart generated!")
    
    '''
    Draws a sample flowchart for demonstration
    '''
    # TODO: Replace this with actual flowchart drawing logic
    def _draw_sample_flowchart(self):
        # Set canvas scroll region
        self.flowchart_canvas.configure(scrollregion=(0, 0, 800, 600))
        
        # Start oval
        self.flowchart_canvas.create_oval(350, 50, 450, 100, fill="lightgreen", outline="black", width=2)
        self.flowchart_canvas.create_text(400, 75, text="Start", font=("Arial", 10, "bold"))
        
        # Process rectangle
        self.flowchart_canvas.create_rectangle(325, 150, 475, 200, fill="lightblue", outline="black", width=2)
        self.flowchart_canvas.create_text(400, 175, text="Process", font=("Arial", 10))
        
        # Decision diamond
        points = [400, 250, 475, 300, 400, 350, 325, 300]  # diamond coordinates
        self.flowchart_canvas.create_polygon(points, fill="lightyellow", outline="black", width=2)
        self.flowchart_canvas.create_text(400, 300, text="Decision?", font=("Arial", 10))
        
        # End oval
        self.flowchart_canvas.create_oval(350, 400, 450, 450, fill="lightcoral", outline="black", width=2)
        self.flowchart_canvas.create_text(400, 425, text="End", font=("Arial", 10, "bold"))
        
        # Connecting lines
        self.flowchart_canvas.create_line(400, 100, 400, 150, arrow=tk.LAST, width=2)
        self.flowchart_canvas.create_line(400, 200, 400, 250, arrow=tk.LAST, width=2)
        self.flowchart_canvas.create_line(400, 350, 400, 400, arrow=tk.LAST, width=2)
    
    '''
    Starts panning operation on flowchart canvas
    Arg:
        event - mouse click event
    '''
    def _start_pan(self, event):
        self.flowchart_canvas.scan_mark(event.x, event.y)
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    '''
    Performs panning operation on flowchart canvas
    Arg:
        event - mouse motion event
    '''
    def _do_pan(self, event):
        self.flowchart_canvas.scan_dragto(event.x, event.y, gain=1)
    
    '''
    Handles zoom functionality for flowchart canvas
    Arg:
        event - mouse wheel event
    '''
    def _zoom_canvas(self, event):
        # Determine zoom direction
        if event.delta > 0 or event.num == 4:
            zoom_factor = 1.1  # zoom in
        else:
            zoom_factor = 0.9  # zoom out
        
        # Apply zoom
        self.zoom_scale *= zoom_factor
        self.flowchart_canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)
        
        # Update scroll region
        self.flowchart_canvas.configure(scrollregion=self.flowchart_canvas.bbox("all"))

'''
Main application class for pseudocode to flowchart converter
Manages multiple tabs and overall application state
'''
class PseudocodeFlowchartApp:
    def __init__(self):
        self.root = tk.Tk()  # main application window
        self.tab_counter = 1  # counter for creating unique tab names
        
        self._setup_window()
        self._create_menu()
        self._create_notebook()
        self._create_first_tab()
    
    '''
    Sets up the main application window properties
    '''
    def _setup_window(self):
        self.root.title("Pseudocode to Flowchart Converter")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure styles
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  # Use default theme if clam is not available

        # Apply application color theme
        try:
            # Base background
            self.root.configure(background="#f7f9fc")

            # Frames and labels
            style.configure('TFrame', background="#f7f9fc")
            style.configure('TLabel', background="#f7f9fc", foreground="#1f2937")  # dark slate

            # Buttons
            style.configure('TButton', background="#e5eefb", foreground="#0b5394")
            style.map('TButton', background=[('active', '#d6e6fb')])

            # Generate button
            style.configure('Accent.TButton', background="#007acc", foreground="#ffffff")
            style.map('Accent.TButton', background=[('active', '#0062b3')])

            # Tabs
            style.configure('TNotebook', background="#f7f9fc")
            style.configure('TNotebook.Tab', background="#e6eef8", foreground="#374151")
            style.map('TNotebook.Tab',
                      background=[('selected', '#ffffff'), ('active', '#edf2fb')],
                      foreground=[('selected', '#0b5394')])

            # Scrollbars
            style.configure('TScrollbar', troughcolor="#e5e7eb", background="#c7d2fe", arrowcolor="#4b5563")
            style.map('TScrollbar', background=[('active', '#a5b4fc')])

            # Separators
            style.configure('TSeparator', background="#d1d5db")
        except tk.TclError:
            pass  # ignore if unsupported
    
    '''
    Creates the application menu bar
    '''
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tab", command=self._add_new_tab, accelerator="Ctrl+T / Cmd+T")
        file_menu.add_command(label="Open File", command=self._open_file, accelerator="Ctrl+O / Cmd+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self._save_current_file, accelerator="Ctrl+S / Cmd+S")
        file_menu.add_command(label="Save As...", command=self._save_as_current_file, accelerator="Ctrl+Shift+S / Cmd+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Close Tab", command=self._close_current_tab, accelerator="Ctrl+W / Cmd+W")
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q / Cmd+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Apply colors to menus
        try:
            menubar.configure(background="#f7f9fc", foreground="#1f2937",
                              activebackground="#e5eefb", activeforeground="#0b5394")
            file_menu.configure(background="#ffffff", foreground="#1f2937",
                                activebackground="#e5eefb", activeforeground="#0b5394")
            edit_menu.configure(background="#ffffff", foreground="#1f2937",
                                activebackground="#e5eefb", activeforeground="#0b5394")
        except tk.TclError:
            pass

        edit_menu.add_command(label="Undo", command=self._undo_current_tab, accelerator="Ctrl+Z / Cmd+Z")
        edit_menu.add_command(label="Redo", command=self._redo_current_tab, accelerator="Ctrl+Shift+Z / Cmd+Shift+Z / Ctrl+Y / Cmd+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self._cut_current_tab, accelerator="Ctrl+X / Cmd+X")
        edit_menu.add_command(label="Copy", command=self._copy_current_tab, accelerator="Ctrl+C / Cmd+C")
        edit_menu.add_command(label="Paste", command=self._paste_current_tab, accelerator="Ctrl+V / Cmd+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self._clear_current_tab)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-t>', lambda e: self._add_new_tab())
        self.root.bind('<Command-t>', lambda e: self._add_new_tab())
        self.root.bind('<Control-o>', lambda e: self._open_file())
        self.root.bind('<Command-o>', lambda e: self._open_file())
        self.root.bind('<Control-s>', lambda e: self._save_current_file())
        self.root.bind('<Command-s>', lambda e: self._save_current_file())
        self.root.bind('<Control-Shift-S>', lambda e: self._save_as_current_file())
        self.root.bind('<Command-Shift-S>', lambda e: self._save_as_current_file())
        self.root.bind('<Control-w>', lambda e: self._close_current_tab())
        self.root.bind('<Command-w>', lambda e: self._close_current_tab())
        self.root.bind('<Control-z>', lambda e: self._undo_current_tab())
        self.root.bind('<Command-z>', lambda e: self._undo_current_tab())
        self.root.bind('<Control-y>', lambda e: self._redo_current_tab())
        self.root.bind('<Command-y>', lambda e: self._redo_current_tab())
        self.root.bind('<Control-Shift-Z>', lambda e: self._redo_current_tab())
        self.root.bind('<Command-Shift-Z>', lambda e: self._redo_current_tab())
        self.root.bind('<Control-x>', lambda e: self._cut_current_tab())
        self.root.bind('<Command-x>', lambda e: self._cut_current_tab())
        self.root.bind('<Control-c>', lambda e: self._copy_current_tab())
        self.root.bind('<Command-c>', lambda e: self._copy_current_tab())
        self.root.bind('<Control-v>', lambda e: self._paste_current_tab())
        self.root.bind('<Command-v>', lambda e: self._paste_current_tab())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Command-q>', lambda e: self.root.quit())
    
    '''
    Creates the notebook widget for managing tabs
    '''
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind tab selection event for enhanced highlighting
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.notebook.bind("<Button-1>", self._on_tab_click_highlight)
    
    '''
    Creates the initial tab when application starts
    '''
    def _create_first_tab(self):
        self._add_new_tab()
        self._update_all_tab_display()
    
    '''
    Adds a new tab to the notebook
    '''
    def _add_new_tab(self):
        tab_name = f"Tab {self.tab_counter}"  # default tab name
        new_tab = FlowchartTab(self.notebook, tab_name)
        
        # Create tab with close functionality
        self.notebook.add(new_tab.main_frame, text=tab_name)
        
        # Store reference to tab object
        if not hasattr(self.notebook, 'tab_objects'):
            self.notebook.tab_objects = {}
        self.notebook.tab_objects[new_tab.main_frame] = new_tab
        
        # Set up the parent reference for tab name updating
        new_tab.parent_app = self

        self.notebook.select(new_tab.main_frame)  # Select the new tab
        self.tab_counter += 1  # Increment counter
        self._update_all_tab_display()
        
        # Bind click events for tab management
        self.notebook.bind("<Button-2>", self._close_tab_on_click)  # Middle click
        self.notebook.bind("<Button-3>", self._show_tab_context_menu)  # Right click
    
    '''
    Closes tab on middle-click
    Arg:
        event - mouse click event
    '''
    def _close_tab_on_click(self, event):
        tab_index = self.notebook.index(f"@{event.x},{event.y}")  # get tab index from mouse position
        if tab_index is not None:
            self._close_tab(tab_index)
    
    '''
    Shows context menu for tab operations
    Arg:
        event - right-click event
    '''
    def _show_tab_context_menu(self, event):
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")  # get tab index from mouse position
            if tab_index is not None:
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(label="Close Tab", command=lambda: self._close_tab(tab_index))
                context_menu.add_command(label="Close Other Tabs", command=lambda: self._close_other_tabs(tab_index))
                context_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass  # Click was not on a tab
    
    '''
    Closes the specified tab
    Arg:
        tab_index - index of tab to close
    '''
    def _close_tab(self, tab_index):
        total_tabs = self.notebook.index("end")
        
        if total_tabs > 1:  # Don't close if it's the only tab
            tab_widget = self.notebook.nametowidget(self.notebook.tabs()[tab_index])
            
            # Clean up tab object reference
            if hasattr(self.notebook, 'tab_objects'):
                self.notebook.tab_objects.pop(tab_widget, None)
            
            self.notebook.forget(tab_index)
        else:
            messagebox.showinfo("Info", "Cannot close the last tab!")
            
        self._update_all_tab_display()  # Update remaining tabs display
    
    '''
    Closes all tabs except the specified one
    Arg:
        keep_tab_index - index of tab to keep open
    '''
    def _close_other_tabs(self, keep_tab_index):
        tabs_to_close = []  # list of tab indices to close
        total_tabs = self.notebook.index("end")  # total number of tabs
        
        for i in range(total_tabs):
            if i != keep_tab_index:
                tabs_to_close.append(i)
        
        # Close tabs in reverse order to maintain correct indices
        for tab_index in reversed(tabs_to_close):
            tab_widget = self.notebook.nametowidget(self.notebook.tabs()[tab_index])
            
            # Clean up tab object reference
            if hasattr(self.notebook, 'tab_objects'):
                self.notebook.tab_objects.pop(tab_widget, None)
            
            self.notebook.forget(tab_index)
        
        self._update_all_tab_display()  # Update remaining tab display
    
    '''
    Handles tab selection change event
    Arg:
        event - tab change event
    '''
    def _on_tab_changed(self, event):
        # Update window title with current tab name
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    self.root.title(f"Pseudocode to Flowchart Converter - {tab_object.tab_name}")
        except tk.TclError:
            pass
    
    '''
    Handles tab click for visual feedback
    Arg:
        event - click event
    '''
    def _on_tab_click_highlight(self, event):
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")  # Get the clicked tab index
            if tab_index is not None:
                self.notebook.after_idle(lambda: self._refresh_tab_styles())  # Force a visual update to ensure proper highlighting
        except (tk.TclError, TypeError):
            pass
    
    '''
    Refreshes tab styles to ensure proper highlighting
    '''
    def _refresh_tab_styles(self):
        try:
            current_selection = self.notebook.index("current")  # Get current selection
            self.notebook.after(1, lambda: self.notebook.event_generate("<<NotebookTabChanged>>"))  # Force style update by briefly changing and restoring
        except tk.TclError:
            pass
    
    '''
    Updates the display name of a tab
    Arg:
        tab_object - the FlowchartTab object
        new_name - new name for the tab
    '''
    def update_tab_name(self, tab_object, new_name):
        try:
            for tab_widget in self.notebook.tabs():
                widget = self.notebook.nametowidget(tab_widget)
                if hasattr(self.notebook, 'tab_objects'):
                    if self.notebook.tab_objects.get(widget) == tab_object:
                        display_name = new_name.replace('.psc', '') if new_name.endswith('.psc') else new_name
                        self.notebook.tab(tab_widget, text=f"{display_name}")
                        tab_object.tab_name = new_name
                        
                        # Update window title if this is the current tab
                        if self.notebook.select() == tab_widget:
                            self.root.title(f"Pseudocode to Flowchart Converter - {display_name}")
                        break
        except tk.TclError:
            pass
    
    '''
    Updates display of all tabs
    '''
    def _update_all_tab_display(self):
        try:
            total_tabs = self.notebook.index("end")
            for i, tab_widget in enumerate(self.notebook.tabs()):
                widget = self.notebook.nametowidget(tab_widget)
                if hasattr(self.notebook, 'tab_objects'):
                    tab_object = self.notebook.tab_objects.get(widget)
                    if tab_object:
                        current_text = self.notebook.tab(tab_widget, "text")
        except tk.TclError:
            pass
    
    '''
    Opens a file in the current tab
    '''
    def _open_file(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._upload_file()
        except tk.TclError:
            pass
    
    '''
    Saves the file in the current tab
    '''
    def _save_current_file(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._save_file()
        except tk.TclError:
            pass

    '''
    Closes the currently selected tab (if more than one tab is open)
    '''
    def _close_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab:
                tab_index = self.notebook.index(current_tab)
                self._close_tab(tab_index)
        except tk.TclError:
            pass
    
    '''
    Performs undo in the current tab
    '''
    def _undo_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._undo_action()
        except tk.TclError:
            pass
    
    '''
    Performs redo in the current tab
    '''
    def _redo_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._redo_action()
        except tk.TclError:
            pass
    
    '''
    Clears all text in the current tab
    '''
    def _clear_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._clear_editor()
        except tk.TclError:
            pass
    
    '''
    Saves the current file with a new name (Save As)
    '''
    def _save_as_current_file(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._save_file_as()
        except tk.TclError:
            pass
    
    '''
    Cuts selected text in the current tab
    '''
    def _cut_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._cut_text()
        except tk.TclError:
            pass
    
    '''
    Copies selected text in the current tab
    '''
    def _copy_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._copy_text()
        except tk.TclError:
            pass
    
    '''
    Pastes text from clipboard in the current tab
    '''
    def _paste_current_tab(self):
        try:
            current_tab = self.notebook.select()
            if current_tab and hasattr(self.notebook, 'tab_objects'):
                tab_widget = self.notebook.nametowidget(current_tab)
                tab_object = self.notebook.tab_objects.get(tab_widget)
                if tab_object:
                    tab_object._paste_text()
        except tk.TclError:
            pass
    
    '''
    Starts the main application loop
    '''
    def run(self):
        self.root.mainloop()

'''
Main entry point for the application
Creates and runs the pseudocode flowchart converter
'''
def main():
    app = PseudocodeFlowchartApp()  # create main application instance
    app.run()


if __name__ == "__main__":
    main()