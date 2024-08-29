from app import app
from flask import current_app, request, jsonify
from app.services.ai_text_service import AiTextService
from app.services.image_generation_service import ImageGenerationService
from app.services.facebook_service import FacebookService
from app.services.scheduler_service import SchedulerService
from datetime import datetime, timedelta
import base64
from io import BytesIO

@app.route('/generate-ad-content', methods=['POST'])
def generate_ad_content():
    data = request.json
    product_description = data.get('product_description')

    if not product_description:
        return jsonify({"error": "Product description is required"}), 400

    ai_text_service = AiTextService(current_app.config['GEMINI_API_KEY'])
    image_service = ImageGenerationService(current_app.config['DALLE_API_KEY'])

    try:
        # Generate ad copy
        ad_copy = ai_text_service.generate_ad_copy(product_description)

        # Generate image
        image = image_service.generate_image(product_description)

        # Convert image to base64 for easy transmission
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            "message": "Ad content generated successfully",
            "ad_copy": ad_copy,
            "image": img_str
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

@app.route('/create-ab-test', methods=['POST'])
def create_ab_test():
    # Create multiple ad variations and track performance
    pass

@app.route('/schedule-ad', methods=['POST'])
def schedule_ad():
    data = request.json
    product_description = data.get('product_description')
    post_time = datetime.now() + timedelta(minutes=5)  # Schedule 5 minutes from now

    scheduler = SchedulerService()
    scheduler.schedule_ad({"product_description": product_description}, post_time)

    return jsonify({"message": "Ad scheduled successfully"})