import requests


class FreeApi:
    def __init__(self):
        self.api_url = "https://api.uomg.com/api/rand.avatar?sort=男&format=json"

    def get_result(self):
        return self.free_api_request(self.api_url)

    def free_api_request(self, url, params=None, is_post=False):
        try:
            if is_post:
                response = requests.post(url, data=params, timeout=60)
            else:
                if params:
                    response = requests.get(url, params=params, timeout=60)
                else:
                    response = requests.get(url, timeout=60)

            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return response.json()  # Return JSON response as a dictionary
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    api = FreeApi()
    result = api.get_result()
    print(result)
