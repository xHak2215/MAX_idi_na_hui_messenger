from PIL import Image
import io

def zip_images(bytes:bytes, compress_present=20) -> bytes:
    # Сохраняем в байтовый поток
    output_buffer = io.BytesIO()
    byte = io.BytesIO(bytes)
    image = Image.open(byte)
    width, height = image.size
    new_size = (round(width-((width/100)*compress_present)), round(height-((height/100)*compress_present)))# вычесление по процентам 
    
    resized_image = image.resize(new_size)
    resized_image.save(output_buffer, optimize=True, quality=50, format="JPEG")
    
    return output_buffer.getvalue()

if __name__ == "__main__":
    import os
    
    f=open(os.path.join(os.getcwd(), "media", "0.jpg"), 'rb')
    data=zip_images(f.read())
    f=open("test.jpg", 'wb')
    f.write(data)
    f.close()