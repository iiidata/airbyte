#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

PAGE_METRICS = [
    "page_fans",
    "page_views_by_site_logged_in_unique",
    "page_fans_city",
    "page_fans_gender_age",
    "page_impressions_by_age_gender_unique",
    "page_views_total",
    "page_views_by_age_gender_logged_in_unique",
    "page_views_by_referers_logged_in_unique",
    "page_engaged_users",
    "page_post_engagements",
    "page_impressions_by_city_unique"
]

POST_METRICS = [
    "post_engaged_users",
    "post_engaged_fan",
    "post_negative_feedback",
    "post_negative_feedback_unique",
    "post_clicks",
    "post_clicks_unique",
    "post_impressions",
    "post_impressions_unique",
    "post_impressions_fan",
    "post_impressions_fan_unique",
    "post_impressions_organic",
    "post_impressions_organic_unique",
    "post_impressions_viral",
    "post_impressions_viral_unique",
    "post_reactions_like_total",
    "post_reactions_love_total",
    "post_reactions_wow_total",
    "post_reactions_haha_total",
    "post_reactions_sorry_total",
    "post_reactions_anger_total"
]

PAGE_FIELDS = ",".join(
    [
        "id", "about", "ad_campaign", "affiliation", "app_id", "artists_we_like", "attire", "awards", "band_interests",
        "band_members", "bio", "birthday", "booking_agent", "built", "can_checkin", "can_post", "category", "company_overview",
        "country_page_likes", "cover", "current_location", "description", "display_subtext", "displayed_message_response_time",
        "emails", "fan_count", "featured_video", "followers_count", "general_info", "general_manager", "global_brand_page_name", "impressum", "instagram_business_account", "link",
        "location", "members", "mission", "name", "name_with_location_descriptor", "new_like_count", "phone", "rating_count", "single_line_address", "talking_about_count",
        "username", "website", "were_here_count"
    ]
)

POST_FIELDS = ",".join(
    [
        "message",
        "story",
        "created_time",
        "shares",
        "permalink_url",
        "attachments"
    ]
)
