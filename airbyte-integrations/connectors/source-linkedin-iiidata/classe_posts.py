import requests
import json


class Linkedin:
    def __init__(self, access_t, org_id):
        self.access_token = access_t
        self.domain = "https://api.linkedin.com"
        self.api_version = "v2"
        self.org_id = org_id

    def __create_url(self,resource):
        return "/" + self.api_version + "/" + resource + "?count=100&q=authors&authors=List(urn%3Ali%3Aorganization%3A" + self.org_id + ")"

    def __get_headers(self):
        return {'Authorization': 'Bearer ' + self.access_token, 'X-Restli-Protocol-Version':'2.0.0'}

    def __call_url(self,url) :
        response = requests.get(self.domain + url, headers=self.__get_headers())
        if response.status_code == 200:
            return response.json()
        raise response.raise_for_status()

    def __get_ressource_list(self,resource):
        list = []
        url = self.__create_url(resource)
        while url is not None:
            response = self.__call_url(url)
            list+=response["elements"]
            url = None
            for link in response["paging"]["links"]:
                if link["rel"]=="next":
                    url = link["href"]
        return list

    def get_post_list(self):
        return self.__get_ressource_list("ugcPosts")

access_t = "AQWM4EIwMSOh32H9mQJsO_Om9ggtl9BN8Ym2d6wwkYSfXYzKwiryrLbYcAIZz79JeOiZxWUtJoQs0sPAEI1_Qf5QEKDlywrpOqzqLp7A0V0_z9Gjp_p1aSY0-Aa7WrKYmpXOjIkayak3gFXIKcyGKfDs2y2CA33R7unixY0875tGqikys0bF-9rwbz9kl_0i9Y6CxWEa4IZOdFZqigBmuEymWda63GMoyYAgofyguaBFgZwJNv6WLcpQEocfbvEp4QJYWBMkKncnN-ZxE3IIqvKpcYpIAT-eMyxrQp76GOTofdWPsiugnGubTEMynLu1weuoRQNUEkMNkfH7g7hmTbmaB4KU3Q"
org_id = "18950458"
linkedinConnector = Linkedin(access_t, org_id)
linkedinConnector.get_post_list()