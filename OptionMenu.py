#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Scott Thomson <scotty3785@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import Tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.om_variable = tk.StringVar(self)

        b1 = tk.Button(self, text="Colors", width=8, command=self.use_colors)
        b2 = tk.Button(self, text="Sizes", width=8, command=self.use_sizes)

        self.om = tk.OptionMenu(self, self.om_variable, ())
        self.om.configure(width=20)
        self.use_colors()

        b1.pack(side="left")
        b2.pack(side="left")
        self.om.pack(side="left", fill="x", expand=True)


    def _reset_option_menu(self, options, index=None):
        '''reset the values in the option menu

        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = self.om["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  self.om_variable.set(value))
        if index is not None:
            self.om_variable.set(options[index])

    def use_colors(self):
        '''Switch the option menu to display colors'''
        self._reset_option_menu(["red","orange","green","blue"], 0)

    def use_sizes(self):
        '''Switch the option menu to display sizes'''
        self._reset_option_menu(["x-small", "small", "medium", "large"], 0)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


def main():
	
	return 0

if __name__ == '__main__':
	main()

