import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Im2ASCII")
    root.geometry("400x200")

    button = tk.Button(root, text = "Click Me!", command = root.destroy)

    button.pack(padx = 20, pady = 20)

    root.mainloop()


if __name__ == "__main__":
    main()

