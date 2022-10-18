import csv
import time
student_infos = []

def load_stu_info():
    """
    加载学生信息
    从stu_infos.csv文件中加载数据
    :return: 无
    """
    with open(r"stu_infos.csv", encoding='utf-8-sig') as file:
        f_csv = csv.reader(file)
        header = next(f_csv)
        for row in f_csv:
            student_info = {}
            for index in range(3):
                student_info[header[index]] = row[index]
            student_infos.append(student_info)


def login():
    """
    用户使用学号和密码进行登录
    最多让用户登录三次，如果连续三次都登录失败（用户名或者密码错误），只要密码和用户都正确表示登录成功
    :return:登录成功返回True和学号，三次都登录失败返回False和None
    """
    retry_time = 0
    while retry_time < 3:
        user_no = input('请输入登录账号：')
        password = input('请输入密码：')
        for i in student_infos:
            if i['no']==user_no and i['password']==password:
                return True,user_no
        print('用户名或者密码错误！！！请重新输入。')
        retry_time += 1
    else:
        return False, None

def add(user_no):
    for x in student_infos:
        if user_no==x['no']:
            name=x['name']
            break
    times=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    choices=['出勤','迟到','请假','缺勤']
    a=int(input("\t该学生出勤情况：1-出勤\t2-迟到\t3-请假\t4-缺勤:"))
    if a==1:
        data=choices[0]
    elif a==2:
        data=choices[1]
    elif a==3:
        data=choices[2]
    else:
        data=choices[3]
    with open(r"attendance.csv",'a+',newline='', encoding='utf-8') as f:
        wf = csv.writer(f)
        wf.writerow([user_no,name,times,data])#写入一行数据
        print("{}同学{}数据已经写入成功！操作时间是{}".format(name,data,times))


def select():
    student = []
    with open(r"attendance.csv", encoding='utf-8-sig') as file:
        f_csv = csv.reader(file)
        header = next(f_csv)
        for row in f_csv:
            students = {}
            for index in range(4):
                students[header[index]] = row[index]
            student.append(students)
        name=input("请输入你需要查找的姓名：")
        print("  学号\t\t姓名\t\t操作时间\t\t出勤状态")
        for a in student:
            if a['name']==name:
                print(a['no']+'\t'+a['name']+'\t'+a['time']+'\t\t'+a['state'])
            else:
                print("无此人！！！")
                break


if __name__ == '__main__':
    load_stu_info()
    success, stu_no = login()
    print(stu_no)
    if success:
        print('登录成功！')
        add(stu_no)
        q = int(input("你想要查询出勤数据吗？\tyes(1)--no(0)"))
        if q == 1:
            select()
        else:
            print("欢迎下次登录电子考勤系统")
    else:
        print('登录失败')
