import io
import os
import numpy as np
import itertools as it
from PIL import Image as pil
from PIL import ImageTk

class Image:
    def __init__(self):
        pass
    
    def getImage(self):
        return self.image

    def getFileName(self):
        return self.filename

    def getResolution(self):
        return self.resolution

    def getRedChannel(self):
        return self.redChannel

    def getGreenChannel(self):
        return self.greenChannel

    def getBlueChannel(self):
        return self.blueChannel
    
    def setImage(self, _filename):
        self.image = pil.open(_filename)

    def setFileName(self, _filename):
        self.filename = _filename
    
    def setResolution(self, _resolution):
        #Resolução da imagem (width, height)
        self.resolution = _resolution

    def setRedChannel(self, _redChannel):
        self.redChannel = _redChannel

    def setGreenChannel(self, _greenChannel):
        self.greenChannel = _greenChannel
        
    def setBlueChannel(self, _blueChannel):
        self.blueChannel = _blueChannel

    def separate_RGB_Channels(self, _img):
        img = self.getImage()

        # Converte a imagem para 'RGB'
        rgb_img = img.convert('RGB')

        r, g, b =  [], [], []
        width, height = rgb_img.size
        self.setResolution((width, height))
        i = 0
        j = 0

        while i < width:
            while j < height:
                # Separa os canais RGBs em listas (com PIL)
                r.append(rgb_img.getpixel((i, j))[0])
                g.append(rgb_img.getpixel((i, j))[1])
                b.append(rgb_img.getpixel((i, j))[2])
                j+=1
            j=0
            i+=1

        self.setRedChannel(r)
        self.setGreenChannel(g)
        self.setBlueChannel(b)

    def generate_thumbnail(self, _img, first = False):
        """Generate image data using PIL
        """
        maxsize = (320, 320)
        #img = pil.fromarray(_img, 'RGB')
        img = pil.frombytes('RGB', (512, 512), _img, decoder_name="raw")
        #img = pil.frombuffer('RGB', (512, 512), _img)
        img = img.transpose(pil.TRANSPOSE)
        img.show()
        img.save('teste.bmp')
        img.thumbnail(maxsize)

        if first:                     # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
            
        del maxsize
        return ImageTk.PhotoImage(img)

    def normalize(self, r, g, b):
        fmax, fmin = max(max(r), max(g), max(b)), min(min(r), min(g), min(b))
        print(fmax, fmin)
        auxR = [np.uint8(((255/(fmax - fmin))*(i - fmin))) for i in r]
        auxG = [np.uint8(((255/(fmax - fmin))*(i - fmin))) for i in g]
        auxB = [np.uint8(((255/(fmax - fmin))*(i - fmin))) for i in b]
        del fmin, fmax
        return (auxR, auxG, auxB)

    def apply_operations(self, _img1, _img2, _ops):
        img_temp = Image()
        if _ops['-ADD-']:
            img_temp = self.add_operation(_img1, _img2)
        elif _ops['-SUB-']:
            img_temp = self.sub_operation(_img1, _img2)
        elif _ops['-MUL-']:
            img_temp = self.mult_operation(_img1, _img2)
        elif _ops['-DIV-']:
            img_temp = self.div_operation(_img1, _img2)
        elif _ops['-AND-']:
            img_temp = self.and_operation(_img1, _img2)
        elif _ops['-OR-']:
            img_temp = self.or_operation(_img1, _img2)
        elif _ops['-NOT-']:
            img_temp = self.not_operation(_img1)
        return img_temp

    def add_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) + int(y) for x, y in it.zip_longest(r1, r2, fillvalue=0)]
        temp_g = [int(x) + int(y) for x, y in it.zip_longest(g1, g2, fillvalue=0)]
        temp_b = [int(x) + int(y) for x, y in it.zip_longest(b1, b2, fillvalue=0)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(max(_img1.getResolution()[0], _img2.getResolution()[0]), max(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def sub_operation(self, _img1, _img2):
        arr_img_result = None

        # Get dos canais já setados
        r1, g1, b1 = _img1.getRedChannel(), _img1.getGreenChannel(), _img1.getBlueChannel()
        r2, g2, b2 = _img2.getRedChannel(), _img2.getGreenChannel(), _img2.getBlueChannel()

        temp_r = [int(x) - int(y) for x, y in it.zip_longest(r1, r2, fillvalue=0)]
        temp_g = [int(x) - int(y) for x, y in it.zip_longest(g1, g2, fillvalue=0)]
        temp_b = [int(x) - int(y) for x, y in it.zip_longest(b1, b2, fillvalue=0)]

        temp_r, temp_g, temp_b = self.normalize(temp_r, temp_g, temp_b)

        arr_img_result = np.dstack([temp_r, temp_g, temp_b])
        arr_img_result = np.asarray(arr_img_result)

        arr_img_result = arr_img_result.reshape(max(_img1.getResolution()[0], _img2.getResolution()[0]), max(_img1.getResolution()[1], _img2.getResolution()[1]), 3)

        return arr_img_result

    def mult_operation(self, _img1, _img2):
        print("Multiplicação")

    def div_operation(self, _img1, _img2):
        print("Divisão")

    def and_operation(self, _img1, _img2):
        print("AND")

    def or_operation(self, _img1, _img2):
        print("OR")

    def not_operation(self, _img1):
        print("NOT")