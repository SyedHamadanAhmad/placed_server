import google.generativeai as genai
from django.conf import settings
import json
import requests
from serpapi.google_search import GoogleSearch
def init_gemini():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp',
                              generation_config={"response_mime_type": "application/json"})
    return model

def search_youtube(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",  # Search for videos
        "order":"relevance",
        "key": settings.GEMINI_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        
        # Prepare the result with video details
        video_details = []

        # Iterate over the search results and extract necessary information
        for entry in response_data['items']:
            video_title = entry['snippet']['title']
            video_id = entry['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            
            # Generate embed code (iframe)
            
            
            # Append details to the list
            video_details.append({
                "title": video_title,
                "video_url": video_url
            })
        
        # Return the video details
        return video_details
    else:
        print("Error:", response.status_code)
        return [];

def make_table_of_contents(model, topic, level, depth, area):
    prompt = (
        f"You are an expert in pedagogy with over 10 years of experience creating courses "
        f"for engineering students preparing for placements. Generate a table of contents for a course "
        f"based on the following criteria:\n"
        f"- Student ability: {level}\n"
        f"- Depth required: {depth}/100\n"
        f"- Topic: {topic}\n"
        f"- Placement domain: {area}\n\n"
        f"Return the output as a JSON object with the following schema:\n"
        f"{{'depth':int, 'course_name': str, 'num_contents': int, 'contents': [str] }}. Dont include the duration for which each topic is taught or any other information besides the topic name. The number of topics should be indicative of the depth the student wants to achieve in the course as well as the level of students current ability. In terms of level between 0 to 0.33, consider a student a novice. Between 0.33 to 0.8 consider the student intermediate. Above 0.7 consider the student well versed with most concepts"
    )

    response=model.generate_content(prompt)
    try:
        response_data=json.loads(response.text)

       

        return response_data
    except json.JSONDecodeError:
        print("Error decoding JSON from response:", response.text)
        return None
    


def generate_course(model, contents, level, depth, topic):
    n=len(contents)
    prompt = (
        f"You are an expert in pedagogy with 10 years of experience in making courses in {topic}. You are given a table of contents along with a student's level and depth. Level signifies the student's current understanding of the topics. "
        f"Depth signifies how deep they want to study the topics in. Use the level as an indication of how simple the language should be and how simply you need to explain topics. "
        f"Use depth as an indication of how many subtopics you need to explain per topic along with base cases, etc. Prepare a course for the given list of topics: {contents}, "
        f"given that the student's level is {level} and they want to understand the topic at a depth of {depth} out of 100. "
        "Include links to articles(link to specific articles which can be used as a resource to study this topic). When linking to articles, link to easy to understand study resources like Geeks for Geeks(just an example, find more resources like this). Keep the chapter names the same as given in the list. Write around 500 words about the topic and dont talk about documentation. Talk about how that topic is relevant in the field. Talk about what aspects of learning the topic can help the student"
        "Generate in the schema: \n"
        "{'topic_name': str, 'paragraphs': [str], 'links': [str]}.\n"
        "Don't include the duration for which each topic is taught or any other information besides the topic name. "
        "The number of topics should be indicative of the depth the student wants to achieve in the course as well as the level of the student's current ability. "
        "In terms of level, between 0 to 0.33, consider a student a novice. Between 0.33 to 0.8, consider the student intermediate. Above 0.8, consider the student well-versed with most concepts. Only return website links that definitely work do not hallucinate. Length of response should be equal to {n}. Cover every topic in contents, it is a necessary requirement"
    )
    response = model.generate_content(prompt)

    try:
        # Parse the JSON response
        response_data = json.loads(response.text)
        print(len(response_data))
        print(len(contents))
        for i in range(len(contents)):
            print(f"Generating yt links for {contents[i]}")
            yt_links=search_youtube(contents[i])
            response_data[i]['yt_links']=yt_links
        
        
        # # Add youtube links to the response data
        # response_data['yt_links'] = youtube_results

        # Return the updated response data
        return response_data
    
    except json.JSONDecodeError:
        print("Error decoding JSON from response:", response.text)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def search_image(query):
    try:
        search=GoogleSearch({
            "q":query,
            "tbm":"isch",
            "num":3,
            "api_key":settings.SERP_API_KEY
        })

        results=search.get_dict()
        image_result=results.get("images_results", [])
        first_image = image_result[2]
        print(first_image['original'])
        return first_image['original']
    except:
        return 0;
