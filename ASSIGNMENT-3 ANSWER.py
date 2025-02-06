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
def select_image(self):
        # Opens file manager to select a File
        self.filename = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")],
        )
        if not self.filename:
            return

        # Loading the image using OpenCV
        self.original_image = cv2.imread(self.filename)
        if self.original_image is None:
            print("Error! Image not Loaded!")
            return

        # Remove previous image and clear undo/redo Stacks
        self.modified_image = None
        self.undo_stack.clear()
        self.redo_stack.clear()

        # Display the selected image
        self.display_image()

    def display_image(self):
        if self.original_image is None:
            print("Error! Image not Loaded!")
            return

        # Set Slider Value
        slider_value = self.zoom_slider.get() if hasattr(self, "zoom_slider") else 100
        factor = slider_value / 100

        # Display Original Image
        original_image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        original_height, original_width, original_channels = original_image_rgb.shape

        # We try to resize image so that it fits in canvas of size 600x600
        original_scale = min(600/original_width, 600/original_height, 1)
        original_preview_scale = original_scale * factor
        preview_original_width = int(original_width * original_preview_scale)
        preview_modified_height = int(original_height * original_preview_scale)
        preview_original_image = cv2.resize(original_image_rgb, (preview_original_width, preview_modified_height), interpolation=cv2.INTER_AREA)

        # Display Original Image in left Canvas
        self.tk_original_image = ImageTk.PhotoImage(image=Image.fromarray(preview_original_image))
        self.canvas_original.config(width=preview_original_width, height=preview_modified_height)
        self.canvas_original.delete("all")
        self.canvas_original.create_image(preview_original_width // 2, preview_modified_height // 2, image=self.tk_original_image)      # It places image in the center of canvas

        # Loading Modified Image
        if self.modified_image is None:
            image_to_show = self.original_image
        else:
            image_to_show = self.modified_image
        modified_image_rgb = cv2.cvtColor(image_to_show, cv2.COLOR_BGR2RGB)

        # We try to resize image so that it fits in canvas of size 600x600
        modified_height, modified_width, modified_channels = modified_image_rgb.shape
        modified_scale = min(600/modified_width, 600/modified_height, 1)
        modified_preview_scale = modified_scale * factor
        preview_modified_width = int(modified_width * modified_preview_scale)
        preview_modified_height = int(modified_height * modified_preview_scale)
        preview_modified_image = cv2.resize(modified_image_rgb, (preview_modified_width, preview_modified_height), interpolation=cv2.INTER_AREA)

        # Display Modified Image in Right Canvas
        self.tk_modified_image = ImageTk.PhotoImage(Image.fromarray(preview_modified_image))
        self.canvas_modified.config(width=preview_modified_width, height=preview_modified_height)
        self.canvas_modified.delete("all")
        self.canvas_modified.create_image(preview_modified_width // 2, preview_modified_height // 2, image=self.tk_modified_image)      # It places Image in center of canvas

        # Saving the preview dimensions
        self.preview_dimensions = (preview_modified_width, preview_modified_height)
        self.ratio = modified_width / preview_modified_width if preview_modified_width != 0 else 1

    def crop(self):
        if self.original_image is None and self.modified_image is None:
            print("Error! No Image available to Crop!")
            return
        self.crop_mode = True

        # Binding mouse clicks for crop action on right canvas
        self.canvas_modified.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas_modified.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas_modified.bind("<ButtonRelease-1>", self.on_button_release)
        print("Crop mode activated. Click and drag on Right canvas to select the area.")

    def on_button_press(self, event):
        # Record the starting position for Crop action
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        if self.crop_id:
            self.canvas_modified.delete(self.crop_id)
            self.crop_id = None

    def on_mouse_move(self, event):
        # Updating the crop rectangle as the mouse is dragged
        if not self.crop_mode:
            return
        current_x, current_y = event.x, event.y
        if self.crop_id is None:
            self.crop_id = self.canvas_modified.create_rectangle(self.crop_start_x, self.crop_start_y, current_x, current_y, outline="red", width=2)
        else:
            self.canvas_modified.coords(self.crop_id, self.crop_start_x, self.crop_start_y, current_x, current_y)