#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import subprocess

from pytesseract import image_to_string
from tkinter import Tk, filedialog
from shutil import which

class PaperCode:

    def __init__(self, img_path, language='python'):

        # Get text from image
        self.text = image_to_string(img_path)

        # List of languages supported with execute command and file extension
        self.lang_support = ( 5,    # Number of supported languages
            ('python',  lambda: exec(self.text),                                                    'py'),
            ('bash',    lambda: subprocess.run(self.text, shell=True, executable='/bin/bash'),      'sh'),
            ('lua',     lambda: subprocess.run(['lua', '-e', 'loadstring([['+self.text+']])()']),   'lua'),
            ('perl',    lambda: subprocess.run('perl -e \'{'+self.text+'}\'', shell=True),          'pl'),
            ('ruby',    lambda: subprocess.run('ruby -e \'('+self.text+')\'', shell=True),          'rb')
        )

        # Check if the language is supported
    
        self.language = None

        for i in range(self.lang_support[0]):
            if  language == self.lang_support[i+1][0] \
                and which(self.lang_support[i+1][0]) != None:
                    self.language = self.lang_support[i+1]; break

        if self.language == None:
            print("Warning: this language cannot be executed.")
            extension = input('What file extension do you want for your file (def: ".txt"): ') or '.txt'
            self.language = (language, None, extension)

        # We remove the last character which can cause problems at runtime.
        l=len(self.text); self.text = self.text[:l-1]

    def run(self):

        # Exectuion of script #
        if not (self.language[1] == None):
            self.language[1]()

        else: # Not compatible #
            print("Warning: this language cannot be executed.\nInfo: You can export the file with ' PaperCode.export() '.")


    def export(self, name='PaperCode_export'):

        root=Tk(); root.withdraw()
        export_path = filedialog.askdirectory()
        root.destroy()

        if export_path != '':
            export_path = f'{export_path}/{name}.{self.language[2]}'
            export_file = open(export_path, 'w')
            export_file.write(self.text)
            export_file.close()

            print("Info: File exported to \""+export_path+"\"")


if __name__ == '__main__':

    root = Tk(); root.withdraw()
    img_path = filedialog.askopenfilename()
    root.destroy()

    lang = input('What is the language to be executed (def: python): ') or 'python'

    code = PaperCode(img_path, lang)
    code.run() # code.export('name_file')
