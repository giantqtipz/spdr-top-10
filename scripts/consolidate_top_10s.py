from os import path, remove
import pandas as pd
from .download_top_10s import *

"""
    Description:
        - Consolidate holdings from Mark's excel file with Top 10 Holdings from Sector SPDRs website
"""

class ConsolidateTop10s(DownloadTop10s):
    def __init__(self, logger, directory):
        super().__init__(logger, directory)

        self._log = logger

        self.excel_file = None

        self.__excel_columns = ["Company", "Symbol", "Weight"]
        self.__csv_columns = ["Company Name", "Symbol", "Index Weight"]
        self.__order_columns = [3,2,0,1]

        self.__sectors_directory = "sectors"

        self.__output_name = path.join(self._parent_output_directory, self._today_string, f"SPDR_Top_10_Holdings_{self._today}")
        self.__output_extension = ".xlsx"

        self.__results = None

        self._check_output_path()


    def __consolidate_data(self):
        """
            Description:
                - Utilize pandas library to simulate vlookup between Mark's excel file, and each Top 10 Holdings from Sector SPDRs website
        """

        dataframes = []

        for _, sector in enumerate(self._tickers):
            self._log(f"Consolidating holdings for {sector['sector']}")
            excel = pd.read_excel(self.excel_file, index_col=None, sheet_name=sector["index"], names=self.__excel_columns)
            csv = pd.read_csv(path.join(self.__sectors_directory, self._today_string, f"{sector['sector']}-{date.today()}.csv"), skiprows=1, index_col=None, usecols=self.__csv_columns)
            
            vlookup = excel.merge(csv, left_on="Symbol", right_on="Symbol", how="inner").drop(columns=["Company", "Index Weight"])
            vlookup["Sector"] = sector["index"] # Append a sector column
            vlookup["Weight"] = vlookup["Weight"].transform(lambda x: '{:,.2%}'.format(x)) # Converts decimal Weights to percentages
            
            vlookup = vlookup.iloc[:, self.__order_columns] # Rearrange columns

            dataframes.append(vlookup)
        
        self.__results = pd.concat(dataframes)


    def __export_to_csv(self):
        """
            Description:
                - Export consolidated holdings from Mark's file, and Top 10s from Sector SPDRs website into a single excel output file
        """

        if path.isfile(f"{self.__output_name}{self.__output_extension}"):
            self._log(f"Output file for today {self._today} already exists - deleting existing file")
            remove(f"{self.__output_name}{self.__output_extension}")
        
        self._log(f"Creating excel output file")
        
        self.__results.to_excel(path.join(f"{self.__output_name}{self.__output_extension}"))

        self._log(f"Output file created and saved in /{self.__output_name}{self.__output_extension}")


    def run_program(self):
        self.__consolidate_data()
        self.__export_to_csv()


if __name__ == "__main__":
    consolidate_top_10s = ConsolidateTop10s("output")
    consolidate_top_10s.run_program()