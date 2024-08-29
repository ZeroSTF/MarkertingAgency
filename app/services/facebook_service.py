from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.campaign import Campaign

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
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        image = AdImage(parent_id=ad_account.get_id_assured())
        image[AdImage.Field.filename] = 'ad_image.png'
        image[AdImage.Field.bytes] = image_bytes
        image.remote_create()
        return image[AdImage.Field.hash]

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