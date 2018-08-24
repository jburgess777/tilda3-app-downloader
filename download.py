#!/usr/bin/python
import os
import app
import http_client

def download(url, target, expected_hash):
    http_client.get(url).raise_for_status().download_to(TEMP_FILE)
    os.rename(TEMP_FILE, target)

def download_list(items):
    for i, item in enumerate(items):
        http_client.get(item["url"]).raise_for_status().download_to(item["target"])

def download_app(app):
    files_to_update = []
    for file in app.files:
        file_path = "%s/%s" % (app.folder_path, file["file"])
        data = {
            "url": file["link"],
            "target": file_path,
            "expected_hash": file["hash"],
            "title": app.folder_name + "/" + file["file"]
        }
        
        if file["file"] == "main.py": # Make sure the main.py is the last file we load
            files_to_update.append(data)
        else:
            files_to_update.insert(0, data)

    download_list(files_to_update)

def install(app):
    if not app.files:
        app.fetch_api_information()

    if not os.path.isdir(app.folder_path):
        os.mkdir(app.folder_path)

    download_app(app)

os.mkdir('apps')
cats=app.get_public_app_categories()
for c in cats:
    print "Category", c
    for a in app.get_public_apps(category=c):
        print "Downloading", a
        install(a)

#wf=app.get_public_apps(category='wifi')

