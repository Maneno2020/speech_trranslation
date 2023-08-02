import tkinter
from tkinter import *
from tkinter import messagebox

import phonenumbers
import tkintermapview
from opencage.geocoder import OpenCageGeocode
from phonenumbers import carrier
from phonenumbers import geocoder
from tkinter.ttk import *

key = '6d39e59b395343798debb9253dc01f39'
root = tkinter.Tk()
root.geometry("500x500")

label1 = Label(text="Enter the phone number to track")
label1.pack()


def getResult():
    num = number.get("1.0", END)

    try:
        num1 = phonenumbers.parse(num)
    except:
        messagebox.showerror("Error", "Number box is empty or non numeric character was used")

    location = geocoder.description_for_number(num1, "en")
    service_provider = carrier.name_for_number(num1, "en")

    ocg = OpenCageGeocode(key)
    querry = str(location)
    results = ocg.geocode(querry)

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    my_label = LabelFrame(root)
    my_label.pack(pady=10)

    map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
    map_widget.set_position(lat, lng)
    map_widget.set_marker(lat, lng, text="Phone number location")
    map_widget.set_zoom(10)
    map_widget.place(relx=1.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack()

    adr = tkintermapview.convert_coordinates_to_address(lat,lng)

    result.insert(END, "The Country of this number is:" + location)
    result.insert(END, "\nThe sim card for this number is:" + service_provider)

    result.insert(END, "\nLatitude is: " + str(lat))
    result.insert(END, "\nLongitude is: " + str(lng))

    # result.insert(END, "\nStreet address is: " + adr.Street)
    # result.insert(END, "\nCity Address is: " + adr.city)
    # result.insert(END, "\nPostal Address is: " + adr.postal)


number = Text(height=1)
number.pack()

style = Style()
style.configure("TButton", font=('calibri', 20, 'bold'), borderwidth=4)
style.map('TButton', foreground=[('active', '!disabled', 'green')],
          background=[('active', 'black')])
button = Button(text="Track number", command=getResult)
button.pack(pady=10, padx=100)

result = Text(height=10)
result.pack()

root.mainloop()
