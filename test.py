import cloudscraper
import json
import time
import requests


# Define the URL
url = "https://grok.com/rest/app-chat/conversations/new"

# Define headers
headers = {
    "sec-fetch-dest": "document",
}

# Define the request body
payload = {
    "temporary": False,
    "modelName": "grok-3",
    "message": "你好",
    "fileAttachments": [],
    "imageAttachments": [],
    "disableSearch": False,
    "enableImageGeneration": True,
    "returnImageBytes": False,
    "returnRawGrokInXaiRequest": False,
    "enableImageStreaming": True,
    "imageGenerationCount": 2,
    "forceConcise": False,
    "toolOverrides": {},
    "enableSideBySide": True,
    "isPreset": False,
    "sendFinalMetadata": True,
    "customInstructions": "",
    "deepsearchPreset": "",
    "isReasoning": False
}

# Set cookies
cookies = {
    "sso": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiYzFmMTk3MDYtYjhmYS00MmNkLTlkNjQtNTJhMDNmNzI3ZDAxIn0.U3uFCk5iaQmVKN5WLxTBjJGJwh4IO98ms8NjVVQ5qNI",
    "sso-rw": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiYzFmMTk3MDYtYjhmYS00MmNkLTlkNjQtNTJhMDNmNzI3ZDAxIn0.U3uFCk5iaQmVKN5WLxTBjJGJwh4IO98ms8NjVVQ5qNI",
    "_ga": "GA1.1.881743868.1740789941",
    "cf_clearance": "ZC5p_3dWZA_Jzcg0zTLR4Fthq5N.wY_4uDEG9kmWoH0-1740844977-1.2.1.1-NxpwDkJZuGIseDyLhEWO5zoDBF5ZExxOilf1KZWu.MdhVFKA_FS0u.evjwJYS4Q4WUaBHQ2oFHvLrkRWNgm186RoDdvBQIJFdciUXy2Hxp5jHZw3aVWryjV4rc0WZ21T0CCd7sqM6aqqCHub6gI0iDoxMJyUbAOrtR0LbWi_P09CmK3lt6aFTHjQo12xUA47zTXACUi3uRR.5VJUvgTzXwrksWnIIT2g.03QJpH1mif2mf8waEY4Um8Sf3CCZXR8Lbxtl.E5NSjmuFP5XPIem71PhqMfE9Zqq9NCHVg1hVo0vcCnVu_7gM2ghHxVFbO5ZokiB5fr3Re8pR59yO5_vpuQoz74urjxE1p8Jl_G8ZWd7POXaddF8x_d0jJQKKk60v_sgUEDRzjLFFi2M8GXFCDTpM91AeNaGBBOgfzHyfA",
    "_ga_8FEWB057YH": "GS1.1.1740844979.5.1.1740844994.0.0.0"
}

# Create a cloudscraper session
scraper = cloudscraper.create_scraper()
# Update the scraper's cookies
for key, value in cookies.items():
    scraper.cookies.set(key, value)

try:
    # Send the POST request with stream=True to handle streaming response
    with scraper.post(
        url=url,
        headers=headers,
        json=payload,
        stream=True
    ) as response:
        
        # Check if the request was successful
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        
        # Process the streaming response
        print("Streaming Response:")
        
        # Option 1: Process line by line (if the stream is line-delimited)
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(f"Received: {decoded_line}")
                
                # Attempt to parse as JSON if applicable
                try:
                    json_data = json.loads(decoded_line)
                    # Process the JSON data as needed
                    print(f"Parsed JSON: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    # Not valid JSON, just print the raw line
                    pass
                
                # Optional: Add a small delay to make the output more readable
                time.sleep(0.1)
        
        # Option 2 (Alternative): Process chunks of data
        # Uncomment this section and comment out Option 1 if needed
        """
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(f"Received chunk: {chunk.decode('utf-8')}")
                time.sleep(0.1)
        """
        
except Exception as e:
    print(f"An error occurred: {e}")


# session = requests.Session()
# # Add cookies to the session
# session.cookies.update(cookies)

# try:
#     # Send the POST request with stream=True to handle streaming response
#     response = session.post(
#         url=url,
#         headers=headers,
#         json=payload,
#         stream=True
#     )
    
#     # Check if the request was successful
#     response.raise_for_status()
#     print(f"Status Code: {response.status_code}")
    
#     # Process the streaming response
#     print("Streaming Response:")
    
#     # Process line by line (for line-delimited responses)
#     for line in response.iter_lines():
#         if line:
#             decoded_line = line.decode('utf-8')
#             print(f"Received: {decoded_line}")
            
#             # Attempt to parse as JSON if applicable
#             try:
#                 json_data = json.loads(decoded_line)
#                 # Process the JSON data as needed
#                 print(f"Parsed JSON: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
#             except json.JSONDecodeError:
#                 # Not valid JSON, just print the raw line
#                 pass
            
#             # Optional: Add a small delay to make the output more readable
#             time.sleep(0.1)
    
#     # Alternative: Process chunks of data
#     # Uncomment this section and comment out the above loop if needed
#     """
#     for chunk in response.iter_content(chunk_size=1024):
#         if chunk:
#             print(f"Received chunk: {chunk.decode('utf-8')}")
#             time.sleep(0.1)
#     """
        
# except requests.exceptions.RequestException as e:
#     print(f"Request error: {e}")
# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     # Close the session when done
#     session.close()