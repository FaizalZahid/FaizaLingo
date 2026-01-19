"""
Note:
The compiled version using Pyinstaller is still not updated:
1. House of Hikmah is still called Bayt al-Hikmah 2.0
2. I didn't put the credit for the notes from jpn-language.com/category/learn-japanese/grammar
3. etc.

Will compile again for major changes rather than minor changes.

Do contact me at https://house-of-hikmah.canny.io/feedback-issues-or-suggestions
"""

import os
import sys
import json
import random
import sqlite3
import pyttsx3
import webbrowser
import tkinter as tk
from tkinter import font
from langdetect import detect
from pydub import AudioSegment
from pydub.playback import play
from tkinter import messagebox, simpledialog


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class FaizaLingo:
    def __init__(self, root):
        self.root = root

        # Load fonts
        font_files = {
            'Poppins': [
                'Poppins-Regular.ttf',
                'Poppins-Bold.ttf'
            ],
            'Roboto': [
                'Roboto-Regular.ttf',
                'Roboto-Bold.ttf'
            ]
        }
        
        # Register fonts
        for font_family, files in font_files.items():
            for font_file in files:
                font_path = resource_path(os.path.join('fonts', font_file))
                # Load the font using the operating system
                if sys.platform == "win32":
                    # Windows
                    from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
                    FR_PRIVATE = 0x10
                    FR_NOT_ENUM = 0x20
                    
                    windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
                    # Notify running applications
                    windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)
                else:
                    # macOS and Linux
                    # Create temporary font directory if it doesn't exist
                    temp_font_dir = os.path.join(os.path.expanduser('~'), '.fonts')
                    os.makedirs(temp_font_dir, exist_ok=True)
                    # Copy font to user font directory
                    shutil.copy2(font_path, os.path.join(temp_font_dir, font_file))
        
        self.root.update()

        self.root.title("FaizaLingo (Japanese)")
        self.root.iconbitmap(default="ringo.ico")

        self.label1 = tk.Label(root, text="FaizaLingo 🍎", font=("Poppins", 18))
        self.label1.pack(padx=60, pady=20)

        self.button_learn = tk.Button(root, text="Learn 🏫", font=("Roboto", 18), width=20, command=self.learn_action)
        self.button_learn.pack(pady=10)

        self.button_reset = tk.Button(root, text="Reset Progress 🔃", font=("Roboto", 18), width=20, command=self.reset_action)
        self.button_reset.pack(pady=10)

        self.button_exit = tk.Button(root, text="Exit ✋", font=("Roboto", 18), width=20, command=self.exit_action)
        self.button_exit.pack(pady=10)

        self.button_donate = tk.Button(root, text="Donate 🧧", font=("Roboto", 18), width=20, command=self.donate_action)
        self.button_donate.pack(pady=10)

        self.button_bayt_al_hikmah_2 = tk.Button(root, text="Webpage 🌐", font=("Roboto", 18), width=20, command=self.bayt_al_hikmah_2_action)
        self.button_bayt_al_hikmah_2.pack(pady=10)

        self.label2 = tk.Label(root, text="Brought to you by House of Hikmah", font=("Roboto", 12))
        self.label2.pack(padx=60, pady=5)

        self.conn = sqlite3.connect("data/notes.db")
        self.cursor = self.conn.cursor()
        self.current_note_index = 0
        self.total_marks = 0
        self.bar_length = 20


    def speak(self, message):
        engine = pyttsx3.init()
        language = detect(message)
        voices = engine.getProperty('voices')

        """
        This is tricky. Since I installed manually, I have the voices in my system.
        The sound will not work in other system but I'll keep it for future revision if I want to implement the voice again.
        """

        # for i, voice in enumerate(voices):
        #     try:
        #         print(f"Voice {i}: {voice}")  # Print the language associated with each voice
        #     except IndexError:
        #         print(f"Voice {i}: Language information not available")

        if language == 'en':
            voice_id = 1
        elif language == 'ja':
            voice_id = 4
        else:
            voice_id = 0
        
        engine.setProperty('voice', voices[voice_id].id)
        engine.say(message)
        engine.runAndWait()


    def play_wav_file(self, file_path):
        audio = AudioSegment.from_wav(file_path)
        play(audio)


    def learn_action(self):
        self.play_wav_file("audio/bite.wav")
        # Destroy widgets from the homepage
        self.label1.pack_forget()
        self.button_learn.pack_forget()
        self.button_reset.pack_forget()
        self.button_exit.pack_forget()
        self.button_donate.pack_forget()
        self.button_bayt_al_hikmah_2.pack_forget()
        self.label2.pack_forget()

        # Create widgets for the second page
        self.second_page_label = tk.Label(self.root, text="Category:", font=("Poppins", 18))
        self.second_page_label.pack(padx=60, pady=20)

        self.button_vocabulary = tk.Button(self.root, text="Vocabulary 📚", font=("Roboto", 18), width=20, command=self.vocabulary_action)
        self.button_vocabulary.pack(padx=10, pady=10)

        self.button_grammar = tk.Button(self.root, text="Grammar 📏", font=("Roboto", 18), width=20, command=self.grammar_action)
        self.button_grammar.pack(padx=10, pady=10)

        self.button_hiragana = tk.Button(self.root, text="Hiragana 🍰", font=("Roboto", 18), width=20, command=self.hiragana_action)
        self.button_hiragana.pack(padx=10, pady=10)

        self.button_katakana = tk.Button(self.root, text="Katakana 🈁", font=("Roboto", 18), width=20, command=self.katakana_action)
        self.button_katakana.pack(padx=10, pady=10)

        self.button_notes = tk.Button(self.root, text="Notes 📝", font=("Roboto", 18), width=20, command=self.notes_action)
        self.button_notes.pack(padx=10, pady=10)

        self.button_back = tk.Button(self.root, text="🔙", font=("Roboto", 18), command=self.back_to_homepage)
        self.button_back.pack(padx=10, pady=10)

        self.label2 = tk.Label(root, text="Brought to you by House of Hikmah", font=("Roboto", 12))
        self.label2.pack(padx=60, pady=5)


    def back_to_homepage(self):
        # Destroy widgets from the second page
        self.second_page_label.pack_forget()
        self.button_vocabulary.pack_forget()
        self.button_grammar.pack_forget()
        self.button_hiragana.pack_forget()
        self.button_katakana.pack_forget()
        if hasattr(self, "button_notes"):
            self.button_notes.pack_forget()
        self.button_back.pack_forget()
        self.label2.pack_forget()

        # Recreate widgets for the homepage
        self.label1.pack(padx=60, pady=20)
        self.button_learn.pack(pady=10)
        self.button_reset.pack(pady=10)
        self.button_exit.pack(pady=10)
        self.button_donate.pack(pady=10)
        self.button_bayt_al_hikmah_2.pack(pady=10)
        self.label2.pack(padx=60, pady=5)


    def vocabulary_action(self):
        self.play_wav_file("audio/bite.wav")
        filename = "data/vocab.json"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                vocab_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find vocab.json file.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return

        num_questions = simpledialog.askinteger("How many?", "How many questions do you want to answer?", initialvalue=5)
        if num_questions is None:
            return

        selected_questions = random.sample(vocab_data[0]["questions"], min(num_questions, len(vocab_data[0]["questions"])))

        # Display questions to the user
        self.display_question(selected_questions, 0, filename)

        self.root.wait_window(self.question_window)


    def grammar_action(self):
        self.play_wav_file("audio/bite.wav")
        filename = "data/grammar.json"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                vocab_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find vocab.json file.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return

        num_questions = simpledialog.askinteger("How many?", "How many questions do you want to answer?", initialvalue=5)
        if num_questions is None:
            return

        selected_questions = random.sample(vocab_data[0]["questions"], min(num_questions, len(vocab_data[0]["questions"])))

        # Display questions to the user
        self.display_question(selected_questions, 0, filename)

        self.root.wait_window(self.question_window)


    def hiragana_action(self):
        self.play_wav_file("audio/bite.wav")
        filename = "data/hiragana.json"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                vocab_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find vocab.json file.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return

        num_questions = simpledialog.askinteger("How many?", "How many questions do you want to answer?", initialvalue=5)
        if num_questions is None:
            return

        selected_questions = random.sample(vocab_data[0]["questions"], min(num_questions, len(vocab_data[0]["questions"])))

        # Display questions to the user
        self.display_question(selected_questions, 0, filename)

        self.root.wait_window(self.question_window)


    def katakana_action(self):
        self.play_wav_file("audio/bite.wav")
        filename = "data/katakana.json"

        try:
            with open(filename, "r", encoding="utf-8") as file:
                vocab_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find vocab.json file.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return

        num_questions = simpledialog.askinteger("How many?", "How many questions do you want to answer?", initialvalue=5)
        if num_questions is None:
            return

        selected_questions = random.sample(vocab_data[0]["questions"], min(num_questions, len(vocab_data[0]["questions"])))

        total_marks = 0

        # Display questions to the user
        self.display_question(selected_questions, 0, filename)

        self.root.wait_window(self.question_window)


    def donate_action(self):
        webbrowser.open("https://ko-fi.com/faizalzahid", new=1)


    def bayt_al_hikmah_2_action(self):
        webbrowser.open("https://houseofhikmah.org", new=1)


    def display_question(self, questions, idx, filename):
        if not hasattr(self, "question_window") or not self.question_window:
            self.question_window = tk.Toplevel(self.root)
            self.question_window.title("Questions")
            self.question_window.geometry("600x300")

        if hasattr(self, "question_window"):
            self.question_window.destroy()
            self.question_window = tk.Toplevel(self.root)
            self.question_window.title("Questions")
            self.question_window.geometry("600x300")

        self.question_frame = tk.Frame(self.question_window, padx=10, pady=5)
        self.question_frame.pack()

        self.selected_option = tk.IntVar()

        text_label = tk.Label(self.question_frame, text=f"Question {idx + 1}: {questions[idx]['text']}", font=("Poppins", 18))
        text_label.pack(anchor="w")

        # Display options with radio buttons
        for option_idx, option in enumerate(questions[idx]['options']):
            option_radio = tk.Radiobutton(self.question_frame, text=f"{option_idx + 1}. {option}",
                                          variable=self.selected_option, value=option_idx, font=("Roboto", 12))
            option_radio.pack(anchor="w")

        # Add a "Submit" button to check the answer
        submit_button = tk.Button(self.question_frame, text="Submit", command=lambda: self.submit_answer(questions, idx, filename), font=("Roboto", 12))
        submit_button.pack(pady=10)

        self.question_window.after(100, lambda: self.speak(questions[idx]['text']))


    def submit_answer(self, questions, idx, filename):
        selected_option_idx = self.selected_option.get()
        selected_option_text = questions[idx]['options'][selected_option_idx]

        if not questions[idx]['attempted']:
            # Check the answer if it hasn't been checked yet
            if selected_option_text == questions[idx]['answer']:
                self.play_wav_file('audio/correct.wav')
                questions[idx]['correct'] = True
                messagebox.showinfo("Correct", "Your answer is correct!")
            else:
                self.play_wav_file('audio/false.wav')
                messagebox.showinfo("Incorrect", f"The answer is {questions[idx]['answer']}.")
                questions[idx]['correct'] = False

            questions[idx]['attempted'] = True

        if idx < len(questions) - 1:
            # Display the next question
            self.display_question(questions, idx + 1, filename)
        elif idx == len(questions) - 1:
            # Last question, close the question window
            self.question_window.destroy()

            # Save changes
            self.save_changes(questions, filename)

            # Display total marks
            self.calculate_total_marks(questions)
            
            # Display total marks and health bar
            total_marks_message = f"Total Marks: {self.total_marks}/{len(questions)}"
            health_bar = self.create_health_bar(self.total_marks / len(questions))
            messagebox.showinfo("Total Marks", f"{total_marks_message}\n{health_bar}")


    def calculate_total_marks(self, questions):
        self.total_marks = sum(1 for question in questions if question['correct'])


    def create_health_bar(self, percentage):
        filled_length = int(self.bar_length * percentage)
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)
        return f"[{bar}]"


    def save_changes(self, questions, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = [{"category": "vocabulary", "questions": []}]

        for updated_question in questions:
            for existing_question in existing_data[0]["questions"]:
                if updated_question["text"] == existing_question["text"]:
                    existing_question["attempted"] = updated_question["attempted"]
                    existing_question["correct"] = updated_question["correct"]
                    break

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
            self.play_wav_file('audio/done.wav')
            messagebox.showinfo("Saved", "Changes saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving changes: {e}")


    def notes_action(self):
        self.play_wav_file("audio/bite.wav")
        # Destroy widgets from the second page
        self.second_page_label.pack_forget()
        self.button_vocabulary.pack_forget()
        self.button_grammar.pack_forget()
        self.button_hiragana.pack_forget()
        self.button_katakana.pack_forget()
        self.button_notes.pack_forget()
        self.button_back.pack_forget()
        self.label2.pack_forget()

        # Create widgets for the third page (Notes)
        self.third_page_label = tk.Label(self.root, text="Notes:", font=("Poppins", 18))
        self.third_page_label.pack(padx=120, pady=20)

        self.button_hiragana_notes = tk.Button(self.root, text="🍰 Hiragana notes 📝", font=("Roboto", 18), width=22, command=self.hiragana_notes_action)
        self.button_hiragana_notes.pack(pady=10)

        self.button_katakana_notes = tk.Button(self.root, text="🈁 Katakana notes 📝", font=("Roboto", 18), width=22, command=self.katakana_notes_action)
        self.button_katakana_notes.pack(pady=10)

        self.button_grammar_notes = tk.Button(self.root, text="📏 Grammar notes 📝", font=("Roboto", 18), width=22, command=self.grammar_notes_action)
        self.button_grammar_notes.pack(pady=10)

        self.button_back_to_second_page = tk.Button(self.root, text="🔙", font=("Roboto", 18), command=self.back_to_second_page)
        self.button_back_to_second_page.pack(pady=10)

        self.label2_notes = tk.Label(root, text="Brought to you by House of Hikmah. Notes are from jpn-language.com/category/learn-japanese/grammar", font=("Roboto", 12))
        self.label2_notes.pack(padx=60, pady=5)


    def hiragana_notes_action(self):
        self.play_wav_file("audio/bite.wav")
        # Create a new window for displaying Hiragana notes
        self.display_hiragana_notes_window()


    def display_hiragana_notes_window(self):
        self.hiragana_notes_window = tk.Toplevel(self.root)
        self.hiragana_notes_window.title("Hiragana Notes")
        self.hiragana_notes_window.geometry("800x800")

        # Create a frame for the note text and scrollbar
        note_frame = tk.Frame(self.hiragana_notes_window)
        note_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(note_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget to display the note
        self.note_text = tk.Text(note_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.note_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to scroll the text widget
        scrollbar.config(command=self.note_text.yview)

        self.next_button = tk.Button(self.hiragana_notes_window, text="Next", width=20, command=self.display_next_hiragana_note)
        self.next_button.pack(pady=10)

        # Set font size for the note text
        self.note_text.config(font=("Roboto", 12))  # Adjust the font size as needed

        # Display the first Hiragana note
        self.display_first_hiragana_note()


    def display_first_hiragana_note(self):
        self.cursor.execute("SELECT * FROM hiragana_notes ORDER BY `order` ASC LIMIT 1")
        note = self.cursor.fetchone()
        if note:
            self.note_text.insert(tk.END, note[1])
            self.current_note_index = note[0]


    def display_next_hiragana_note(self):
        self.current_note_index += 1
        self.cursor.execute("SELECT * FROM hiragana_notes WHERE `order` = ? LIMIT 1", (self.current_note_index,))
        note = self.cursor.fetchone()
        if note:
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert(tk.END, note[1])
        else:
            messagebox.showinfo("End of Notes", "No more notes available.")


    def katakana_notes_action(self):
        self.play_wav_file("audio/bite.wav")
        # Create a new window for displaying Hiragana notes
        self.display_katakana_notes_window()


    def display_katakana_notes_window(self):
        self.katakana_notes_window = tk.Toplevel(self.root)
        self.katakana_notes_window.title("Katakana Notes")
        self.katakana_notes_window.geometry("800x800")

        # Create a frame for the note text and scrollbar
        note_frame = tk.Frame(self.katakana_notes_window)
        note_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(note_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget to display the note
        self.note_text = tk.Text(note_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.note_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to scroll the text widget
        scrollbar.config(command=self.note_text.yview)

        self.next_button = tk.Button(self.katakana_notes_window, text="Next", width=20, command=self.display_next_katakana_note)
        self.next_button.pack(pady=10)

        # Set font size for the note text
        self.note_text.config(font=("Roboto", 12))  # Adjust the font size as needed

        # Display the first Hiragana note
        self.display_first_katakana_note()


    def display_first_katakana_note(self):
        self.cursor.execute("SELECT * FROM katakana_notes ORDER BY `order` ASC LIMIT 1")
        note = self.cursor.fetchone()
        if note:
            self.note_text.insert(tk.END, note[1])
            self.current_note_index = note[0]


    def display_next_katakana_note(self):
        self.current_note_index += 1
        self.cursor.execute("SELECT * FROM katakana_notes WHERE `order` = ? LIMIT 1", (self.current_note_index,))
        note = self.cursor.fetchone()
        if note:
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert(tk.END, note[1])
        else:
            messagebox.showinfo("End of Notes", "No more notes available.")


    def grammar_notes_action(self):
        self.play_wav_file("audio/bite.wav")
        # Create a new window for displaying Hiragana notes
        self.display_grammar_notes_window()


    def display_grammar_notes_window(self):
        self.grammar_notes_window = tk.Toplevel(self.root)
        self.grammar_notes_window.title("Grammar Notes")
        self.grammar_notes_window.geometry("800x800")

        # Create a frame for the note text and scrollbar
        note_frame = tk.Frame(self.grammar_notes_window)
        note_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(note_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget to display the note
        self.note_text = tk.Text(note_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.note_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to scroll the text widget
        scrollbar.config(command=self.note_text.yview)

        self.next_button = tk.Button(self.grammar_notes_window, text="Next", width=20, command=self.display_next_grammar_note)
        self.next_button.pack(pady=10)

        # Set font size for the note text
        self.note_text.config(font=("Roboto", 12))  # Adjust the font size as needed

        # Display the first Hiragana note
        self.display_first_grammar_note()


    def display_first_grammar_note(self):
        self.cursor.execute("SELECT * FROM grammar_notes ORDER BY `order` ASC LIMIT 1")
        note = self.cursor.fetchone()
        if note:
            self.note_text.insert(tk.END, note[1])
            self.current_note_index = note[0]


    def display_next_grammar_note(self):
        self.current_note_index += 1
        self.cursor.execute("SELECT * FROM grammar_notes WHERE `order` = ? LIMIT 1", (self.current_note_index,))
        note = self.cursor.fetchone()
        if note:
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert(tk.END, note[1])
        else:
            messagebox.showinfo("End of Notes", "No more notes available.")


    def back_to_second_page(self):
        # Destroy widgets from the third page
        self.third_page_label.pack_forget()
        self.button_hiragana_notes.pack_forget()
        self.button_katakana_notes.pack_forget()
        self.button_grammar_notes.pack_forget()
        self.button_back_to_second_page.pack_forget()
        self.label2_notes.pack_forget()

        # Recreate widgets for the second page
        self.second_page_label.pack(padx=60, pady=20)
        self.button_vocabulary.pack(padx=10, pady=10)
        self.button_grammar.pack(padx=10, pady=10)
        self.button_hiragana.pack(padx=10, pady=10)
        self.button_katakana.pack(padx=10, pady=10)
        self.button_notes.pack(padx=10, pady=10)
        self.button_back.pack(padx=10, pady=10)
        self.label2.pack(padx=60, pady=5)


    def reset_action(self):
        # Destroy widgets from the homepage
        self.label1.pack_forget()
        self.button_learn.pack_forget()
        self.button_reset.pack_forget()
        self.button_exit.pack_forget()
        self.button_donate.pack_forget()
        self.button_bayt_al_hikmah_2.pack_forget()
        self.label2.pack_forget()

        # Create widgets for the second page
        self.second_page_label = tk.Label(self.root, text="Category:", font=("Poppins", 18))
        self.second_page_label.pack(padx=60, pady=20)

        self.button_vocabulary = tk.Button(self.root, text="Vocabulary 📚", font=("Roboto", 18), width=20, command=self.reset_vocabulary_action)
        self.button_vocabulary.pack(padx=10, pady=10)

        self.button_grammar = tk.Button(self.root, text="Grammar 📏", font=("Roboto", 18), width=20, command=self.reset_grammar_action)
        self.button_grammar.pack(padx=10, pady=10)

        self.button_hiragana = tk.Button(self.root, text="Hiragana 🍰", font=("Roboto", 18), width=20, command=self.reset_hiragana_action)
        self.button_hiragana.pack(padx=10, pady=10)

        self.button_katakana = tk.Button(self.root, text="Katakana 🈁", font=("Roboto", 18), width=20, command=self.reset_katakana_action)
        self.button_katakana.pack(padx=10, pady=10)

        self.button_back = tk.Button(self.root, text="🔙", font=("Roboto", 18), command=self.back_to_homepage)
        self.button_back.pack(padx=10, pady=10)

        self.label2 = tk.Label(root, text="Brought to you by House of Hikmah", font=("Roboto", 12))
        self.label2.pack(padx=60, pady=5)


    def reset_hiragana_action(self):
        filename = "data/hiragana.json"
        self.reset_progress(filename)


    def reset_katakana_action(self):
        filename = "data/katakana.json"
        self.reset_progress(filename)


    def reset_vocabulary_action(self):
        filename = "data/vocab.json"
        self.reset_progress(filename)


    def reset_grammar_action(self):
        filename = "data/grammar.json"
        self.reset_progress(filename)


    def reset_progress(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {filename} file.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON file.")
            return

        for item in data:
            for question in item["questions"]:
                question["attempted"] = False
                question["correct"] = False

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.play_wav_file('audio/done.wav')
            messagebox.showinfo("Reset Progress", "Progress reset successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving changes: {e}")


    def exit_action(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            self.play_wav_file('audio/bye.wav')


root = tk.Tk()
app = FaizaLingo(root)
root.mainloop()
app.conn.close()