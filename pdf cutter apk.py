from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.treeview import TreeView, TreeViewNode
from PyPDF3 import PdfFileReader, PdfFileWriter
import tkinter.filedialog
import tkinter.messagebox

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(Label(text='Pdf Cutter', font_size=25))
        self.files = []
        self.tree = None
        self.output_path = None
        self.pages = []

        open_files_button = Button(text="Open Files", on_press=self.select_files)
        self.add_widget(open_files_button)

    def select_files(self, instance):
        files = tkinter.filedialog.askopenfilename(multiple=True)
        if not files:
            tkinter.messagebox.showerror("Error", "No files selected")
            return
        self.files = files
        self.pages = []
        for file in self.files:
            try:
                page = self.extract_first_page(file)
                self.pages.append(page)
            except Exception as e:
                tkinter.messagebox.showerror("Error reading file", str(e))
                continue
        self.output_path = tkinter.filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not self.output_path:
            tkinter.messagebox.showerror("Error", "No file saved")
            return
        try:
            self.save_pdf(self.pages, self.output_path)
        except Exception as e:
            tkinter.messagebox.showerror("Error saving file", str(e))
            return
        tkinter.messagebox.showinfo("Success", "Pages combined successfully")

    def extract_first_page(self, pdf_path):
        pdf = PdfFileReader(pdf_path)
        first_page = pdf.getPage(0)
        return first_page

    def save_pdf(self, pages, output_path):
        pdf_writer = PdfFileWriter()
        for i, page in enumerate(pages):
            pdf_writer.addPage(page)
        with open(output_path, "wb") as f:
            pdf_writer.write(f)


class PdfCutterApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    PdfCutterApp().run()

