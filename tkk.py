def pop_window(content):
    #弹窗，显示content里的内容
    import tkinter as tk
    from tkinter import messagebox        #引入弹窗库
    window=tk.Tk()
    window.title('error')
    window.attributes("-alpha", 0.0)
    window.geometry('0x0')
    messagebox.showinfo(title='error',message=content)

i = 1
print (type(i)==int)