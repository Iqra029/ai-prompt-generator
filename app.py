import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

def build_midjourney_prompt(subject, style, lighting, camera, aspect_ratio, quality, negative_prompt, stylize, chaos, custom_params):
    prompt_parts = [subject.strip()]
    
    if style and style != "None":
        prompt_parts.append(f"in {style} style")
    if lighting and lighting != "None":
        prompt_parts.append(f"lit by {lighting}")
    if camera and camera != "None":
        prompt_parts.append(f"shot from a {camera} perspective")
    if quality:
        prompt_parts.append("highly detailed, 8k resolution, cinematic lighting, photorealistic")
    
    base_prompt = ", ".join(prompt_parts)
    
    params = []
    if aspect_ratio:
        params.append(f"--ar {aspect_ratio}")
    if quality:
        params.append("--q 2 --v 6.0")
    if stylize and stylize != "100":
        params.append(f"--s {stylize}")
    if chaos and chaos != "0":
        params.append(f"--c {chaos}")
    if negative_prompt.strip():
        params.append(f"--no {negative_prompt.strip()}")
    if custom_params.strip():
        params.append(custom_params.strip())
        
    final_output = base_prompt + (" " + " ".join(params) if params else "")
    return final_output

def build_text_ai_prompt(subject, style, tone, output_format, negative_prompt):
    prompt = f"Act as an expert content creator and specialist in {subject.strip()}.\n\n"
    if style and style != "None":
        prompt += f"Writing Style: {style}\n"
    if tone and tone != "None":
        prompt += f"Tone: {tone}\n"
    if output_format.strip():
        prompt += f"Output Format: {output_format.strip()}\n"
    if negative_prompt.strip():
        prompt += f"Constraints / Exclude: Do NOT include or reference {negative_prompt.strip()}\n"
    
    prompt += f"\nTask: Provide a detailed, highly structured, step-by-step breakdown on '{subject.strip()}'. Avoid generic intro fillers and provide actionable, real-world value immediately."
    return prompt

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_prompt = ""
    image_url = ""
    form_data = {}
    
    if request.method == 'POST':
        ai_tool = request.form.get('ai_tool', 'midjourney')
        subject = request.form.get('subject', '')
        style = request.form.get('style', '')
        lighting = request.form.get('lighting', '')
        camera = request.form.get('camera', '')
        aspect_ratio = request.form.get('aspect_ratio', '16:9')
        quality = request.form.get('quality') == 'on'
        tone = request.form.get('tone', '')
        output_format = request.form.get('output_format', '')
        negative_prompt = request.form.get('negative_prompt', '')
        stylize = request.form.get('stylize', '100')
        chaos = request.form.get('chaos', '0')
        custom_params = request.form.get('custom_params', '')
        
        form_data = request.form
        
        if subject:
            if ai_tool in ['midjourney', 'dalle']:
                generated_prompt = build_midjourney_prompt(
                    subject, style, lighting, camera, aspect_ratio, 
                    quality, negative_prompt, stylize, chaos, custom_params
                )
                # Generate live preview image URL via Pollinations
                encoded_prompt = urllib.parse.quote(f"{subject}, {style}, {lighting}, 8k quality photorealistic")
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            else:
                generated_prompt = build_text_ai_prompt(subject, style, tone, output_format, negative_prompt)
                
    return render_template('index.html', prompt=generated_prompt, image_url=image_url, data=form_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
