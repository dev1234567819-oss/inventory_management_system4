"""Thin wrappers around tkinter messagebox for consistent usage."""

from tkinter import messagebox


def show_error(title, message, parent=None):
    messagebox.showerror(title, message, parent=parent)


def show_info(title, message, parent=None):
    messagebox.showinfo(title, message, parent=parent)


def show_warning(title, message, parent=None):
    messagebox.showwarning(title, message, parent=parent)


def ask_yes_no(title, message, parent=None):
    return messagebox.askyesno(title, message, parent=parent)
