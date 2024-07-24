import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd

import im2ascii as i2a

from os import path

def main():
    root = tk.Tk()
    root.title("Im2ASCII")

    input_path = tk.StringVar(value = "Image not selected")
    output_path = tk.StringVar(value = "output.txt")

    def no_file_selected():
        """
        A pop up window that appears when the user doesn't select an input image
        and attempts to convert.
        """
        popup = tk.Tk()
        popup.title("")
        label = ttk.Label(popup, text = "Please select a file!")
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Continue", command = popup.destroy)
        B1.pack()
        popup.mainloop()


    def get_file_name():
        """
        Callback function that retrieves the input image filename.
        """
        filename = fd.askopenfilename()
        if len(filename) == 0:
            filename = "Image not selected"
        input_path.set(filename)
        output_path.set(
            path.dirname(input_path.get()) + path.basename(input_path.get()).stem
        )

        print(output_path.get())
        file_picker_label.configure(text = input_path.get())
    
    def initiate_convert():
        """
        Callback function that collects all the provided inputs, parses them and
        sends them to the im2ASCII function.
        """
        inp = input_path.get()
        out = output_path.get()
        width = output_entry.get()

        if inp == "Image not selected":
            no_file_selected()
            return

        flags = {}
        if width != "":
            flags["-w"] = width
        
        flag_list = []

        for k, v in flags.items():
            flag_list += [k, v]

        i2a.main(["dummy", inp, out] + flag_list)



    file_picker_button = ttk.Button(root, text = "Select an image", command=get_file_name)
    file_picker_label = ttk.Label(root, text = input_path.get(), anchor = "e", justify=tk.LEFT)

    width_label = tk.Label(root, text="Enter output image width (optional):")
    width_entry = tk.Entry(root)

    output_label = tk.Label(root, text="Enter output image name (optional):")
    output_entry = tk.Entry(root)

    convert_button = tk.Button(root, text = "Convert!", command=initiate_convert)

    file_picker_label.grid(column = 0, row = 0, padx = 20, pady = 20)
    file_picker_button.grid(column = 1, row = 0, padx = 20, pady = 20)
    width_label.grid(column = 0, row = 1, padx = 20, pady = 20)
    width_entry.grid(column = 1, row = 1, padx = 20, pady = 20)
    output_label.grid(column = 0, row = 2, padx = 20, pady = 20)
    output_entry.grid(column = 1, row = 2, padx = 20, pady = 20)

    convert_button.grid(column = 1, row = 3, padx = 20, pady = 20)

    root.mainloop()


if __name__ == "__main__":
    main()

