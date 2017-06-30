from scrape_handler import *

try:
	# for Python 2
	import Tkinter as tk
	import tkMessageBox as tmb
except ImportError:
	# for Python 3
	import tkinter as tk
	import tkinter.messagebox as tmb


class GuiHandler(object):
	"""
	GUI Handler class implementation.
	"""

	def __init__(self):
		self.program_name = 'Žodžių reikšmė'
		self.root = tk.Tk()
		self.root.columnconfigure(0, weight=1)
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(2, weight=1)
		self.root.rowconfigure(3, weight=1)

	def start_deployment_in_gui(self):
		"""
		Starts deployment in GUI window.
		"""
		self.root.resizable(width=True, height=True)
		self.root.focus_set()

		self.__center_window()
		self.root.wm_title(self.program_name)
		self.__create_buttons_and_labels()
		self.__create_textfields()
		self.__bind()
		self.root.mainloop()

	def __bind(self):
		self.root.bind('<Return>', self.__search)
		self.output_text_lt1.bind("<Button-3>", self.__translate_text)
		self.output_text_lt1.bind("<Up>", self.__get_selected_text)

		self.translate_label.bind("<Enter>", self.__on_enter)

	# self.translate_label.bind("<Leave>", self.on_leave)

	def __create_textfields(self):
		self.output_text_lt1 = tk.Text(self.root, width=60, height=10)
		self.output_text_lt1.grid(row=2, column=0, sticky="wens")
		self.output_text_en1 = tk.Text(self.root, width=60, height=10)
		self.output_text_en1.grid(row=2, column=1, sticky="wens")
		self.output_text_lt2 = tk.Text(self.root, width=60, height=10)
		self.output_text_lt2.grid(row=3, column=0, sticky="wens")
		self.output_text_en2 = tk.Text(self.root, width=60, height=10)
		self.output_text_en2.grid(row=3, column=1, sticky="wens")

	def __create_buttons_and_labels(self):
		tk.Button(self.root, command=self.__search, text='Search').grid(
			row=0,
			column=1,
			sticky="wens",
			pady=5)

		self.function_field_1 = tk.Entry(self.root)
		self.function_field_1.grid(row=0, column=0, sticky="we")
		self.function_field_1.insert('0', "labas")

		self.translate_label = tk.Label(self.root, text="Pažymėti teksta, ir užvesti pelyte, kad išverstų")
		self.translate_label.grid(row=1, column=0, sticky="w")

	def __post_output_log(self):
		self.output_text_lt1.configure(state="normal")
		self.output_text_lt1.insert('1.0', "test" + "\n")
		self.output_text_lt1.configure(state="disabled")

	def __on_enter(self, event):
		selected = self.output_text_lt1.get(tk.SEL_FIRST, tk.SEL_LAST)
		translate_to_en = translate_from_lt_english(selected)
		self.translate_label.configure(text=translate_to_en)

	def __search(self):
		"""
		Fill text fields
		:return:
		"""

		# Lithuanian
		entered_value = self.function_field_1.get()
		synonyms_lt = get_synonims(entered_value)
		LOGGER.info(synonyms_lt)
		if synonyms_lt:
			self.output_text_lt1.insert('1.0', synonyms_lt + "\n\n")

			entymology_lt = get_lt_word_etymology(strip_lt(entered_value))
			self.output_text_lt2.insert('1.0', entymology_lt + "\n\n")

		if entered_value:
			# English
			translate_to_en = translate_from_lt_english(entered_value)
			self.output_text_en1.insert('1.0', translate_to_en + "\n\n")
			etymology = get_en_word_etymology(translate_to_en)
			self.output_text_en2.insert('1.0', etymology + "\n\n")

	def __center_window(self):
		"""
		Centers the window of tkinter.
		"""
		w = 750  # width for the Tk root
		h = 500  # heighetymologyt for the Tk root

		# get screen width and height
		ws = self.root.winfo_screenwidth()  # width of the screen
		hs = self.root.winfo_screenheight()  # height of the screen

		# calculate x and y coordinates for the Tk root window
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)

		# set the dimensions of the screen and where it is placed
		self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def __get_selected_text(self, event):
		"""
		Get selected text, and put it on search field.
		:param event:
		:return:
		"""
		selected = self.output_text_lt1.get(tk.SEL_FIRST, tk.SEL_LAST)
		LOGGER.info(selected)
		self.function_field_1.delete(0, tk.END)
		self.function_field_1.insert(0, selected)

	def __translate_text(self, event):
		"""
		Translate selected text, and display it
		:param event:
		:return:
		"""
		selected = self.output_text_lt1.get(tk.SEL_FIRST, tk.SEL_LAST)
		translate_to_en = translate_from_lt_english(selected)
		self.output_text_en1.insert('1.0', translate_to_en + "\n\n")


if __name__ == "__main__":
	gui_handler = GuiHandler()
	gui_handler.start_deployment_in_gui()
