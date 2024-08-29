from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.campaign import Campaign
from io import BytesIO
import os
import tempfile
import time

class FacebookService:
    def __init__(self, access_token, ad_account_id):
        self.ad_account_id = ad_account_id
        FacebookAdsApi.init(access_token=access_token)

    def create_ad(self, image, ad_copy, title, link):
        ad_account = AdAccount(self.ad_account_id)

        # Upload image
        image_hash = self._upload_image(ad_account, image)

        # Create ad creative
        creative = self._create_ad_creative(ad_account, image_hash, ad_copy, title, link)

        # Create campaign
        campaign = self._create_campaign(ad_account)

        # Create ad
        ad = Ad(parent_id=self.ad_account_id)
        ad.update({
            'name': title,
            'adset_id': campaign['id'],
            'creative': {'creative_id': creative['id']},
            'status': 'PAUSED',
        })
        ad.remote_create()

        return ad

    def _upload_image(self, ad_account, image):
        temp_file_path = None
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                # Save the image to the temporary file
                image.save(temp_file, format='PNG')
                temp_file_path = temp_file.name

            # Create AdImage using the temporary file
            ad_image = AdImage(parent_id=ad_account.get_id_assured())
            ad_image[AdImage.Field.filename] = temp_file_path
            ad_image.remote_create()
            
            return ad_image[AdImage.Field.hash]
        finally:
            if temp_file_path:
                self._delete_file_with_retry(temp_file_path)

    def _delete_file_with_retry(self, file_path, max_attempts=5, delay=1):
        for attempt in range(max_attempts):
            try:
                os.unlink(file_path)
                break
            except WindowsError:
                if attempt == max_attempts - 1:
                    print(f"Failed to delete temporary file: {file_path}")
                else:
                    time.sleep(delay)

    def _create_ad_creative(self, ad_account, image_hash, ad_copy, title, link):
        creative = AdCreative(parent_id=ad_account.get_id_assured())
        creative[AdCreative.Field.name] = title
        creative[AdCreative.Field.object_story_spec] = {
            'page_id': '<YOUR_PAGE_ID>',
            'link_data': {
                'image_hash': image_hash,
                'link': link,
                'message': ad_copy,
                'name': title,
            }
        }
        creative.remote_create()
        return creative

    def _create_campaign(self, ad_account):
        campaign = Campaign(parent_id=ad_account.get_id_assured())
        campaign[Campaign.Field.name] = 'My Campaign'
        campaign[Campaign.Field.objective] = 'LINK_CLICKS'
        campaign[Campaign.Field.status] = 'PAUSED'
        campaign.remote_create()
        return campaign