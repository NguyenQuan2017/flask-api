"""[General Configuration Params]
"""
from os import environ, path
from dotenv import load_dotenv
import os
from moviepy.config import change_settings

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
change_settings({
    "IMAGEMAGICK_BINARY": "/usr/bin/convert"
})