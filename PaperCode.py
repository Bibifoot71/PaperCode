#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import subprocess

from pytesseract import image_to_string
from tkinter import Tk, filedialog
from shutil import which

class PaperCode:

    def __init__(self, img_path, language='python'):

        self.text = image_to_string(img_path)

        # Check if the language is supported
        self._check_languages(); self.language = None
        for i in range(self.supported_languages[0]):
            if language == self.supported_languages[i+1]:
                self.language = language; break

        # If not compatible
        if self.language == None:
            print("Warning: this language cannot be executed.")

        # We remove the last character which can cause problems at runtime.
        l=len(self.text); self.text = self.text[:l-1]


    def _check_languages(self):

        self.supported_languages = [5,'python'] # [0]: Total of supported languages

        lang_list = ('bash', 'lua', 'perl', 'ruby')

        for i in range(self.supported_languages[0]-1):

            if not (which(lang_list[i]) == None):
                  self.supported_languages.append(lang_list[i])
            else: self.supported_languages.append(False)


    def run(self):

        # Python #
        if   self.language == self.supported_languages[1]: exec(self.text)

        # Bash #
        elif self.language == self.supported_languages[2]: subprocess.run(
            self.text, shell=True, executable='/bin/bash'
        )

        # Lua #
        elif self.language == self.supported_languages[3]: subprocess.run(
            ['lua', '-e', 'loadstring([['+self.text+']])()']
        )

        # Perl #
        elif self.language == self.supported_languages[4]: subprocess.run(
            'perl -e \'{'+self.text+'}\'', shell=True
        )

        # Ruby #
        elif self.language == self.supported_languages[5]: subprocess.run(
            'ruby -e \'('+self.text+')\'', shell=True
        )

        else: # Not compatible #
            print("Warning: this language cannot be executed.\nInfo: You can export the file with ' PaperCode.export() '.")


    def export(self, name='PaperCode_export'):

        root=Tk(); root.withdraw()
        export_path = filedialog.askdirectory()
        root.destroy()

        if export_path != '':

            if   self.language == self.supported_languages[1]: extension = 'py'
            elif self.language == self.supported_languages[2]: extension = 'sh'
            elif self.language == self.supported_languages[3]: extension = 'lua'
            elif self.language == self.supported_languages[4]: extension = 'pl'
            elif self.language == self.supported_languages[5]: extension = 'rb'

            export_path = f'{export_path}/{name}.{extension}'
            export_file = open(export_path, 'w')
            export_file.write(self.text)

            print("Info: File exported to \""+export_path+"\"")



if __name__ == '__main__':

    root = Tk(); root.withdraw()
    img_path = filedialog.askopenfilename()
    root.destroy()

    lang = input('What is the language to be executed (def: python): ') or 'python'

    code = PaperCode(img_path, lang)
    code.run() # code.export('name_file')
