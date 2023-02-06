'''the main purpose of this function is to filter spam post'''
def is_spam_post(post_content):
    spam_keyword = [
        'Make sure you sub to my channel bras',
        'MemeBook', 
        'web3social',
        'web3社交+投研',
        '你所不了解的币圈',
        '123导航',
        'airdrops',
        '黄站',
        'Damus最大',
        '波場用戶回饋',
        'damus中文最大电',
        'Sign up to get 6TRX',
        '成人短视频',
        'Thanks me later',
        '澳门金沙',
        '早期好项目',
        '全国同城约',
        '全球华人社区群',
        'Meet girls nak',
        '广告机器人卡',
        '全国同城',
        '引流',
        '支付宝',
        '红包',
        '推广',
        '黑丝',
        '友好交流，长期看好',
        '互帮互助',
        '灰产',
        '互联网打工人',
        '湾区中国留学生',
        'Click the link below to recei',
        '硅谷攻城狮',
        '管理 3D 设置',
        '加群不迷路',
        '群推工具',
        'Resource search robot'
    ]
    for w in spam_keyword:
        if w in post_content:
            return True
    return False