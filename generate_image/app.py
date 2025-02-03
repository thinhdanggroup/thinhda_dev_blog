from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("mps")
pipe.safety_checker = None
pipe.requires_safety_checker = False

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = """
a super cat helps a dog to cross the road
"""
image = pipe(prompt).images[0]
image.save("output.png")