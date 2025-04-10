from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Step 1: Authorize the client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # This opens a browser the first time
drive = GoogleDrive(gauth)

# Step 2: Upload your Excel file to Drive
file_path = "pharmexcil_members.xlsx"  # Change if your filename is different

upload_file = drive.CreateFile({'title': file_path})
upload_file.SetContentFile(file_path)
upload_file.Upload()

print("✅ File uploaded to Google Drive successfully!")
