import os
def get_onedrive_location(base_directory: str):
    user = "\\".join(base_directory.split("\\")[0:3])
    onedrive_location_local = user + "\\OneDrive - Singapore Aero Engine Services Pte Ltd"
    if os.path.exists(onedrive_location_local):
        return onedrive_location_local
    else:
        raise ValueError
    #get index of Users
    #get user
    #find onedrive
    #return location of onedrive

base_directory = os.getcwd().strip("//src")
pdf_folder_path = base_directory + r'\src\pdfs'
print(get_onedrive_location(base_directory))
