import requests


            "email_subject": {
                "type": "string",
                "description": "Optional. The subject line of the email (default: 'YouTube Thumbnail').",
            },
            "email_body": {
                "type": "string",
                "description": "Optional. The body of the email (can include a message).",
            },

url = "https://www.youtube.com/watch?v=Qu2GhmOGgfY"

video_id = url.split("?v=")[-1]

download_url = f"http://img.youtube.com/vi/{video_id}/default.jpg"

print(download_url)
res = requests.get(download_url)

if res.status_code==200:
    with open("demo.jpg","wb") as img :
        img.write(res.content)
    
    print("thumbnail downloaded succefully")

print("!done")