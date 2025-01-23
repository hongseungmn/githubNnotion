import requests
import os
import subprocess

# 커밋 메시지와 설명 가져오기
def get_commit_info():
    result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %an %ad %s %b'], capture_output=True, text=True)
    commit_data = result.stdout.strip()
    
    # 커밋 데이터 파싱
    commit_parts = commit_data.split(' ', 4)  # 해시, 작성자, 날짜, 메시지, 본문으로 분리
    commit_hash = commit_parts[0]  # 커밋 해시
    commit_author = commit_parts[1]  # 작성자
    commit_date = commit_parts[2]  # 날짜
    commit_message = commit_parts[3]  # 메시지
    commit_description = commit_parts[4] if len(commit_parts) > 4 else ""  # 본문 (있을 경우만)

    return commit_date, commit_message, commit_description

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
  
  commit_date, title, subject = get_commit_info()
  data = {
      "Subject": [subject],
      "Title": title
  }
  payload = database.create_page_payload(data)
  
  res = database.create_page(page_payload=payload)
  
  