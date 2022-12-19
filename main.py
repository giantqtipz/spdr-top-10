import PySimpleGUI as sg
from os import path
from scripts.download_top_10s import *
from scripts.consolidate_top_10s import *
from logs.log_setup import *

"""
    Description:
        - GUI for downloading, and consolidating SPDR Top 10 Holdings with Mark's files, and Top 10 Holdings from the SPDR website
"""

class SPDRTop10Generator:
    def __init__(self):

        self.log = logging.getLogger(path.basename(__file__))

        self.__layout = [
            [
                sg.Text("Mark's File:"), 
                sg.Input(key="-IN-"), 
                sg.FileBrowse(file_types=(
                    ("XLSX", "*.xlsx*"),
                    ("XLS", "*.xls*"),
                    ("LOG", "*.log*")
                ))
            ],
            [
                sg.Exit(), 
                sg.Button("Download New Top 10s"),
                sg.Button("Consolidate Top 10s"),
                sg.Button("Log")
            ]
        ]

    
    def __validate_file(self, file):
        """
            Description:
                - Validates if file exists
        """

        if file and path.isfile(file):
            return True
        self.log.warning("File doesn't exist")
        sg.popup_error("File doesn't exist")
        return False


    def _run_program(self):

        self.log.info("Launched application")
        window = sg.Window("SPDR Top 10 Generator", self.__layout)

        while True:
            event, values = window.read()
            match event:
                case sg.WIN_CLOSED:
                    self.log.info("Closed application")
                    break
                case "Exit":
                    window.close()
                case "Download New Top 10s":
                    download_top_10 = DownloadTop10s("sectors")
                    download_top_10.run_program()
                case "Consolidate Top 10s":
                    if self.__validate_file(values["-IN-"]):
                        consolidate_top_10s = ConsolidateTop10s("output")
                        consolidate_top_10s.excel_file = values["-IN-"]
                        consolidate_top_10s.run_program()
                case "Log":
                    self.log.info("Reading log file")
                    with open(yaml_path, 'r') as f:
                        config = yaml.safe_load(f)    
                        log_file = config["handlers"]["file"]["filename"]
                        if self.__validate_file(log_file):
                            with open(log_file, 'r') as l:
                                sg.popup_scrolled(l.read())
                    


if __name__ == "__main__":
    spdr_top_10_generator = SPDRTop10Generator()
    spdr_top_10_generator._run_program()