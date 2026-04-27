# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:44:49 2026

@author: student
"""

import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Список цитат: текст, автор, тема
quotes = [
    {"text": "Любовь не знает ни меры, ни цены", "author": "Эрих Мария Ремарк", "topic": "Любовь"},
    {"text": "Лучшая дружба — та, которая начинается с недоразумений", "author": "Уинстон Черчилль", "topic": "Дружба"},
    {"text": "Единственный способ сделать что-то хорошо — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Работа"},
    {"text": "Умение жить — самая редкая вещь в мире. Большинство людей просто существует", "author": "Оскар Уайльд", "topic": "Жизнь"},
    {"text": "Час работы научит большему, чем день объяснений", "author": "Жан-Жак Руссо", "topic": "Труд"},
]

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор цитат")
        self.history = []

        # Текущая цитата
        self.current_quote_label = tk.Label(root, text="", wraplength=300, font=('Arial', 12))
        self.current_quote_label.pack(pady=10)

        # Кнопка генерации
        self.gen_button = tk.Button(root, text="Случайная цитата", command=self.generate_quote)
        self.gen_button.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
        self.author_var = tk.StringVar()
        self.author_filter = tk.Entry(filter_frame, textvariable=self.author_var)
        self.author_filter.grid(row=0, column=1)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0)
        self.topic_var = tk.StringVar()
        self.topic_filter = tk.Entry(filter_frame, textvariable=self.topic_var)
        self.topic_filter.grid(row=1, column=1)

        self.filter_button = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=2, columnspan=2, pady=5)

        # История
        history_frame = tk.Frame(root)
        history_frame.pack(pady=10)

        tk.Label(history_frame, text="История сгенерированных цитат:").pack()
        self.history_listbox = tk.Listbox(history_frame, width=60, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(history_frame, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки сохранения/загрузки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.save_btn = tk.Button(btn_frame, text="Сохранить историю", command=self.save_history)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.load_btn = tk.Button(btn_frame, text="Загрузить историю", command=self.load_history)
        self.load_btn.pack(side=tk.LEFT, padx=5)

    def generate_quote(self):
        if not quotes:
            messagebox.showwarning("Нет цитат", "Список цитат пуст.")
            return

        quote = random.choice(quotes)
        
        # Проверка на пустые строки
        if not quote["text"].strip() or not quote["author"].strip() or not quote["topic"].strip():
            messagebox.showerror("Ошибка данных", "Найдена цитата с пустыми полями. Проверьте исходные данные.")
            return

        self.current_quote_label.config(
            text=f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})'
        )
        
        # Добавляем в историю только если такой ещё нет (по тексту и автору)
        entry = f'"{quote["text"]}" — {quote["author"]} ({quote["topic"]})'
        if entry not in self.history:
            self.history.append(entry)
            self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def apply_filter(self):
        author = self.author_var.get().strip().lower()
        topic = self.topic_var.get().strip().lower()
        
        filtered_history = []
        
        for item in self.history:
            item_lower = item.lower()
            author_match = not author or author in item_lower
            topic_match = not topic or topic in item_lower
            
            if author_match and topic_match:
                filtered_history.append(item)
        
        self.history_listbox.delete(0, tk.END)
        
        for item in filtered_history:
            self.history_listbox.insert(tk.END, item)

    def save_history(self):
        if not self.history:
            messagebox.showinfo("История пуста", "Нет истории для сохранения.")
            return

        filename = "quote_history.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"История сохранена в {filename}")
            
            # Проверка на пустые строки при сохранении (уже проверено при добавлении)
            
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_history(self):
        filename = "quote_history.json"
        
        if not os.path.exists(filename):
            messagebox.showerror("Файл не найден", f"Файл {filename} не найден.")
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                loaded_history = json.load(f)
            
            # Проверка на пустые строки при загрузке
            valid_history = []
            
            for entry in loaded_history:
                if entry and isinstance(entry, str) and entry.strip():
                    valid_history.append(entry.strip())
                else:
                    print(f"Предупреждение: пропущена пустая или некорректная запись: {entry}")
            
            if not valid_history:
                messagebox.showwarning("Пустая история", "В файле нет валидных записей.")
                return

            self.history = valid_history
            self.update_history_list()
            messagebox.showinfo("Успех", f"История загружена из {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()