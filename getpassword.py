import tkinter
from tkinter import *
from tkinter import messagebox
import json
import re
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk  
import os 
import openpyxl

def get_stored_password():
    try:
        with open("password.txt", "r") as file:
            password = file.read().strip()
            return password
    except FileNotFoundError:
            return