import requests

def inpainting(caption, 
               photos_url, 
               masks_url, 
               count, 
               paint_mask, 
               guidance_scale,
               negative_prompt,
               output_size,
               blend,
               sampling_steps,
               mask_blur,
               inpaint_area,
               inpaint_mask_padding,
               sampling_method,
               masked_content,
               model_version
            ):
    
    api_url = "https://ai.picsart.com/inpainting/v1/"
    headers = {"accept": "application/json",
               "Authorization": "",
               "Content-Type": "application/json"}

    photos_url = eval(photos_url)
    masks_url = eval(masks_url)
    output_size = eval(output_size)

    data = list()

    for i in range(len(photos_url)):
        params = {
            "caption": caption,
            "photo_url": photos_url[i],
            "mask_url": masks_url[i],
            "count": count,
            "paint_mask": paint_mask,
            "guidance_scale": guidance_scale,
            "negative_prompt": negative_prompt,
            "output_size": output_size,
            "seek": -1,
            "blend": blend,
            "sampling_stpes": sampling_steps,
            "mask_blur": mask_blur,
            "inpaint_area": inpaint_area,
            "inpaint_mask_padding": int(inpaint_mask_padding),
            "sampling_method": sampling_method,
            "masked_content": masked_content,
            "model_version": model_version
        }
        response = requests.post(api_url, headers=headers, json=params)
        if response.status_code == 200:
            data += response.json().get("data")
        else:
            print("Error: ", response.json())
    return f"{data}"
            