# urls_manager.py

import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import json
from xml.etree import ElementTree as ET
import sqlite3
import matplotlib.pyplot as plt

class UrlManager:
    """
    A class to manage URLs in a SQLite database.
    """
    def __init__(self, db_name='urls.db'):
        """
        Initialize the UrlManager.

        :param db_name: Name of the SQLite database.
        """
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS urls
                          (id INTEGER PRIMARY KEY,
                           url TEXT,
                           description TEXT,
                           category TEXT)''')
        self.conn.commit()

    def add_url(self, url, description, category):
        """
        Add a URL to the database.

        :param url: The URL.
        :param description: The description of the URL.
        :param category: The category of the URL.
        """
        self.c.execute("INSERT INTO urls (url, description, category) VALUES (?, ?, ?)", (url, description, category))
        self.conn.commit()

    def delete_url(self, id):
        """
        Delete a URL from the database.

        :param id: The ID of the URL to be deleted.
        """
        self.c.execute("DELETE FROM urls WHERE id=?", (id,))
        self.conn.commit()

    def get_urls(self):
        """
        Get all URLs from the database.

        :return: A cursor with the URLs.
        """
        return self.c.execute("SELECT * FROM urls")

    def get_insights_data(self):
        """
        Get insights data about the distribution of URLs by category.

        :return: A dictionary with categories as keys and counts as values.
        """
        categories = {}
        for row in self.get_urls():
            category = row[3]
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        return categories

    def export_csv(self, file_name):
        """
        Export URLs to a CSV file.

        :param file_name: The name of the CSV file.
        """
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "URL", "Category"])
            for row in self.get_urls():
                writer.writerow([row[2], row[1], row[3]])

    def export_json(self, file_name):
        """
        Export URLs to a JSON file.

        :param file_name: The name of the JSON file.
        """
        urls = []
        for row in self.get_urls():
            urls.append({"description": row[2], "url": row[1], "category": row[3]})
        with open(file_name, 'w') as file:
            json.dump(urls, file, indent=4)

    def export_xml(self, file_name):
        """
        Export URLs to an XML file.

        :param file_name: The name of the XML file.
        """
        urls = ET.Element('urls')
        for row in self.get_urls():
            url = ET.SubElement(urls, 'url')
            description = ET.SubElement(url, 'description')
            description.text = row[2]
            link = ET.SubElement(url, 'link')
            link.text = row[1]
            category = ET.SubElement(url, 'category')
            category.text = row[3]
        tree = ET.ElementTree(urls)
        tree.write(file_name)

class UrlManagerApp:
    def __init__(self):
        self.url_manager = UrlManager()
        self.app = tk.Tk()
        self.app.title("URL Manager")

        self.url_label = tk.Label(self.app, text="URL:")
        self.url_label.grid(row=0, column=0, sticky='e')
        self.url_entry = tk.Entry(self.app)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we', columnspan=2)

        self.description_label = tk.Label(self.app, text="Description:")
        self.description_label.grid(row=1, column=0, sticky='e')
        self.description_entry = tk.Entry(self.app)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we', columnspan=2)

        self.category_label = tk.Label(self.app, text="Category:")
        self.category_label.grid(row=2, column=0, sticky='e')
        self.category_entry = tk.Entry(self.app)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we', columnspan=2)

        self.add_button = tk.Button(self.app, text="Add URL", command=self.add_url)
        self.add_button.grid(row=0, column=3, padx=5, pady=5, sticky='we')

        self.delete_button = tk.Button(self.app, text="Delete Selected", command=self.delete_url)
        self.delete_button.grid(row=1, column=3, padx=5, pady=5, sticky='we')

        self.url_listbox = tk.Listbox(self.app, width=50, height=10)
        self.url_listbox.grid(row=3, column=0, padx=5, pady=5, sticky='nswe', columnspan=4)
        self.url_listbox.grid_rowconfigure(0, weight=1)
        self.url_listbox.grid_columnconfigure(0, weight=1)

        self.export_csv_button = tk.Button(self.app, text="Export to CSV", command=self.export_csv)
        self.export_csv_button.grid(row=4, column=0, padx=5, pady=5, sticky='we')

        self.export_json_button = tk.Button(self.app, text="Export to JSON", command=self.export_json)
        self.export_json_button.grid(row=4, column=1, padx=5, pady=5, sticky='we')

        self.export_xml_button = tk.Button(self.app, text="Export to XML", command=self.export_xml)
        self.export_xml_button.grid(row=4, column=2, padx=5, pady=5, sticky='we')

        self.show_insights_button = tk.Button(self.app, text="Show Insights", command=self.show_insights)
        self.show_insights_button.grid(row=4, column=3, padx=5, pady=5, sticky='we')

        self.refresh_list()

    def add_url(self):
        url = self.url_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        if self.validate_url(url) and self.validate_description(description) and self.validate_category(category):
            self.url_manager.add_url(url, description, category)
            self.refresh_list()
            self.url_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)

    def delete_url(self):
        selected_id = self.url_listbox.curselection()
        if selected_id:
            self.url_manager.delete_url(selected_id[0]+1)
            self.refresh_list()

    def validate_url(self, url):
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return False
        return True

    def validate_description(self, description):
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return False
        return True

    def validate_category(self, category):
        if not category:
            messagebox.showerror("Error", "Please enter a category.")
            return False
        return True

    def refresh_list(self):
        self.url_listbox.delete(0, tk.END)
        for row in self.url_manager.get_urls():
            self.url_listbox.insert(tk.END, f"Description: {row[2]}, URL: {row[1]}, Category: {row[3]}")

    def export_csv(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_name:
            self.url_manager.export_csv(file_name)

    def export_json(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_name:
            self.url_manager.export_json(file_name)

    def export_xml(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
        if file_name:
            self.url_manager.export_xml(file_name)

    def show_insights(self):
        insights_data = self.url_manager.get_insights_data()
        if insights_data:
            categories = list(insights_data.keys())
            counts = list(insights_data.values())

            plt.bar(categories, counts)
            plt.xlabel('Categories')
            plt.ylabel('Count')
            plt.title('Insights: Category Distribution')
            plt.show()
        else:
            messagebox.showinfo("Insights", "No data available for insights.")

    def run(self):
        self.app.mainloop()
        self.url_manager.conn.close()

if __name__ == '__main__':
    app = UrlManagerApp()
    app.run()
