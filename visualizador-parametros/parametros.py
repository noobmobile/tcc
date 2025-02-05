import numpy as np
from noise import pnoise2
from PIL import Image, ImageDraw, ImageFont

def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    noise = np.zeros((height, width))
    
    for y in range(height):
        for x in range(width):
            noise_value = pnoise2(x / scale,
                                  y / scale,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=width,
                                  repeaty=height,
                                  base=0)
            noise[y][x] = noise_value
    
    # Normalizar para intervalo [0, 255]
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    noise = (noise * 255).astype(np.uint8)
    
    return noise

def add_caption(image, caption, font_size=20):
    draw = ImageDraw.Draw(image)
    try:
        # Usar uma fonte padrão
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Se a fonte padrão não estiver disponível, usar uma fonte padrão do sistema
        font = ImageFont.load_default()
    
    # Adicionar texto na parte inferior da imagem
    text_bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) / 2
    text_y = image.height - text_height - 10
    
    # Adicionar um fundo para o texto
    draw.rectangle([text_x - 5, text_y - 5, text_x + text_width + 5, text_y + text_height + 5], fill="black")
    draw.text((text_x, text_y-5), caption, font=font, fill="white")
    
    return image

def create_image_grid(images, captions, grid_size, output_filename):
    # Assumindo que todas as imagens têm o mesmo tamanho
    img_width, img_height = images[0].size
    grid_width = img_width * grid_size[1]
    grid_height = img_height * grid_size[0]
    
    grid_image = Image.new('L', (grid_width, grid_height))
    
    for i, (img, caption) in enumerate(zip(images, captions)):
        img_with_caption = add_caption(img, caption)
        x = (i % grid_size[1]) * img_width
        y = (i // grid_size[1]) * img_height
        grid_image.paste(img_with_caption, (x, y))
    
    grid_image.save(output_filename)
    # abre a imagem
    grid_image.show()

def main():
    width = 512
    height = 512 
    
    # Parâmetros para diferentes texturas
    parameters = [
        {'scale': 100, 'octaves': 3, 'persistence': 0.5, 'lacunarity': 1.0},
        {'scale': 100, 'octaves': 3, 'persistence': 0.5, 'lacunarity': 2.0},
        {'scale': 100, 'octaves': 3, 'persistence': 0.5, 'lacunarity': 4.0},
    ]
    
    captions = [
        'Lacunaridade: 1',
        'Lacunaridade: 2',
        'Lacunaridade: 4',
    ]
    
    images = []
    for params in parameters:
        noise = generate_perlin_noise(width, height, **params)
        img = Image.fromarray(noise)
        images.append(img)
    
    create_image_grid(images, captions, (1, 3), 'perlin_noise_comparison_with_captions.png')
    # abre a imagem após geração

    

if __name__ == "__main__":
    main()
