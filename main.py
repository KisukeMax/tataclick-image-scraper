from requests_html import HTMLSession
import os
from urllib.parse import urlparse
import requests
import pandas as pd
from tqdm import tqdm

def download_image(url ,save_path, pid_number, image_number, chunk_size=128):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    r = requests.get(url,  stream=True)
    # print(r.status_code)
    if r.status_code == 404:
        return "no file lol"
        # print(r.status_code)
    else:
        # print(r.status_code)
        a = urlparse(url)
        
        # get orignal file name
        f_name = os.path.basename(a.path)
        new_name = pid_number + "_" + str(image_number) + "." + f_name.split(".")[-1]
    
    with open(save_path + "/" + new_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    return save_path + "/" + new_name


df = pd.read_excel("listing_id.xlsx")
for row_number , row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        listing_id = str(row.get("Listing ID"))
        listing_sku = str(row.get("SKU code"))
        print(listing_id)
        s = HTMLSession()
        url = f"https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/productDetails/{listing_id}?isPwa=true&isMDE=true"
        print(url)
        r = s.get(url)
        jb = r.json()
        for n , img_lists in enumerate(jb.get("galleryImagesList")):
            # print(img_lists)
            for img in img_lists.get("galleryImages"):
                # print(img.get("key"))
                if img.get("key") == "superZoom":
                    img_url = "https:" +  img.get("value")
                    img_name = listing_sku
                    download_image(img_url,"images", img_name,n+1)
                    df.at[row_number,"img_" + (str(n))] = img_url
    except:
        pass
df.to_excel("results.xlsx", index=False)