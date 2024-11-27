from wand.image import Image

def svg_to_png(input_file, output_file):
    """
    Convert an SVG file to a PNG file using Wand.
    
    :param input_file: Path to the input SVG file.
    :param output_file: Path to the output PNG file.
    """
    with Image(filename=input_file, format='svg') as img:
        img.format = 'png'
        img.save(filename=output_file)
    print(f"Successfully converted {input_file} to {output_file}")

# Example usage
input_svg = "C:\\Users\\Sammiykay\\Desktop\\projects\\stella\\ecommerce\\store\\templates\\store\\example.svg" # Path to your SVG file
output_png = "example.png"  # Path to save the PNG file
svg_to_png(input_svg, output_png)
