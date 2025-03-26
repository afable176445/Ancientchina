import requests
import json
import os

def generate_travel_plan(destination, duration, interests, api_key):

    try:
        url = "https://api.deepseek.com/v1/chat/completions"  # Replace with the correct DeepSeek API endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
          "model": "deepseek-chat",  # Specify the model you want to use
          "messages": [
            {
              "role": "user",
              "content": f"Create a detailed travel plan for {destination} ancient cities in china for {duration}. The traveler is interested in {interests}.  dont more than 150 words."
            }
          ],
          "max_tokens": 500,  # Adjust as needed
          "temperature": 0.7  # Adjust for creativity vs. accuracy
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        response.raise_for_status()  # Raise an exception for bad status codes (4xx, 5xx)

        response_data = response.json()

        # Extract the generated text from the response
        travel_plan = response_data["choices"][0]["message"]["content"]
        return travel_plan

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with DeepSeek API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing DeepSeek API response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def generate_search_results(query, api_key):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Enhanced prompt to request structured data with image suggestions
        prompt = f"""Provide detailed information about '{query}' in ancient Chinese history, including:
        1. A comprehensive overview (200-300 words)
        2. 3 relevant image suggestions (provide descriptive keywords for image search)
        3. Key historical facts
        Format the response as JSON with these keys: 'overview', 'image_keywords', 'facts'"""

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.5,
            "response_format": {"type": "json_object"}  # Request JSON response
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]

        # Parse the JSON response
        result = json.loads(content)

        # Get actual image URLs from a free image API (like Unsplash)
        image_urls = []
        for keyword in result.get('image_keywords', [])[:3]:  # Limit to 3 images
            try:
                img_url = get_image_url(keyword + " ancient china")
                if img_url:
                    image_urls.append(img_url)
            except:
                continue

        result['image_urls'] = image_urls
        return result

    except Exception as e:
        print(f"Error in generate_search_results: {e}")
        return None


def get_image_url(keyword):
    """Get a relevant image URL from Unsplash"""
    try:
        access_key = "-UMCJ8oa8hgsXX0LKWRO2kFH90nr2neR689ihpv9aaw"  # Get from https://unsplash.com/developers
        url = f"https://api.unsplash.com/search/photos?page=1&query={keyword}&client_id={access_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']  # Return medium-sized image
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None

if __name__ == '__main__':
    # Example usage (for testing):
    api_key = os.environ.get("DEEPSEEK_API_KEY")  # Load API key from environment variable
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
    else:
        destination = "Paris"
        duration = "3 days"
        interests = "art, history, food"
        plan = generate_travel_plan(destination, duration, interests, api_key)
        print(plan)