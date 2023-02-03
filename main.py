import PySimpleGUI as sg
from os import path
import yaml
from logs.log_setup import *
from scripts.download_top_10s import *
from scripts.consolidate_top_10s import *

"""
    Description:
        - GUI for downloading, and consolidating SPDR Top 10 Holdings with Mark's files, and Top 10 Holdings from the SPDR website
"""

class SPDRTop10Generator:
    def __init__(self):

        self._log = logging.getLogger(path.basename(__file__))
        self._print = sg.Print

        self.__layout = [
            [
                sg.Text("File Upload:"), 
                sg.Input(key="-INPUT-"), 
                sg.FileBrowse(file_types=(
                    ("XLSX", "*.xlsx*"),
                    ("XLS", "*.xls*"),
                    ("LOG", "*.log*")
                )),
                sg.InputText("Disclaimer Date", size=(14,1), key="-INPUTDATE-")
            ],
            [
                sg.Exit(), 
                sg.Button("Download New Top 10s"),
                sg.Button("Consolidate Top 10s"),
                sg.Button("Log")
            ],
            # [sg.Multiline("", size=(80, 20), autoscroll=True, key='-LOG-', reroute_stdout=True, reroute_stderr=True)]
        ]

        self._window = sg.Window("SPDR Top 10 Generator", self.__layout, finalize=True)

    def _log_process(self, text, print = True):
        """
            Description:
                - Logger for entire application
                - Logs each process into top10s.log file and logs in real time inside the application 
        """
        self._log.info(text)
        # if print == True:
        #     self._window['-LOG-'].update(f"- {text}\n", append=True)

    
    def __validate_file(self, file):
        """
            Description:
                - Validates if file exists
        """
        if file and path.isfile(file):
            return True
        self._log_process("File doesn't exist")
        return False


    def __open_log(self):
        """
            Description:
                - Reads YAML configuration file to fetch filename of logger
        """
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)    
            log_file = config["handlers"]["file"]["filename"]
            if self.__validate_file(log_file):
                with open(log_file, 'r') as l:
                    sg.popup_scrolled(l.read(), size=(80, 20))


    def _run_program(self):

        self._log_process("Launched application")

        while True:
            event, values = self._window.read()

            match event:
                case sg.WIN_CLOSED:
                    self._log_process("Closed application")
                    self._window.close()
                    break
                case "Exit":
                    self._log_process("Closed application")
                    self._window.close()
                    break
                case "Download New Top 10s":
                    self._log_process(f"Downloading today's top 10s from Sector SPDR's website. Open log for more details.")
                    download_top_10 = DownloadTop10s(self._log_process, "sectors")
                    download_top_10.run_program()
                case "Consolidate Top 10s":
                    if self.__validate_file(values["-INPUT-"]):
                        self._log_process("Consolidating downloaded top 10s with Mark's file.")
                        consolidate_top_10s = ConsolidateTop10s(self._log_process, "output")
                        consolidate_top_10s.disclaimer_date = values["-INPUTDATE-"]
                        consolidate_top_10s.excel_file = values["-INPUT-"]
                        consolidate_top_10s.run_program()
                case "Log":
                    self._log_process("Reading log file")
                    self.__open_log()
                
                   
                    
        self._window.close()

if __name__ == "__main__":
    spdr_top_10_generator = SPDRTop10Generator()
    spdr_top_10_generator._run_program()


class SPDRTop10Generator:
    pass