# encoding:utf-8

from tkinter import *
from tkinter import filedialog

import os
import re
from zhon.hanzi import stops
import chardet


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)

    red = (255, 0, 0)
    cyan = (0, 255, 255)

    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    green = (0, 255, 0)
    magenta = (255, 0, 255)


class NovelRead:
    def __init__(self, init_window):
        self.init_window = init_window
        self.title_list = []
        self.content_list = []
        self.index = 0
        self.total = 0

        # file
        self.file_path = ''
        self.file_content = ''
        self.is_title_find = True

        self.title_listbox_var = StringVar()
        self.title_label_var = StringVar()
        self.content_length_var = IntVar()
        self.init_all()

    def init_all(self):
        # 格子
        frame1 = Frame(self.init_window, bg='red')
        frame1.pack(side=LEFT, expand=False, fill=Y)

        frame2 = Frame(self.init_window, bg='magenta')
        frame2.pack(side=TOP, expand=False, fill=X)

        frame3 = Frame(self.init_window, bg='cyan')
        frame3.pack(side=BOTTOM, expand=False, fill=X)

        frame4 = Frame(self.init_window, bg='yellow')
        frame4.pack(side=LEFT, expand=True, fill=BOTH)

        main_menu = Menu(self.init_window)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label=u'打开文件', command=self.open_file)
        file_menu.add_command(label=u'保存文件', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label=u'退出', command=self.init_window.quit)

        main_menu.add_cascade(label=u'文件', menu=file_menu)
        self.init_window.config(menu=main_menu)

        #  frame1
        title_scroll = Scrollbar(frame1)
        title_scroll.pack(side=RIGHT, expand=False, fill=Y)
        self.title_listbox = Listbox(frame1, yscrollcommand=title_scroll.set, listvariable=self.title_listbox_var)
        self.title_listbox.bind('<<ListboxSelect>>', self.listbox_select)
        title_scroll.config(command=self.title_listbox.yview)
        self.title_listbox.pack(side=LEFT, expand=True, fill=BOTH)

        # frame2
        title_label = Label(frame2, textvariable=self.title_label_var)
        title_label.pack(side=TOP, expand=True, fill=X)

        # frame3
        button1 = Button(frame3, text='第一章', command=lambda: self.jump(1))
        button1.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)
        button2 = Button(frame3, text='上一章', command=lambda: self.jump(self.index - 1))
        button2.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)
        button3 = Button(frame3, text='下一章', command=lambda: self.jump(self.index + 1))
        button3.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)
        button4 = Button(frame3, text='最后一章', command=lambda: self.jump(self.total))
        button4.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)

        button6 = Button(frame3, text=u'保存修改', command=self.save_change)
        button6.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)

        button5 = Button(frame3, text=u'按字数拆分', command=self.redeal_content)
        button5.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)
        entry1 = Entry(frame3, textvariable=self.content_length_var)
        entry1.pack(side=LEFT, expand=False, fill=Y, padx=10, pady=5)

        # frame4
        text_scroll = Scrollbar(frame4)
        text_scroll.pack(side=RIGHT, expand=False, fill=Y)
        self.content_text = Text(frame4, yscrollcommand=text_scroll.set)
        self.content_text.pack(side=LEFT, expand=True, fill=BOTH)
        text_scroll.config(command=self.content_text.yview)

        self.init_window.mainloop()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(title=u'打开文件', filetypes=((u"txt", "*.txt"), (u"所有", "*.*")))
        with open(self.file_path, mode='rb') as fd:
            current_encoding = chardet.detect(fd.read()).get('encoding')
        with open(self.file_path, mode='r', encoding=current_encoding, errors='ignore') as fd:
            self.file_content = fd.read()
        self.title_list = []
        self.content_list = []
        self.deal_file_content()
        self.set_windows_content()
        return

    def deal_file_content(self):
        title_regex = '(第)([\u4e00-\u9fa5a-zA-Z0-9]{1,7})[章节][^\n]{1,35}(|\n)'
        text = ''
        title = ''
        line_list = self.file_content.splitlines(keepends=True)
        for line in line_list:
            if re.match(title_regex, line):
                if not title and text:
                    self.add_title_content(u'前言', text)
                elif title and text:
                    self.add_title_content(title, text)
                title = line.strip()
                text = ''
            else:
                text += line
        if not title and text:
            self.add_title_content(u'前言', text)
        elif title and text:
            self.add_title_content(title, text)
        return

    def deal_file_content_by_len(self, length=5000):
        text = ''
        title = 1
        line_list = re.split(f'([^\s{stops}]*[\s{stops}])', self.file_content)
        for line in line_list:
            text += line
            if len(text) > length:
                self.add_title_content(str(title), text)
                title += 1
                text = ''
        self.is_title_find = False

        return

    def set_windows_content(self):
        self.title_listbox_var.set(tuple(self.title_list))
        self.title_label_var.set(self.title_list[0])
        self.set_content_text(self.content_list[0])
        return

    def redeal_content(self):
        self.title_list = []
        self.content_list = []
        length = self.content_length_var.get()
        self.deal_file_content_by_len(length=length)
        self.set_windows_content()
        return

    def save_file(self):
        text = ''
        for i in range(self.total):
            if self.is_title_find:
                text += self.title_list[i] + '\n'
            text += self.content_list[i]
        self.file_path = filedialog.asksaveasfilename(title=u'保存文件', initialdir=(os.path.expanduser(self.file_path)))
        with open(self.file_path, mode='w', encoding="'utf-8'") as fd:
            fd.write(self.file_path)
        return

    def save_change(self):
        self.content_list[self.index-1] = self.content_text.get(0.0, END)
        self.save_file()
        return

    def add_title_content(self, title, content):
        self.title_list.append(title)
        self.content_list.append(content)
        self.total += 1
        return

    def jump(self, index: int):
        i = self.total if index > self.total else 1 if index < 1 else index
        if i == 0:
            return
        self.index = i

        self.title_listbox.select_clear(0, END)
        self.title_listbox.select_set(i - 1)
        self.title_listbox.see(i - 1)

        self.set_content_text(self.content_list[i - 1])
        self.title_label_var.set(self.title_list[i - 1])
        return

    def listbox_select(self, event):
        index = self.title_listbox.curselection()
        if len(index) > 0:
            self.jump(int(index[0])+1)
        return

    def set_content_text(self, content):
        self.content_text.delete(0.0, END)
        self.content_text.insert(END, content)
        return


if __name__ == '__main__':
    screen = Tk()
    screen.title("小说阅读器 v1.0")
    screen.geometry('700x600+200+200')
    nr = NovelRead(screen)
    nr.init_all()
