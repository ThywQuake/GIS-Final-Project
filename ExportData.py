import ee
import json
import time
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import socks
# import socket
# from tqdm import tqdm
# import requests

# set proxy
# socks.set_default_proxy(socks.PROXY_TYPE_HTTP, "127.0.0.1", 7890)
# socket.socket = socks.socksocket
# requests.packages.urllib3.disable_warnings()

# set ee
ee.Initialize()

# # set google drive
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth(r'C:\vsCode_GIS\final_project\Analysis_Route1\client_secrets.json')
# drive = GoogleDrive(gauth)

# get basic data
clouds=ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CLOUD")
precipitation=ee.ImageCollection("NASA/GPM_L3/IMERG_V06")
nox=ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
sox=ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2")

IC=[clouds,precipitation,nox,sox]
bands=[
    'cloud_optical_depth',
    'precipitationCal',
    'NO2_column_number_density',
    'SO2_column_number_density'
]
folders=['clouds_cn_2019_2022_monthly_mean', 'precipitation_cn_2019_2022_monthly_mean', 'nox_cn_2019_2022_monthly_mean', 'sox_cn_2019_2022_monthly_mean']

with open(r'C:\vsCode_GIS\final_project\shp\china.json','r', encoding='utf-8') as f:
    china = json.load(f)
china_fc = ee.FeatureCollection(china)
china_img = ee.Image().paint(china_fc, 0, 1)

start_year = 2019
end_year = 2022

# basic function
def export(image, region, year, month, folder):
    task = ee.batch.Export.image.toDrive(
                image=image,
                folder=folder,
                description=f'monthly_mean_{year}_{month}',
                scale=5000,
                region=region.geometry()
            )
    task.start()
    print(f'Exporting monthly mean {year}-{month} ...')
    i=0
    while task.active():
        time.sleep(5)
        print(f'{year}-{month}: Running for {i*5} seconds...')
        i+=1
    print(f'Exporting monthly mean {year}-{month} complete!\n{folder}\n')

def export_monthly_means(image_collection,band, region, start_year, end_year, folder,start_month=1,end_month=12):
    year=start_year
    month=start_month
    flag=(year<end_year) or ((year==end_year) and (month<=end_month)) 
    while flag:
        start_date = ee.Date.fromYMD(year, month, 1)
        end_date = start_date.advance(1, 'month')
        monthly_mean = image_collection.filterDate(start_date, end_date).select(band).mean().clip(region)
        # 导出代码
        export(monthly_mean, region,  year, month, folder)
        month+=1
        if month>12:
            month=1
            year+=1
        flag=(year<end_year) or ((year==end_year) and (month<=end_month))

# def download_files_in_folder_by_name(folder_name, destination_folder):
#     # 查询并获取文件夹 ID
#     folder_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
#     folder_id = folder_list[0]['id'] if folder_list else None

#     if folder_id is None:
#         print(f'Folder "{folder_name}" not found.')
#         return

#     # 确保目标文件夹存在
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     # 列出并下载文件夹中的所有文件
#     file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
#     for file in tqdm(file_list, desc=f"Downloading files from '{folder_name}'"):
#         file_path = os.path.join(destination_folder, file['title'])
#         file.GetContentFile(file_path)
#         print(f"Downloaded '{file['title']}' to '{destination_folder}'")

# export!
i=int(input('data type: 0-clouds, 1-precipitation, 2-nox, 3-sox\n'))
start_year=int(input('start year: '))
end_year=int(input('end year: '))
start_month=int(input('start month: '))
end_month=int(input('end month: '))
export_monthly_means(IC[i],bands[i],china_fc,start_year,end_year,folders[i],start_month,end_month)

