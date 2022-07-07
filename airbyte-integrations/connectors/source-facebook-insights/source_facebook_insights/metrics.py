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
