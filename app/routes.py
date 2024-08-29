from flask import current_app, request, jsonify
from app.services.ai_text_service import AiTextService
from app.services.image_generation_service import ImageGenerationService
from app.services.facebook_service import FacebookService

@app.route('/create-ad', methods=['POST'])
def create_ad():
    data = request.json
    product_description = data.get('product_description')

    ai_text_service = AiTextService(current_app.config['GEMINI_API_KEY'])
    image_service = ImageGenerationService(current_app.config['DALLE_API_KEY'])
    facebook_service = FacebookService(
        current_app.config['FACEBOOK_ACCESS_TOKEN'],
        current_app.config['FACEBOOK_AD_ACCOUNT_ID']
    )

    # Generate ad copy
    ad_copy = ai_text_service.generate_ad_copy(product_description)

    # Generate image
    image = image_service.generate_image(product_description)

    # Create Facebook ad
    ad = facebook_service.create_ad(
        image=image,
        ad_copy=ad_copy,
        title=f"New Product: {product_description[:30]}",
        link="https://your-product-link.com"
    )

    return jsonify({
        "message": "Ad created successfully",
        "ad_id": ad['id'],
        "ad_copy": ad_copy
    })