from setuptools import setup

"""
    Description:
        - Converts python script into .dmg file for macs
        - Run "python setup.py py2app" in terminal to start
"""

APP=["main.py"]
DATA_FILES=["logs","scripts","utils","README.MD","requirements.txt"]
OPTIONS={
    "argv_emulation": False,
    "iconfile": "assets/spdr.png",
    "includes": ["os", "yaml", "concurrent.futures", "datetime", "time"],
    "packages": ["pandas", "PySimpleGUI"]
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)