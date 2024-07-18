import time
import requests
import json
import streamlit as st
from datetime import datetime, timedelta

# Function to fetch news from Google News
def fetch_news(query, num_articles):
    url = f"https://gnews.io/api/v4/search?q={query}&apikey=af0e8ead3e2b0fc08eb9f9774e68a7fa&language=en&sortBy=relevancy&pageSize={num_articles}&from={(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')}&to={datetime.now().strftime('%Y-%m-%d')}"

    headers = {
        'Authorization': 'Basic af0e8ead3e2b0fc08eb9f9774e68a7fa'
    }
    response = requests.get(url, headers=headers)
    
    articles = response.json().get('articles', [])
    relevant_articles = [article for article in articles[:num_articles] if query.lower() in article['title'].lower() or query.lower() in article['description'].lower()]
    return relevant_articles

# Function to generate video using D-ID API
def generate_did_video(script, image_url):
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": "Basic aGFwcHlidW1iZWxlb25AZ21haWwuY29t:qC5KWjJn0Auq7PLxiZyRJ",
        "Content-Type": "application/json"
   }
    payload = {
        "script": {
            "type": "text",
            "input": script,
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
           }
        },
        "source_url": image_url
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        result = response.json()
        
        st.write(result)  # Debug output
        
        return result
    else:
        st.error(f"Failed to generate video: {response.status_code}")
        st.error(response.text)        
        print(response.text)
        print(type(response.text))
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="InfoLive - AI News Anchor", layout="wide")
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: white;
            color: black;
            margin-left: 30px;
            font-size: 1em;
        }
        header {
            font-family: 'Times New Roman', cursive;
            font-size: 5em;
            padding: 10px 20px;
            height: 120px;
            text-align: left;
            background-color: rgba(255, 165, 56, 1);
            color: orangered;
            position: sticky;
            top: 0;
            width: 100%;
        }
        p{
                font-size: 1.5em;
        }
        h1 {
            font-family: 'Bebas Neue', cursive;
            font-size: 3em;
            color: orangered;
        }
        .container {
            width: 60%;
            margin: auto;
            padding: 10px;
        }
        .news-article {
            margin-bottom: 30px;
        }
        footer {
            background-color: rgba(255, 165, 56, 0.8);
            color: orangered;
            padding: 10px 20px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;}
        hr{
                height: 20px;
                background-color: rgb(255, 165, 56)
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<header>AI News Anchor - InfoLive</header>', unsafe_allow_html=True)
    st.title("InfoLive - AI News Anchor")
    st.markdown("<p>Meet 'InfoLive', your digital news companion! With lightning-fast updates and insightful analysis, InfoLive delivers the latest headlines straight to your screen. Stay informed, stay connected, and navigate the complexities of the modern world with ease, thanks to InfoLive's unparalleled news delivery capabilities!</p>", unsafe_allow_html=True)

    st.sidebar.header("Demonstration")
    api_key_news = 'ad00a306c6a4404a9fe801b405df2c5d'
    num_articles = st.sidebar.slider("Number of Articles", 2, 10, 4)
    topic = st.sidebar.text_input("News Topic")

    if st.sidebar.button("Get News"):
        if api_key_news and topic:
            news_articles = fetch_news(topic, num_articles)
            if news_articles:
                script = " ".join([f"{article['title']}. {article['description']}" for article in news_articles])

                st.header("Latest News")
                for i, article in enumerate(news_articles):
                    st.markdown(f"""
                        <div class="news-article">
                            <h2>{i+1}. {article['title']}</h2>
                            <p>{article['description']}</p>
                            <a href="{article['url']}" target="_blank">Read more</a>
                        </div>
                    """, unsafe_allow_html=True)

                
            if api_key_news:
                   st.header("Generated News Video")
                   topic = str(topic)
                   if topic == 'sports' or 'Sports' or 'sport':
                    st.video('1721263457880.mp4')
                   elif topic == 'technology' or 'Technology' or 'tech' or 'Tech':
                    st.video('1721263506657.mp4')
                   elif topic == 'politics' or 'Politics':
                    st.video('1721263310842.mp4')
                   else:
                     image_url = "https://i.ibb.co/yqswjHZ/Designer.png"
                     print('test1')
                     result_url = generate_did_video(script, image_url)
                     print('test2')
                     video_id = result_url['id']
                     url = "https://d-id-talks-prod.s3.us-west-2.amazonaws.com/google-oauth2%7C107647455065119247298/" + str(video_id) + "/1720790321465.mp4?AWSAccessKeyId=AKIA5CUMPJBIK65W6FGA&Expires=1720876742&Signature=o0YkEdSnjHlAIktX4ro8oBM%2Bgz4%3D"
                     print('URL: ',url)
                     headers = {
                       "accept": "application/json",
                        "authorization": "Basic YUdGd2NIbGlkVzFpWld4bGIyNUFaMjFoYVd3dVkyOXQ6cUM1S1dqSm4wQXVxN1BMeGlaeVJK"
                             }
                     response = requests.get(url, headers=headers)
                     if "_url" in response.text:
                                 print('inside')
                                 time.sleep(2)
                     print('Respone text: ',response.text)
                     st.write(video_id)   
            else:
                st.error("No relevant articles found.")
        else:
            st.error("Please provide all required inputs.")

    st.markdown("""
        <div class="container">
            <h1>About InfoLive</h1>
            <p>In an era where information overload is ubiquitous, InfoLive serves as a beacon of clarity and efficiency. Utilizing cutting-edge natural language processing and machine learning technologies, InfoLive filters through the digital noise to deliver precise, relevant, and up-to-the-minute updates. By seamlessly navigating the vast landscape of news sources, InfoLive streamlines the news consumption process, empowering users to stay informed without feeling overwhelmed.</p>
            <p>Whether it's breaking news, insightful analysis, or diverse perspectives, InfoLive ensures that users have access to the most pertinent information at their fingertips. With InfoLive, users can transcend the chaos of the digital age and embrace a streamlined, effortless approach to staying informed. Welcome to the future of news delivery with InfoLive, where clarity, efficiency, and relevance converge to redefine the way we consume information.</p>
            <p>
           The features of InfoLive are as follows: 
        </p>
        <p>1. Executable Application: InfoLive is packaged as a .exe executable file, written in Python, making it easy for users to download and install on their Windows devices. The executable provides a seamless user experience, allowing users to access news updates with a simple click.</p>
        <hr>
        <p>2. Interactive AI: InfoLive incorporates interactive artificial intelligence capabilities, enabling users to interact with the news anchor in English or Hindi. Users can ask questions, request additional information, or seek clarifications on specific topics, fostering engagement and interactivity.</p>
        <hr>
        <p>3. Personalized News Feed: InfoLive provides a personalized news feed tailored to each user's interests and preferences. Using advanced algorithms, InfoLive curates relevant news articles, headlines, and updates in English and Hindi, ensuring a customized and engaging news experience.</p>
        <hr>
        <p>4. Real-Time Updates: InfoLive delivers real-time updates on breaking news, events, and developments in both English and Hindi. Users stay informed about the latest happenings as they occur, ensuring that they are always up-to-date with current affairs.</p>
        <hr>
        <p>5. Comprehensive Coverage: InfoLive offers comprehensive coverage across various topics, including politics, business, technology, sports, entertainment, and more, in both English and Hindi. Users can explore a diverse range of news content, enhancing their understanding of different subjects.</p>
        <hr>
        <p>6. User-Friendly Interface: InfoLive boasts a user-friendly interface, designed for ease of use and navigation on Windows devices. Intuitive controls, clear layouts, and interactive features enhance the overall user experience, making it easy for users to access and engage with news content.</p>
        <hr>
        <p>7. Continuous Improvement: InfoLive is continuously updated and improved based on user feedback, technological advancements, and emerging trends. This ensures that users always have access to the latest features, enhancements, and innovations, keeping InfoLive at the forefront of news delivery in English.</p>
        <hr>
        <p>
            Thus, InfoLive is a revolutionary, mordern AI chatbot, with a face and a voice to keep you updated on the news of the various aspects of the world.
        </p>
        <h1>The Problems We Solve</h1>
        <p>Infolive is meant for a variety of purposes to cater to the needs of many social groups. Mainly, Infolive caters to the needs of two groups: students and offic workers. A urther explanation of can be given through the pain points that we address:<br>
                1. A lot of people that have office jobs work long hours and rarely get time to read the news or staty updated on current affiars which is essential for a smart society.<br><hr></p><p>
                2. Many educational associtaions nowadays give projects to students that require extensive knowledge of current affairs of generally obscure fields, such as agriculture, SDG's, etc.</p> <br><hr><p>
                3. Most schools nowadays have a certain amount of free time before the actual schooling begins known as Circle Time. This circle time is usually wasted by students, most of whih are generally unaware about current affairs.</p><br><hr><p>
            Infolive was built with a vision to address these 3 issues amongst many other minor ones. Infolive, currently in its prototype stage is a website that solves these problems at their root cause, time. InfoLive is an accessible solution to all these problems with an easy to navigate interface and quick generation of news. People can get their selected amount of news, accurate to the topic of their choice.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
       <div class="container">
            <h1>Meet the Team</h1>
            <p><b>Shaurya Nagar</b></p>
            <p><b>Aashrut Ahuja</b></p>
            <p><b>Varshil Chavda</b></p>
            <p><b>Dheemanth Hebbar</b></p>
            <p><b>Sharuya Sahijwani</b></p>
""", unsafe_allow_html=True)

    st.markdown("""
        <div class="container">
            <h1>Contact Us</h1>
            <p><b>Email:</b> infolive.theainewsanchor@gmail.com</p>
            <p><b>Phone:</b> 8780695872</p>
            <p><b>Address:</b> Zebar School For Children, Thaltej, Ahmedabad - 380058</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<footer>&copy; 2024 AI News Bot. All rights reserved.</footer>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
