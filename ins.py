from selenium import webdriver
import time, json, random


class Ins:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
    
    def login(self, username, password):
        self.driver.get('https://www.instagram.com/')
        time.sleep(1)
        self.driver.find_element_by_css_selector('input[name="username"]').send_keys(username)
        time.sleep(0.2)
        self.driver.find_element_by_css_selector('input[name="password"]').send_keys(password)
        time.sleep(0.2)
        self.driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF').click()
        time.sleep(5)
    
    def get_dict(self):
        _str = self.driver.find_element_by_css_selector('pre').text
        _dict = json.loads(_str)
        return _dict
    
    def get_target_id(self, target_username):
        self.driver.get('https://www.instagram.com/{}/?__a=1'.format(target_username))
        time.sleep(1)
        _dict = self.get_dict()
        return _dict['graphql']['user']['id']
    
    def set_target_id(self, target_id):
        self.target_id = target_id
    
    def get_followers(self):
        _list = []
        after = ''
        while True:
            self.driver.get('https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={{"id":"{}","first":50,"after":"{}"}}'.format(self.target_id, after))
            time.sleep(random.randint(1, 5))
            _dict = self.get_dict()
            for val in _dict['data']['user']['edge_followed_by']['edges']:
                _list.append([val['node']['id'], val['node']['username']])
            after = _dict['data']['user']['edge_followed_by']['page_info']['end_cursor']
            if after == '':
                break
        return _list
    
    def get_following(self):
        _list = []
        after = ''
        while True:
            self.driver.get('https://www.instagram.com/graphql/query/?query_hash=3dec7e2c57367ef3da3d987d89f9dbc8&variables={{"id":"{}","first":50,"after":"{}"}}'.format(self.target_id, after))
            time.sleep(random.randint(1, 5))
            _dict = self.get_dict()
            for val in _dict['data']['user']['edge_follow']['edges']:
                _list.append([val['node']['id'], val['node']['username']])
            after = _dict['data']['user']['edge_follow']['page_info']['end_cursor']
            if after == '':
                break
        return _list
    
    def quit(self):
        self.driver.quit()


def write_followers(_list):
    with open('followers.json', 'r') as f:
        _dict = json.load(f)
    _dict[time.strftime('%m%d', time.localtime())] = _list
    with open('followers.json', 'w') as f:
        json.dump(_dict, f)

def write_following(_list):
    with open('following.json', 'r') as f:
        _dict = json.load(f)
    _dict[time.strftime('%m%d', time.localtime())] = _list
    with open('following.json', 'w') as f:
        json.dump(_dict, f)


def commend_init():
    username = input('username: ')
    password = input('password: ')
    target_username = input('target_username: ')
    try:
        ins = Ins()
        ins.login(username, password)
        target_id = ins.get_target_id(target_username)
        ins.quit()
    except:
        ins.quit()
        print('error')
    else:
        _dict = {'username': username, 'password': password, 'target_id': target_id}
        with open('info.json', 'w') as f:
            json.dump(_dict, f)
        _dict = {}
        with open('followers.json', 'w') as f:
            json.dump(_dict, f)
        with open('following.json', 'w') as f:
            json.dump(_dict, f)

def commend_run():
    with open('info.json', 'r') as f:
        _dict = json.load(f)
    try:
        ins = Ins()
        ins.login(_dict['username'], _dict['password'])
        ins.set_target_id(_dict['target_id'])
        followers = ins.get_followers()
        following = ins.get_following()
        ins.quit()
    except:
        ins.quit()
        print('error')
    else:
        write_followers(followers)
        write_following(following)
    
def commend_Run():
    while True:
        date = time.strftime('%m%d', time.localtime())
        with open('followers.json', 'r') as f:
            dict1 = json.load(f)
        with open('following.json', 'r') as f:
            dict2 = json.load(f)
        if date not in dict1 or date not in dict2:
            commend_run()
        time.sleep(3600)

def commend_compare():
    def compare(list1, list2):
        dict1 = {v1: v2 for v1, v2 in list1}
        dict2 = {v1: v2 for v1, v2 in list2}
        set1 = set(dict1.keys())
        set2 = set(dict2.keys())
        print(' ', 'decrease')
        for val in set1.difference(set2):
            print('   ', dict1[val])
        print(' ', 'increase')
        for val in set2.difference(set1):
            print('   ', dict2[val])
    date1 = input('date1: ')
    date2 = input('date2: ')
    with open('followers.json', 'r') as f:
        dict1 = json.load(f)
    with open('following.json', 'r') as f:
        dict2 = json.load(f)
    if date1 in dict1 and date1 in dict2 and date2 in dict1 and date2 in dict2:
        print('followers')
        compare(dict1[date1], dict1[date2])
        print('following')
        compare(dict2[date1], dict2[date2])
    else:
        if date1 not in dict1 or date1 not in dict2:
            print('error', date1)
        if date2 not in dict1 or date2 not in dict2:
            print('error', date2)


def commend_help():
    print("選取登入後: 依照指示輸入帳號及密碼後，輸入欲觀察之對象user_name。")
    print("選取執行後: 會依照登入之資訊，自動抓取觀察對象的followers & followings至資料庫中")
    print("選取自動執行後: 每天自動抓資料")
    print("選取比對後: 填入欲分析且已經抓取過資料的兩天日期，即能夠比對這兩天的followers & followings變動")
    
    
if __name__ == '__main__':
    print('There are six commends: 登入(init), 執行(run), 自動執行(Run), 比對(compare), 幫助(help), 退出(quit)')
    while True:
        commend = input('> ')
        if commend == '登入' or commend == "init":
            commend_init()
        elif commend == '執行' or commend == "run":
            commend_run()
        elif commend == '自動執行' or commend == "Run":
            commend_Run()
        elif commend == '比對' or commend == "compare":
            commend_compare()
        elif commend == '幫助'  or commend == "help":
            commend_help()
        elif commend == '退出' or commend == "quit":
            break
        else:
            print('error')