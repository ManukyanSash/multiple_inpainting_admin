import requests
import uuid

def get_id_of_image(image_id, image):
    api_url = "https://ai.picsart.com/photos/" + image_id
    headers = {"Authorization": ""}

    with open(image, "rb") as image_file:
        image_data = image_file.read()

    files = {
        "image": (image, image_data)
    }
    response = requests.post(api_url, headers=headers, files=files)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    return ("Error:", response.status_code)

def segmentation(image_id, segment_class):
    api_url = "https://ai.picsart.com/multiMatting/"
    headers = {"Authorization": ""}
    params = dict()
    if segment_class != "sky":
        params = {
            "photo_id": image_id,
            "segmentation_class": segment_class
        }
    else:
        api_url = "https://ai.picsart.com/skySegmentation/"
        params = {
            "original_photo_id": image_id
        }
   
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        url = data["data"].get("url")
        return url
    else:
        print("Error:", response.status_code)   

def ret_files(inp, segment):
    out_img_url = list()
    out_mask_url = list()
    for image in inp:
        random_image_id = str(uuid.uuid4())

        image_url = get_id_of_image(random_image_id, image.name)
        image_url = image_url.get("data").get("url")
        mask_url = segmentation(random_image_id, segment)
        
        out_img_url.append(image_url)
        out_mask_url.append(mask_url)
    return f"{out_img_url}", f"{out_mask_url}" 