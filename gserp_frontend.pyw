from tkinter import *
from tkinter import ttk
from apify_client import ApifyClient
import re
import sys
from threading import Thread
import os

def fetch_links(query):
    client = ApifyClient("") #your apify key
    # Prepare the actor input
    run_input = {
        #"queries": "write for me + travel",
        "queries": query,
        "maxPagesPerQuery": 1,
        "resultsPerPage": 100,
        "countryCode": "",
        "customDataFunction": """async ({ input, $, request, response, html }) => {
        return {
        pageTitle: $('title').text(),
        };
        };""",
    }
    # Run the actor and wait for it to finish
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)

    total_items = 0

    # Fetch and print actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results = item.get('organicResults', None)
        with open('./formatted-links.txt', 'w') as f:
            for item in results:
                url = item.get('url', None)
                #print(url)
                x = re.search("^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)", url) 
                f.write(x.group())
                f.write('\n')
                total_items + 1
        f.close()
    os._exit(0)
    

def function(root, widget, widget2, input):
    query = input()
    thread = Thread(target=fetch_links, args=(query, ))
    widget.grid_forget()
    widget2.grid_forget()
    pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280)
    # place the progressbar
    pb.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
    thread.start()
    pb.start()
    
root = Tk()
photo = PhotoImage(file = "./resources/logo.png")
main = PhotoImage(file = "./resources/main.png")
root.iconphoto(False, photo)
root.title("GSERP Formatted")
root.geometry("540x240")
frm = ttk.Frame(root)
frm.grid()
#label
#ttk.Label(frm, text="Enter search keywords: ").grid(column=0, row=0)
#input
splash = Label(frm, image=main)
splash.grid(column=0, row=0)
input = StringVar()
input_entry = ttk.Entry(frm, textvariable=input, cursor="hand2", font=('roboto', 20), justify=CENTER)
input_entry.grid(column=0, row=1, sticky=(W, E), pady=[0, 10], padx=[25, 20])
#submit_button
btn = ttk.Button(frm, text="Search", command=lambda : function(frm, input_entry, btn, input.get))
btn.grid(column=0, row=2)
root.mainloop()
