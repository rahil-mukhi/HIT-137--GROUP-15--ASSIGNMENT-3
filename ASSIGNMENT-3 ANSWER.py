# GROUP NAME : CAS/DAN GROUP-15
# GROUP MEMBERS: 385218 RAHIL MUKHI
#                374427 RENISH VEKARIYA
#                384646 RUHINA RAJABALI
#                383635 RUSHABHKUMAR SAVAJ

# Importing Required Libraries
from tkinter import *
from tkinter import filedialog,ttk
import cv2
from PIL import ImageTk, Image

class ImageEditor:
    # Creating _init_ method which will get executed at object creation time
    def __init__(self,root):
        self.root = root
        self.root.title("Python Image Editor - CAS/DAN Group = 15")
        self.root.geometry("1200x800")

        self.original_image = None
        self.modified_image = None
        self.filename = None

        # We will use two stacks for Undo / Redo functionality
        self.undo_stack = []
        self.redo_stack = []

        # Attributes for cropping Function
        self.crop_mode = None
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_id = None

        self.main_ui()

    def main_ui(self):

        # Top container will hold two canvas for original and modified images
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Canvas to show original Image
        self.canvas_original = Canvas(self.canvas_frame, width=350, height=350, bg="gray")
        self.canvas_original.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # Canvas to show modified Image
        self.canvas_modified = Canvas(self.canvas_frame, width=350, height=350, bg="gray")
        self.canvas_modified.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # Creating Frame for buttons and slider
        self.button_frame = Frame(self.root,padx=20, pady=10)
        self.button_frame.pack(fill=X)

        # Adding Buttons and Slider
        select_image_button = Button(self.button_frame, text="Select Image", command=self.select_image)
        select_image_button.pack(side=LEFT, padx=5)
        crop_button = Button(self.button_frame, text="Crop", command=self.crop)
        crop_button.pack(side=LEFT, padx=5)
        grayscale_button = Button(self.button_frame, text="Grayscale", command=self.grayscale)
        grayscale_button.pack(side=LEFT, padx=5)
        rotate_button = Button(self.button_frame, text="Rotate", command=self.rotate)
        rotate_button.pack(side=LEFT, padx=5)
        undo_button = Button(self.button_frame, text="Undo", command=self.undo)
        undo_button.pack(side=LEFT, padx=5)
        redo_button = Button(self.button_frame, text="Redo", command=self.redo)
        redo_button.pack(side=LEFT, padx=5)
        self.zoom_slider = Scale(self.button_frame, label="Zoom Image", from_=25, to=125, orient=HORIZONTAL, length=300, command=self.slider)
        self.zoom_slider.set(75)
        self.zoom_slider.pack(side=LEFT, padx=10)
        save_image_button = Button(self.button_frame, text="Save Image", command=self.save_image)
        save_image_button.pack(side=LEFT, padx=5)

        instructions = Label(self.root, text=
            '''Instructions:                                                                                                                                Shortcuts:
            1. Select image to edit.                                                                                                            Select Image = Control + O      Undo = Control + Z
            2. View the original image on left and make changes to right image.                                 Crop = Control + C                    Redo = Control + Y
            3. Use functionality like Crop, Grayscale, or Rotate to edit image.                                     Grayscale = Control + G            Save Image = Control + S
            4. Use Undo/Redo, Zoom, and save your image.                                                                  Rotate = Control + R
            5. Use keyboard shortcuts for faster operations!''',
            justify=LEFT,
            padx=10
        )
        instructions.pack(pady=10)

        # Adding Keyboard Shortcuts
        self.root.bind("<Control-o>", lambda event: self.select_image())
        self.root.bind("<Control-c>", lambda event: self.crop())
        self.root.bind("<Control-g>", lambda event: self.grayscale())
        self.root.bind("<Control-r>", lambda event: self.rotate())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-s>", lambda event: self.save_image())