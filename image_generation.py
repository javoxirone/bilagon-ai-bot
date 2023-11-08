import requests


class DALLERequester:
    def __init__(self, api_key, model_name="image-alpha-001"):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/images"  # Check that this URL is correct
        self.model_name = model_name

    def generate_image(self, description):
        data = {
            "model": self.model_name,
            "text": description,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.post(self.api_url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            image_url = result["data"]["url"]
            return image_url
        else:
            print(f"Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def save_image(self, image_url, filename):
        image = requests.get(image_url)

        if image.status_code == 200:
            with open(filename, "wb") as img_file:
                img_file.write(image.content)
            print(f"Image saved as {filename}")
        else:
            print(f"Failed to download image. Status code: {image.status_code}")
            print(image.text)