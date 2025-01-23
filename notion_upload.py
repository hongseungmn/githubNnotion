import requests
import os

class Database:
  def __init__(self, header ,database_id):
    self.database_id = database_id
    self.header = header

    
  def retrieve_database(self):
    url = f'https://api.notion.com/v1/databases/{self.database_id}'
    res = requests.get(url=url,headers=self.header)
    return res
  
  def create_page_payload(self, data: dict):
    properties = {
        "Subject": {
            "multi_select": [
                {"name": item} for item in data.get("Subject", []) # 과목
            ]
        },
        "Created By": {
            "people": [
                {"id": createdId} for createdId in data.get("Created By", [])  # 생성자
            ]
        },
        
        "Title": {
            "title": [
                {
                    "text": {
                        "content": data.get("Title", "기본 제목")  # 제목
                    }
                }
            ]
        }
    }
    
    payload = {
        "parent": {"database_id": self.database_id},
        "properties": properties,
    }
    return payload
    
    
  def create_page(self, page_payload: dict):
    create_url = "https://api.notion.com/v1/pages"
    
    res = requests.post(create_url, headers=self.header, json=page_payload)
    print(res.status_code)
    return res;
  
  def get_page_info(self, page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    res = requests.get(url)
    print(res.status_code)
    print(res.json())
  
if __name__ == "__main__":
  
  # 환경변수에서 값 받기
  NOTION_TOKEN = os.getenv('NOTION_TOKEN')
  DATABASE_ID = os.getenv('DATABASE_ID')
  # 노션 헤더 생성
  headers = {
      "Authorization": "Bearer " + NOTION_TOKEN,
      "Content-Type": "application/json",
      "Notion-Version": "2022-06-28" 
  }
  database = Database(header=headers, database_id=DATABASE_ID)
  res = database.retrieve_database()
  name = res.json()["last_edited_by"]["id"]

  data = {
      "Subject": ["test1", "test2"],
      "Created By": [name],
      "Title": "새로운 페이지 제목입니다"
  }
  
  
  payload = database.create_page_payload(data)
  print(payload)
  res = database.create_page(page_payload=payload)
  
  