from flask import Flask, make_response, redirect, url_for, request, session
from datetime import datetime, timezone
from .class_files import shop_class
from .class_files import user_class
import random, string
from cryptography.fernet import Fernet
