import json

import requests

from Get_All_Course import get_all_course


def exam_list(stuId):
    allcourse = get_all_course(stuId)
    url = 'https://zjyapp.icve.com.cn/newmobileapi/onlineExam/getExamList_new'
    data = {
        'openClassId': allcourse['openClassId'],
        'courseOpenId': allcourse['courseOpenId'],
        'pageSize': '100',
        'stuId': stuId,
    }
    html = requests.post(url=url, data=data).json()
    if html['code'] == 1:
        return html['examList']
    else:
        print(html['msg'])
        input("回车退出！")


def answer(examid, title):
    url = 'https://zjyapp.icve.com.cn/newmobileapi/onlineExam/previewOnlineExam'
    data = {
        'examId': examid
    }
    html = requests.post(url=url, data=data).json()['data']
    with open(f'{title}.txt', 'w', encoding='utf8') as f:
        for i in html['questions']:
            f.write(f'{int(i["sortOrder"]) + 1},{i["title"]}\n')
            try:
                for j in json.loads(i['dataJson']):
                    select = j["SortOrder"].replace('0', 'A').replace('1', 'B').replace('2', 'C').replace('3', 'D')
                    if select == 0:
                        select = 'A'
                    elif select == 1:
                        select = 'B'
                    elif select == 2:
                        select = 'C'
                    elif select == 3:
                        select = 'D'
                    f.write(f'{select},{j["Content"]}\n')
                answer = i["answer"].replace('0', 'A').replace('1', 'B').replace('2', 'C').replace('3', 'D')
                f.write(f'Answer:{answer}\n')
            except:
                pass
    input("答案已生成在软件目录下。请回车退出")


def main(stuid):
    exams = exam_list(stuid)
    index = 1
    for i in exams:
        print(f'【{index}】{i["title"]}\t{i["startDate"]}')
        index += 1
    target = exams[int(input("请输入序号：")) - 1]
    answer(target['examId'], target['title'])


if __name__ == '__main__':
    main('')
