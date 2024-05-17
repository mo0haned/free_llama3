import requests
import json
import headers_data

class huggingface_api:
    def __init__(self):
        self.session = requests.Session()
        self.get_conversation()
        
    def get_conversation(self,):
        url = "https://huggingface.co/chat/conversation"
        payload = json.dumps({
        "model": "meta-llama/Meta-Llama-3-70B-Instruct",
        "preprompt": ""
        })
        response = self.session.request("POST", url, data=payload, headers=headers_data.headers)
        if response.status_code == 200:
            self.conv_id = response.json()['conversationId']
        else:
            print("Error:", response.status_code)

    def get_chat_id(self,):
        url = f"https://huggingface.co/chat/conversation/{self.conv_id}/__data.json?x-sveltekit-invalidated=11"
        response = self.session.request("GET", url, headers = headers_data.headers)
        if response.status_code == 200:
            return response.json()['nodes'][1]['data'][3]
        else:
            print("Error:", response.status_code)

    def query_the_chat(self,message):
        url = f"https://huggingface.co/chat/conversation/{self.conv_id}"
        chat_id = self.get_chat_id()
        payload = json.dumps({"inputs":message,"id": chat_id,"is_retry":False,"is_continue":False,"web_search":True,"files":[]}
        )
        response = self.session.post(url, data=payload, headers=headers_data.headers, stream=True)
        if response.status_code == 200:
            # Iterate over the streamed response content
            for chunk in response.iter_content(chunk_size=8192):
                # Filter out keep-alive new chunks
                if chunk:
                    try:
                        chunk =json.loads(chunk.decode('utf-8'))
                        if chunk['type'] =='finalAnswer':
                            return chunk['text']
                    except json.JSONDecodeError:
                        pass
        
        else:
            print(f"Error: {response.status_code}")
            

if __name__ == "__main__":
    hf_chat = huggingface_api()
    chat = hf_chat.query_the_chat("what is the weather today in cairo?")
    print(chat)