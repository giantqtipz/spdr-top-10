import concurrent.futures
from datetime import date, datetime as dt
from os import listdir, mkdir, path, remove
import requests
import time
from utils.resources import *

"""
    Description:
        - Automate compiling Sector SPDRs Top 10 holdings for each sector to be distirbuted to Markit-on-Demand
    
    Returns:
        - Eleven (11) Top 10 CSVs for each sector downloaded from www.sectorspdrs.com/sectorspdr/sector/{sector}/index
        - One (1) CSV of reconciled Top 10 Holdings from Mark, and Top 10 Holdings from CSVs from website to be distributed to Markit-on-Demand
"""

class DownloadTop10s():
    def __init__(self, logger, directory):

        self._log = logger

        self._today = date.today()
        self._today_string = self._today.strftime("%Y-%m-%d")

        self.__current_holdings = None
        self.__download_holdings = False

        self._current_directory = path.dirname(__file__)
        self._parent_output_directory = directory
        self._child_output_directory = path.join(self._parent_output_directory, self._today_string)

        self._tickers = [{"sector": sector, "url": f"{url + sector}", "index": prop["index"], "title": prop["title"], "disclaimer": disclaimer} for sector, prop in tickers.items()] 


    def _check_output_path(self):
        """
            Description:
                - Checks if /sectors/ directory exists
                - If False, create directory
        """

        if not path.exists(self._parent_output_directory):
            self._log("/sectors/ directory does not exist - creating directory")
            mkdir(self._parent_output_directory)

        if not path.exists(self._child_output_directory):
            self._log(f"Holdings directory for {self._today} does not exist - creating directory")
            mkdir(self._child_output_directory)
            self.__download_holdings = True


    def __check_sector_files(self):
        """
            Description:
                - Checks if CSVs in /sectors/ directory were generated before today
                - If True, delete files to replace with recent ones
        """

        try:
            self.__current_holdings = listdir(self._child_output_directory)
            file_date = dt.strptime(self.__current_holdings[0].split("-", 1)[1][:-4], "%Y-%m-%d").date()
            
            if file_date != self._today:
                self._log(f"Holdings in /sectors/{file_date} folder are outdated - preparing to download new holdings for today ({self._today})")
                [remove(path.join(self._output_directory, file)) for file in self.__current_holdings]
                self.__download_holdings = True
            else:
                self._log(f"Holdings in /sectors/ folder are current ({self._today}) - abort downloading new holdings")

        except:
            self._log(f"Holdings not found in /sectors/{self._today_string} folder - preparing to download new holdings from today ({self._today})")
            self.__download_holdings = True


    def __download_files(self):
        """
            Description:
                - Download new holdings from SectorSPDRs website
        """

        if self.__download_holdings == True:
            start = time.perf_counter()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self._process_multiple, self._tickers)

            finish = time.perf_counter()

            [self._log(f"{file} downloaded") for file in listdir(self._child_output_directory)]
            self._log(f"Finished downloading all holdings. Took {round(finish - start, 2)} seconds")


    def _process_multiple(self, sector):
        """
            Description:
                - Download new holdings in parallel
        """

        with requests.get(f"{url}{sector['sector']}") as req:
            self._log(f"Fetching holdings for {sector['sector']}", False)
            with open(path.join(self._child_output_directory, f"{sector['sector']}-{date.today()}.csv"), 'wb') as file:    
                file.write(req.content)

    
    def run_program(self):
        self._check_output_path()
        self.__check_sector_files()
        self.__download_files()


if __name__ == "__main__":
    download_top_10 = DownloadTop10s("sectors")
    download_top_10.run_program()