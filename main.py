import requests
import json
import time

def get_comments(oid, max_page=5):
    cookies = {
        'SESSDATA': 'xxx',
        'bili_jct': 'xxx'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://t.bilibili.com/{oid}'
    }
    comments = []
    for page in range(1, max_page+1):
        url = f'https://api.bilibili.com/x/v2/reply/main?oid={oid}&type=17&next={page}&mode=3'
        try:
            resp = requests.get(url, headers=headers, cookies=cookies)
            data = resp.json()
            if data['code'] == 0:
                for reply in data['data']['replies']:
                    comment = {
                        '用户': reply['member']['uname'],
                        '内容': reply['content']['message'],
                        '时间': time.strftime("%Y-%m-%d %H:%M", 
                                   time.localtime(reply['ctime'])),
                        '点赞数': reply['like']
                    }
                    comments.append(comment)
                print(f'第 {page} 页获取成功')
            else:
                print(f'错误：{data["message"]}')
            time.sleep(1)  # 防止触发频率限制
        except Exception as e:
            print(f'请求失败：{str(e)}')
            break
    return comments

# 使用示例
dynamic_id = '836681344644808744'  # 替换实际动态ID
comments = get_comments(dynamic_id)
for comment in comments:
    print(json.dumps(comment, ensure_ascii=False))
print(f'共获取 {len(comments)} 条评论')