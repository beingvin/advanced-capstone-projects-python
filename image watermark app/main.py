from tkinter import Image, Tk, filedialog
from PIL import Image, ImageDraw, ImageFont
window = Tk()
window.withdraw()

filename = filedialog.askopenfilename(initialdir="images/", title="Select Image")

def addWatermark(image, wm_text):
    # Create image object
    opened_image = Image.open(image)

    #Get image size
    image_width, image_height = opened_image.size

    #Draw on image 
    draw = ImageDraw.Draw(opened_image)

    #Specify a font size
    font_size = 50

    #Specify a font size and font size
    font = ImageFont.truetype("arial.ttf", font_size)

    #Specify image location
    x, y = 20, 50
    
    #Add watermark
    draw.text((x, y), wm_text, font= font , fill='#FFF', stroke_width=5, stroke_fill='#222', another='ms')

    #Show the new image
    opened_image.show()


addWatermark(filename, 'watermark')