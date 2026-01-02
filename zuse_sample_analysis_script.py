"""
This python script was used to analyze the quantity of transcribed signs during the
Zuse handwriting Transkribus-model training.
It's goal is to count the transcription of different signs and compare their per-
centage. The data is retrieved from exported Transkribus-Documents as txt-files.
Folder Structure: ./export_job_xxxx/folders_of_exported_transcribus_documents/xxx.txt

The script only contains the class TrainingSampleAnalyzer with its methods.
The class gets initialized at the end of the script. The whole analysis process
is automated.

The results will be saved as png/xlsx-files in the script folder.
"""

# Imports
import os # access files
import matplotlib.pyplot as plt # bar chart design
import numpy as np # simple math functions
import pandas as pd # dataframe for xlsx export

# Class definition
class TrainingSampleAnalyzer:
    """
    This class analyzes the sign quantity und percentage in the transcribed
    Zuse documents.
    """
    def __init__(self) -> None:
        # Initialize all important parameters for analysis.
        self.txt_dict : dict[str, str] = self.read_txt_in_dict()
        self.letter_count : dict[str, int] = {}
        self.number_count : dict[str, int] = {}
        self.special_sign_count : dict[str, int] = {}
        self.amount_all_letters : int = 0
        # Start the counting of each sign type.
        self.count_signs_in_text()
        # Get the usage percentage of different signs from Zuse documents and general german language.
        self.letter_percentage_zuse : dict[str,float] = self.get_letter_percentage_zuse()
        self.letter_percentage_german : dict[str,float] = self.get_letter_percentage_german()
        # Activate exports.
        self.export_plots()
        self.export_counts_as_xlsx()
        self.export_percentage_comparison()
        
    def read_txt_in_dict(self) -> dict[str, str]:
        """
        Goes into folder with the export files from Transkribus
        to look for the txt-file transcriptions.
        The contents will be added to the txt_dict files while
        the archive signature will be used as dict key.

        Returns:
            dict[str, str]: Dictionary with txt-file contents.
                            Key = archive signature
                            Content = text from txt-file
        """
        
        # define var which is going to be the final dictionary with the text content.
        txt_dict = {}
        
        # folder where all the export files are
        base_path = "export_job_20571304"
        
        # iterate over each folder and navigate to the .txt file
        for dir in os.listdir(base_path):
            dir_path = os.path.join(base_path, dir)
            for filename in os.listdir(dir_path):
                if filename.endswith(".txt"):
                    txt_path = os.path.join(dir_path, filename)
                    with open(txt_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # Delete linebreaks as they aren't part of transkribed text which
                        # should be analyzed. 
                        content = content.replace('\n','')
                        # Seperates the archive signature from .txt-filename as it
                        # should be used as a key for txt_dict.
                        key = filename.split('.')[0]
                        txt_dict[key] = content                
                    break
        return txt_dict
    
    def count_signs_in_text(self) -> None:
        """Counts each sign in the texts and
        appends self.letter_count, self.number_count, 
        self.special_sign_count.
        """
        # Iterate over all texts which are stored in self.txt_dict
        for text in self.txt_dict.values():
            # delete all spaces in text string (only signs should be counted).
            text = text.replace(" ","")
            # Iterate over each sign in texts.
            for sign in text:
                # sign is a letter
                if sign.isalpha():
                    # Increase self.amount_all_letters by 1
                    self.amount_all_letters += 1
                    # if the letter isn't yet a key in the dict
                    # -> create new key and set value to 1.
                    if sign not in self.letter_count:
                        self.letter_count[sign] = 1
                    # else increase counter
                    else:
                        self.letter_count[sign] += 1
                # sign is a number
                elif sign.isdigit():
                    # if the number isn't yet a key in the dict
                    # -> create new key and set value to 1.
                    if sign not in self.number_count:
                        self.number_count[sign] = 1
                    # else increase counter
                    else:
                        self.number_count[sign] += 1
                # sign is something else -> special sign
                else:
                    # if the special sign isn't yet a key in the dict
                    # -> create new key and set value to 1.
                    if sign not in self.special_sign_count:
                        self.special_sign_count[sign] = 1
                    # else increase counter
                    else:
                        self.special_sign_count[sign] += 1
        
        # Sort by most transcribed signs.
        self.letter_count = dict(sorted(self.letter_count.items(),
                                        key=lambda item: item[1],
                                        reverse=True))
        
        self.number_count = dict(sorted(self.number_count.items(),
                                        key=lambda item: item[1],
                                        reverse=True))
        
        self.special_sign_count = dict(sorted(self.special_sign_count.items(),
                                        key=lambda item: item[1],
                                        reverse=True))        
        return
    
    def get_letter_percentage_zuse(self) -> dict[str, float]:
        """Access self.letter_count and returns the percentage of each
        letter. Uppercase and undercase letters are count together.

        Returns:
            dict[str, float]: Dictionary with lowercase letter as key and percentage as value.
        """

        dict_letter_percentage_zuse = {}
        # Count together all uppercase and lowercase letters from self.letter_count in
        # new dictionary dict_letter_percentage_zuse
        for key, value in self.letter_count.items():
            # key in lowercase
            key_lower = key.lower()
            # assigns key in dict_letter_percentage_zuse and adds the value
            dict_letter_percentage_zuse[key_lower] = dict_letter_percentage_zuse.get(key_lower, 0) + value
        
        # get the percentage for each letter by using self.amount_all_letters
        for key, value in dict_letter_percentage_zuse.items():
            percentage = value/self.amount_all_letters * 100
            # assign value using 2 digits.
            dict_letter_percentage_zuse[key] = round(percentage, 2)
            
        return dict_letter_percentage_zuse
    
    def get_letter_percentage_german(self) -> dict[str, float]:
        """
        Creates dict with the percentage of letter usage in the german language.
        Source: https://de.wikipedia.org/wiki/Buchstabenh%C3%A4ufigkeit
        Done in method as it would be to long for __init__
        
        Returns:
            dict[str, float]: Dictionary with lowercase letter as key and percentage as value.
        """
        dict_letter_percentage_german = {"e": 17.40,
                                         "n": 9.78,
                                         "i": 7.55,
                                         "s": 7.27,
                                         "r": 7.00,
                                         "a": 6.51,
                                         "t": 6.15,
                                         "d": 5.08,
                                         "h": 4.76,
                                         "u": 4.35,
                                         "l": 3.44,
                                         "c": 3.06,
                                         "g": 3.01,
                                         "m": 2.53,
                                         "o": 2.51,
                                         "b": 1.89,
                                         "w": 1.89,
                                         "f": 1.66,
                                         "k": 1.21,
                                         "z": 1.13,
                                         "p": 0.79,
                                         "v": 0.67,
                                         "ß": 0.31,
                                         "j": 0.27,
                                         "y": 0.04,
                                         "x": 0.03,
                                         "q": 0.02}
        
        return dict_letter_percentage_german
    
    def export_plots(self) -> None:
        """This functions creates bar charts from self.letter_count,
        self.number_count and self.special_sign_count using the mathplotlib.
        This function is saves bar charts as png-files in current folder.
        """
        # Plot for letter quantity.
        keys = [k for k in self.letter_count.keys()]
        values   = [v for v in self.letter_count.values()]

        plt.figure(figsize=(14, 5)) 
        bars = plt.bar(keys, values)
        plt.xlabel("Letters")
        plt.ylabel("Quantity")
        plt.title("Letter quantity")
        plt.xticks(rotation=0)
        max_y_value = max(values)
        plt.yticks(np.arange(0, max_y_value + 1, 500))
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(height),
                ha="center",
                va="bottom",
                fontsize=6
            )
        plt.tight_layout()
        plt.savefig("letters_quantity",
                    dpi=300,
                    bbox_inches="tight")
        
        # Plot for number quantity.
        keys = [k for k in self.number_count.keys()]
        values   = [v for v in self.number_count.values()]

        plt.figure()
        bars = plt.bar(keys, values)
        plt.xlabel("Numbers")
        plt.ylabel("Quantity")
        plt.title("Number quantity")
        plt.xticks(rotation=0)
        max_y_value = max(values)
        plt.yticks(np.arange(0, max_y_value + 1, 50))
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(height),
                ha="center",
                va="bottom",
                fontsize=8
            )
        plt.tight_layout()
        plt.savefig("numbers_quantity",
                    dpi=300,
                    bbox_inches="tight")
        
        # Plot for special sign quantity.
        keys = [k for k in self.special_sign_count.keys()]
        values   = [v for v in self.special_sign_count.values()]

        plt.figure()
        bars = plt.bar(keys, values)
        plt.xlabel("Special sign")
        plt.ylabel("Quantity")
        plt.title("Special sign quantity")
        plt.xticks(rotation=0)
        max_y_value = max(values)
        plt.yticks(np.arange(0, max_y_value + 1, 100))
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(height),
                ha="center",
                va="bottom",
                fontsize=8
            )
        plt.tight_layout()
        plt.savefig("special_sign_quantity",
                    dpi=300,
                    bbox_inches="tight")
        return
    
    def export_counts_as_xlsx(self) -> None:
        """Exports the counted letters, numbers and special signs as an xlsx file.
        """
        # Define template as dict with list of values before creating the dataframes.
        # Use list comprehension and access self.letter_count, self.number_count and
        # self.special_sign_count for this step.
        df_letters_template = {"Letter":[key for key in self.letter_count.keys()],
                               "Count":[value for value in self.letter_count.values()]}
        df_numbers_template = {"Number":[key for key in self.number_count.keys()],
                               "Count":[value for value in self.number_count.values()]}
        df_special_signs_template = {"Sign":[key for key in self.special_sign_count.keys()],
                                    "Count":[value for value in self.special_sign_count.values()]}
        
        # Create the dataframes.
        df_letters = pd.DataFrame(df_letters_template)
        df_numbers = pd.DataFrame(df_numbers_template)
        df_special_signs = pd.DataFrame(df_special_signs_template)

        # Crate excel-file with multiple sheets.
        with pd.ExcelWriter("sign_counts.xlsx", engine="xlsxwriter") as writer:
            df_letters.to_excel(writer, sheet_name="Letters", index=False)
            df_numbers.to_excel(writer, sheet_name="Numbers", index=False)
            df_special_signs.to_excel(writer, sheet_name="Special_signs", index=False)
        return
    
    def export_percentage_comparison(self) -> None:
        """Exports the comparison of Zuses letter usage and common
        german letter usage as an xlsx-file.
        """
        letter_comparison_template = {"Letter":[key for key in self.letter_percentage_zuse.keys()],
                                      "Zuse letter usage":[value for value in self.letter_percentage_zuse.values()],
                                      "German letter usage":[],
                                      "Percentage difference":[]}
        
        # Get german letter usage in the same row
        for letter in letter_comparison_template["Letter"]:
            try:
                letter_comparison_template["German letter usage"].append(self.letter_percentage_german[letter])
            # Some letters used by Zuse aren't part of the german letter usage overview. In this case
            # no value will be asigned, just '-'.
            except KeyError:
                letter_comparison_template["German letter usage"].append("-")
            # Get the percentage difference.
            try:
                percentage_difference = self.letter_percentage_german[letter]-self.letter_percentage_zuse[letter]
            # If it didn't found a value for german letter usage, no comparison is possible.
            except KeyError:
                percentage_difference = "-"
            letter_comparison_template["Percentage difference"].append(percentage_difference)
        
        # Create dataframe and then export as xlsx-file.
        df_percentage_comparison = pd.DataFrame(letter_comparison_template)
        df_percentage_comparison.to_excel("letter_percentage_comparison.xlsx", sheet_name="Letter comparison")
        return
    
# main script
if __name__ == "__main__":
    traning_sample_analyzer = TrainingSampleAnalyzer()