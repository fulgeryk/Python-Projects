from tkinter import *

window = Tk()
window.title("Mile to Km Converter")
window.minsize(300,100)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

def convert_miles_into_km():
    miles = input.get()
    km = int(int(miles) * (16/10))
    label_show.config(text=str(km))


#Entry
input=Entry(width=10)
input.grid(column=1, row=0)

#Label_Miles
label_miles = Label(text="Miles", font=("Arial", 12 ,"bold"))
label_miles.grid(column=2, row=0)

#Label_is equal to
label_equal = Label(text="is equal to", font=("Arial", 12 ,"bold"))
label_equal.grid(column=0, row=1)

#Label afisare
label_show = Label(text="0", font=("Arial", 12 ,"bold"))
label_show.grid(column=1, row=1)

#Label Km
label_km = Label(text="Km", font=("Arial", 12 ,"bold"))
label_km.grid(column=2, row=1)

#Button Calculate
calculate_button = Button(text="Calculate", command=convert_miles_into_km)
calculate_button.grid(column=1,row=2)

window.mainloop()