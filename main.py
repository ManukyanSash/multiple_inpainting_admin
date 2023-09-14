import gradio as gr
from segmentation import ret_files
from inpainting import inpainting
from gui_func import slide_left, slide_right, copy_info_to_inpainting, process_images_data

with gr.Blocks() as main:
    gr.Markdown("Segmentation")
    with gr.Row():
        files = gr.File(label="Upload images", file_count="multiple")
        with gr.Column():
            segment = gr.Dropdown(["hair", 
                                "skin", 
                                "sky", 
                                "lips", 
                                "teeth", 
                                "eyes", 
                                "clothes", 
                                "glasses", 
                                "background", 
                                "foreground", 
                                "all"], label="Segmentation Option", value="skin")
            btn = gr.Button("Segmentation")
        with gr.Column():
            images_url = gr.Textbox(label="Images url")
            segmented_images_url = gr.Textbox(label="Masks url")
            copy_button = gr.Button("Copy info to Inpainting")
    btn.click(fn=ret_files, 
              inputs=[files, segment],
              outputs=[images_url, segmented_images_url])


    gr.Markdown("Inpainting")
    with gr.Column():
        caption = gr.Textbox(label="Caption")
        negative_prompt = gr.Textbox(label="Negative prompt", 
                                     value="bad anatomy, bad proportions, blurry, cloned face, cropped, deformed, dehydrated, disfigured, duplicate, error, extra arms, extra fingers, extra legs, extra limbs, fused fingers, gross proportions, jpeg artifacts, long neck, low quality, lowres, malformed limbs, missing arms, missing legs, morbid, mutated hands, mutation, mutilated, out of frame, poorly drawn face, poorly drawn hands, signature, text, too many fingers, ugly, username, watermark, worst quality", 
                                     interactive=True)
        photos_url = gr.Textbox(label="PhotosUrl")
        masks_url = gr.Textbox(label="MasksUrl")
        with gr.Row():
            source = gr.Dropdown(["PRODUCTION", "STAGING"],
                                label="Source",
                                value="PRODUCTION",
                                interactive=True)
            
            sampling_method = gr.Dropdown(["PNDM", "DPM++SDE_Karras", "DPM++2M_Karras"],
                                        label="Sampling Method",
                                        value="PNDM",
                                        interactive=True)
            
            inpainting_area = gr.Dropdown(["whole_picture", "only_masked"], 
                                        label="Inpainting Area", 
                                        value="whole_picture",
                                        interactive=True)
        with gr.Row():
            model_version = gr.Dropdown(["dreamshaper", "photorealistic", "base"],
                                        label="Model Version",
                                        value="dreamshaper",
                                        interactive=True)
            
            masked_content = gr.Dropdown(["original", "latent_noise"],
                                        label="Masked Count",
                                        value="latent_noise",
                                        interactive=True)
            
            count = gr.Slider(1, 8, value=4, step=1, label="Count", interactive=True)        

        with gr.Row():
            guidance_scale = gr.Slider(1, 30, step=0.5, value=7.5, label="Guidance Scale", interactive=True)
            sampling_steps = gr.Slider(1, 150, step=1, value=50, label="Sampling Steps", interactive=True)
            paint_mask = gr.Checkbox(value=True, label="Paint Mask", interactive=True)
        with gr.Row():
            blend = gr.Checkbox(value=False, label="Blend", interactive=True)
            mask_blur = gr.Slider(0, 50, step=1, label="Mask Blur", interactive=True)
        output_size = gr.Textbox(value=[730, 500], label="out size", visible=False)
        padding = gr.Textbox(value=32, label="padding", visible=False)
    

    copy_button.click(
        fn=copy_info_to_inpainting,
        inputs=[images_url, segmented_images_url],
        outputs=[photos_url, masks_url]
    )
    with gr.Row():
        images = gr.Image(width=730, height=500)
        with gr.Column():
            submit = gr.Button("Inpaint")
            with gr.Row():
                left_button = gr.Button(value="", icon="icons/left.png")
                right_button = gr.Button(value="", icon="icons/right.png")
    process_images_data_textbox = gr.Textbox(visible=False)
    curr_ind = gr.Slider(minimum=0, maximum=7, step=1, interactive=True, visible=False)

    process_images_data_textbox.change(
        process_images_data,
        inputs=process_images_data_textbox,
        outputs=[images, curr_ind]
        )

    left_button.click(
        slide_left,
        inputs=[process_images_data_textbox, images, curr_ind],
        outputs=[images, curr_ind]
    )

    right_button.click(
        slide_right,
        inputs=[process_images_data_textbox, images, curr_ind],
        outputs=[images, curr_ind]
    )

    submit.click(fn=inpainting, 
                 inputs=[caption,
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
                         inpainting_area,
                         padding,
                         sampling_method,
                         masked_content,
                         model_version], 
                 outputs=process_images_data_textbox)
main.launch()