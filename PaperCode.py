#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

from pytesseract import image_to_string

class PaperCode:

    def __init__(self, img_path):

        self.text = self._extract_text(img_path)

    def _extract_text(self, img_path):
        return image_to_string(img_path)

    def run(self):
        exec(self.text)


if __name__ == '__main__':

    from tkinter import Tk, filedialog

    root = Tk(); root.withdraw()

    img_path = filedialog.askopenfilename()

    root.destroy()

    code = PaperCode(img_path)
    code.run()
