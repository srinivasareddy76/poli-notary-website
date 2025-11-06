


#!/usr/bin/env python3
"""
Script to generate and upload professional images for Poli Notary website
This script creates placeholder images and uploads them to S3
"""

import boto3
import os
from PIL import Image, ImageDraw, ImageFont
import io
import requests

def create_professional_images():
    """Create professional placeholder images for the website"""
    
    images = {}
    
    # Define image specifications
    image_specs = {
        'notary-professional.jpg': {
            'size': (600, 400),
            'color': '#2563eb',
            'text': 'Professional\nNotary Public',
            'description': 'Hero section professional image'
        },
        'document-signing.jpg': {
            'size': (400, 300),
            'color': '#1f2937',
            'text': 'Document\nSigning',
            'description': 'Document notarization service'
        },
        'real-estate.jpg': {
            'size': (400, 300),
            'color': '#059669',
            'text': 'Real Estate\nServices',
            'description': 'Real estate signing services'
        },
        'mobile-service.jpg': {
            'size': (400, 300),
            'color': '#dc2626',
            'text': 'Mobile\nNotary',
            'description': 'Mobile notary services'
        },
        'business-documents.jpg': {
            'size': (400, 300),
            'color': '#7c3aed',
            'text': 'Business\nDocuments',
            'description': 'Business notary services'
        },
        'notary-portrait.jpg': {
            'size': (400, 500),
            'color': '#374151',
            'text': 'Poli\nNotary',
            'description': 'Professional portrait for about section'
        },
        'client-1.jpg': {
            'size': (150, 150),
            'color': '#f59e0b',
            'text': 'SJ',
            'description': 'Client testimonial photo'
        },
        'client-2.jpg': {
            'size': (150, 150),
            'color': '#10b981',
            'text': 'MC',
            'description': 'Client testimonial photo'
        },
        'client-3.jpg': {
            'size': (150, 150),
            'color': '#8b5cf6',
            'text': 'ER',
            'description': 'Client testimonial photo'
        }
    }
    
    for filename, spec in image_specs.items():
        print(f"Creating {filename}...")
        image = create_placeholder_image(
            size=spec['size'],
            background_color=spec['color'],
            text=spec['text'],
            is_circular=(filename.startswith('client-'))
        )
        images[filename] = image
    
    return images

def create_placeholder_image(size, background_color, text, is_circular=False):
    """Create a professional placeholder image"""
    
    # Create image
    img = Image.new('RGB', size, color=background_color)
    draw = ImageDraw.Draw(img)
    
    if is_circular:
        # Create circular mask for client photos
        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + size, fill=255)
        
        # Apply circular mask
        img.putalpha(mask)
    
    # Try to use a nice font, fall back to default if not available
    try:
        # Try to load a nice font
        font_size = min(size) // 8 if not is_circular else min(size) // 3
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Add text
    if font:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Add text with white color
        draw.text((x, y), text, fill='white', font=font, align='center')
    
    # Add subtle gradient overlay for more professional look
    overlay = Image.new('RGBA', size, (255, 255, 255, 30))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    
    return img.convert('RGB')

def upload_images_to_s3(images, bucket_name):
    """Upload images to S3 bucket"""
    
    s3_client = boto3.client('s3')
    
    uploaded_urls = {}
    
    for filename, image in images.items():
        print(f"Uploading {filename} to S3...")
        
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        
        # Upload to S3
        key = f"assets/images/{filename}"
        
        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=img_byte_arr.getvalue(),
                ContentType='image/jpeg',
                CacheControl='max-age=31536000',  # Cache for 1 year
                ACL='public-read'
            )
            
            url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
            uploaded_urls[filename] = url
            print(f"✓ Uploaded {filename}: {url}")
            
        except Exception as e:
            print(f"✗ Failed to upload {filename}: {str(e)}")
    
    return uploaded_urls

def create_additional_assets(bucket_name):
    """Create additional assets like favicon, logos, etc."""
    
    s3_client = boto3.client('s3')
    
    # Create a simple favicon
    favicon = create_favicon()
    
    # Upload favicon
    favicon_bytes = io.BytesIO()
    favicon.save(favicon_bytes, format='PNG')
    favicon_bytes.seek(0)
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key='assets/favicon.ico',
            Body=favicon_bytes.getvalue(),
            ContentType='image/x-icon',
            ACL='public-read'
        )
        print("✓ Uploaded favicon.ico")
    except Exception as e:
        print(f"✗ Failed to upload favicon: {str(e)}")

def create_favicon():
    """Create a simple favicon"""
    
    size = (32, 32)
    img = Image.new('RGB', size, color='#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple stamp icon
    draw.rectangle([4, 4, 28, 28], outline='white', width=2)
    draw.rectangle([8, 8, 24, 16], fill='white')
    draw.rectangle([8, 20, 24, 24], fill='white')
    
    return img

def main():
    """Main function to generate and upload all images"""
    
    print("🎨 Generating professional images for Poli Notary website...")
    
    # Get S3 bucket name from environment or use default
    bucket_name = os.environ.get('S3_BUCKET', 'poli-notary-static-assets')
    
    print(f"📦 Target S3 bucket: {bucket_name}")
    
    # Create images
    images = create_professional_images()
    
    # Upload to S3
    if bucket_name:
        uploaded_urls = upload_images_to_s3(images, bucket_name)
        create_additional_assets(bucket_name)
        
        print("\n✅ Image generation and upload complete!")
        print("\n📋 Uploaded images:")
        for filename, url in uploaded_urls.items():
            print(f"  • {filename}: {url}")
    else:
        print("❌ No S3 bucket specified. Set S3_BUCKET environment variable.")
        
        # Save images locally for testing
        print("💾 Saving images locally...")
        os.makedirs('generated_images', exist_ok=True)
        
        for filename, image in images.items():
            local_path = f"generated_images/{filename}"
            image.save(local_path, 'JPEG', quality=95)
            print(f"  • Saved: {local_path}")

if __name__ == "__main__":
    main()


