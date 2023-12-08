

import glob
import json
import os
import re
from uu import Error
trent_type = {
    r"(Trent )?1000-[A-Z]+(?![0-9])\b": "Trent 1000-TENS",
    r"(Trent )?1000-[A-Z]2": "Trent 1000 Pack C",
    r"(Trent )?1000-[A-Z]3": "Trent 1000 Pack B",
    r"(Trent )?9\d{2}-84": "Trent 900",
    r"RB\s?211-524[GH][23](?:-T)?-\d{2}": "RB211-524",
    r"(Trent )?XWB-\d+(?:B)?":"TXWB",
    r"(Trent )?7\d{3}-\d+(?:C)?": "Trent 7000",
    r"(Trent )?8\d{2}-\d+": "Trent 800",
    r"(Trent )?7\d{2}-\d+": "Trent 700",
    r"(Trent )?5\d{2}-\d+": "Trent 500",

}
document_type = {
    "Federal Aviation Administration":"FAA"
}

def get_onedrive_location(base_directory: str):
    user = "\\".join(base_directory.split("\\")[0:3])
    onedrive_location_local = user + "\\OneDrive - Singapore Aero Engine Services Pte Ltd\\LayoutLMV3"
    if os.path.exists(onedrive_location_local):
        return onedrive_location_local
    else:
        raise ValueError
base_directory = os.getcwd().strip("//src")
input_folder_path = get_onedrive_location(base_directory) + r'\test_model_output'
output_folder_path = get_onedrive_location(base_directory) + r'\json_conversion'
json_files = [f for f in os.listdir(input_folder_path) if f.endswith('.json')]
for json_file in json_files:
    file_path = os.path.join(input_folder_path, json_file)
    with open(file_path, 'r') as file:
        data = json.load(file)
        new_json = {
        "PUBLISHED_DATE": "",
        "EFFECTIVE_DATE": "",
        "TURBOFAN_ENGINE": [],
        "DOCUMENT_TYPE": "",
    }
        try:
            for page in data:
                section = ''.join(data[page].get("SECTION", ""))
                print(page)
                print(section + "\n")
                
                if "SUMMARY" in section:
                    #is page1, get document type and published date
                    if type(data[page].get("PUBLISHED_DATE")) == list:
                        new_json["PUBLISHED_DATE"] = ''.join(data[page].get("PUBLISHED_DATE")).strip(")]").lstrip(' ')
                    else:
                        new_json["PUBLISHED_DATE"] = ""
                    for key in document_type:
                        for x in data[page]["DOCUMENT_TYPE"]:
                            if key in x:
                                new_json["DOCUMENT_TYPE"] = document_type[key]
                    if type(data[page].get("EFFECTIVE_DATE")) == list:
                        date = ''.join(data[page].get("EFFECTIVE_DATE")).strip(".").lstrip(' ')
                        new_json["EFFECTIVE_DATE"] = date

                elif "Effective Date" in section and "Applicability" in section:
                    #get turbofan engine and effective date
                    if type(data[page].get("EFFECTIVE_DATE")) == list:
                        if len(data[page].get("EFFECTIVE_DATE")) != 0:
                            new_json["EFFECTIVE_DATE"] = ''.join(data[page].get("EFFECTIVE_DATE")).strip(".").strip(".").lstrip(' ')

                    trent = ' '.join(data[page].get("TURBOFAN_ENGINE", ""))
                    for x in trent_type:
                        matches = re.findall(x, trent)
                        if matches:
                            new_json["TURBOFAN_ENGINE"].append({"Value":trent_type[x]})
        except Error as e:
            print(e)
            continue
    try:
        with open(f"{output_folder_path}\\{json_file}", mode='w') as f:
            json.dump(new_json, f, indent=2)
    except Error as e:
        print(e)
files = glob.glob(input_folder_path + r"\*")
for f in files:
    os.remove(f)