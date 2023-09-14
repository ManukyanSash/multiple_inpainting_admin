import gradio as gr

def copy_info_to_inpainting(*args):
    return args

def process_images_data(data, i = 0):
    data = eval(data)

    if i < 0:
        return data[0].get("url"), 0
    if i >= len(data):
        return data[-1].get("url"), len(data) - 1
    return data[i].get("url"), i

def slide_left(data, images, i):
    res = process_images_data(data, i - 1)
    images = gr.Image.update(value=res[0])
    curr_ind = gr.Slider.update(value=res[1])
    return images, curr_ind

def slide_right(data, images, i):
    res = process_images_data(data, i + 1)
    images = gr.Image.update(value=res[0])
    curr_ind = gr.Slider.update(value=res[1])
    return images, curr_ind
