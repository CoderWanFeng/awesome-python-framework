from tinydb import TinyDB

db = TinyDB('./city_fly.json')

ci_t = db.table('city_index')
ci_t.insert({'city': '广州', 'index': 55})
ci_t.insert({'city': '北京', 'index': 66})
ci_t.insert({'city': '杭州', 'index': 77})
ci_t.insert({'city': '重庆', 'index': 88})

ci_l = db.table('city_line')
ci_l.insert({'from': '广州', 'to': '上海'})
ci_l.insert({'from': '广州', 'to': '北京'})
ci_l.insert({'from': '广州', 'to': '杭州'})
ci_l.insert({'from': '广州', 'to': '重庆'})
