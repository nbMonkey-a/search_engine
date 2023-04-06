from django.shortcuts import render
from elasticsearch import Elasticsearch
from pprint import pprint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
#look 很多权限验证和中间件，都在contrib里
from . import models
import hashlib
import csv

client = Elasticsearch('127.0.0.1', port='9200')

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')
#---------------------------------------------------------------
def login(request): 
    if request.method == 'GET':
        # 用户初次进入展示登录表单
        return render(request, 'login.html')
    elif request.method == 'POST':

        # 给前端传参
        context = {
            'message': ''
        } 

        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')  # 从前端name属性中取值

        # 验证账户名密码
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:  #look hash密码判断写法
            # if user.password == password:  #look 明文密码判断
                context['message'] = '登录成功'
                # look 服务器设置sessionid和其它用户信息。sessionid（服务器给访问它的游览器的身份证）自动生成的。
                # look request.session对象就是django_session表，['is_login']这种键值对的存储，其实就是存在了django_session表里的session_data字段，这个字段是哈希加密的，解密后就是一个键值对的字典
                request.session['is_login'] = True
                request.session['username'] = user.name
                request.session['userid'] = user.id
                return redirect('/index/')  # 返回的响应中包含set-cookie(sessionid='adadaDAD')，游览器收到响应后会把sessionid存到cookie中。
            else:
                context['message'] = '密码不正确'
                return render(request, 'login.html', context=context)
        else:
            context['message'] = '未注册' 
            return render(request, 'login.html', context=context)

def logout(request):
    """ 登出 """
    # 如果session没有的话，用session["is_login"]会报键错误
    # （老师把这句话删了）未登录时不让走登录
    # if not request.session.get('is_login'):
    #     return redirect('/index/')

    # 清除session 登出
    request.session.flush()   # 清除此用户session对应的所有sessiondata
    # del request.session['user_id']  # 清除某个session键值对
    return redirect('/index/')

def _hash_password(password):  # _开头表示内部使用
    """哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()
#--------------------------------------------------------------------------
def search(request):
    key_words = request.GET.get('q', '')
    page_size = 10
    page = request.GET.get('p', '1')  # 获取访问页码
    try:
        page = int(page) 
    except:
        page = 1

    start_time = datetime.now()
    response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
        index="equips",  # 设置索引名称
        doc_type="doc",  # 设置表名称
        # scroll='5m',
        body={  # 书写elasticsearch语句
            "query": {
                "multi_match": {  # multi_match查询
                    "query": key_words,  # 查询关键词
                    "fields": ["title", "description"]  # 查询字段
                }
            },
            "from": (page-1)*page_size,  # 从第几条开始获取
            "size": page_size,  # 获取多少条数据
            "highlight": {  # 查询关键词高亮处理
                "pre_tags": ['<span class="keyWord">'],  # 高亮开始标签
                "post_tags": ['</span>'],  # 高亮结束标签
                "fields": {  # 高亮设置
                    "title": {},  # 高亮字段
                    "description": {},  # 高亮字段
                }
            }
        }
    )
    # scroll_id = response['_scroll_id']
    

    end_time = datetime.now()
    search_time = (end_time - start_time).total_seconds()
    total = response["hits"]["total"]
    if (page % page_size) > 0:  # 计算页数
        page_num = int(total / page_size) + 1
    else:
        page_num = int(total / page_size)

    response_hits = response["hits"]["hits"]
    hit_list = []
    for hit in response_hits:
        hit_dict = {}
        if "title" in hit["highlight"]:
            hit_dict["title"] = "".join(hit["highlight"]["title"])
        else:
            hit_dict["title"] = hit["_source"]["title"]

        if "description" in hit["highlight"]:
            hit_dict["description"] = "".join(hit["highlight"]["description"])[:500]
        else:
            hit_dict["description"] = hit["_source"]["description"]

        hit_dict["url"] = hit["_source"]["url"]                         # 获取返回url
        hit_dict["create_date"] = hit["_source"]["riqi"]
        hit_dict["score"] = hit["_score"]
        hit_dict["source_site"] = hit["_source"]["site"]
        hit_list.append(hit_dict)

    #     for i in range(0, int(total/100)+1):
    # # scroll参数必须指定否则会报错
    #         query_scroll = response.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
    #         results += query_scroll

    with open(r'./static/file/'+ key_words +'.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['所属公司', '设备描述', '设备链接', '发布日期', '相关度评分', '来源'])
        for hit in response_hits:
            writer.writerow([hit['_source']['title'],hit["_source"]["description"],hit["_source"]["url"],hit["_source"]["riqi"],hit["_score"],hit["_source"]["site"]])
    # with open(r'E:\毕业设计相关文档\案例\SimpleSearchEngine-main\django_search_engine\static\file\ '+ key_words +'.csv','w',newline='',encoding='utf-8') as flow:
    #     csv_writer = csv.writer(flow)
    #     for res in response_hits:
    #         print(res)
    #         csv_writer.writerow([res['_id']+','+res['_source']['title']])
# 将该循环得到的信息导出为Excel格式
    # import csv
    # from django.http import HttpResponse

    # re = HttpResponse(content_type='text/csv')
    # re['Content-Disposition'] = 'attachment; filename= ' + key_words + ".csv"
    # re.write(u'\ufeff'.encode('utf8'))
    # with open(r'E:\毕业设计相关文档\案例\SimpleSearchEngine-main\django_search_engine\static\file\ '+ key_words +'.csv', 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(re)
    #     writer.writerow(['Title', 'Description', 'URL', 'Create Date', 'Score', 'Source Site'])
    #     for hit in hit_list:
    #         writer.writerow([hit['title'], hit['description'], hit['url'], hit['create_date'], hit['score'], hit['source_site']])

    # return re

# import csv
# from django.http import HttpResponse

# def export_csv(request):
#     key_words = request.GET.get('q', '')
#     response = client.search(
#         index="equips",
#         doc_type="doc",
#         body={
#             "query": {
#                 "multi_match": {
#                     "query": key_words,
#                     "fields": ["title", "description"]                }
#             },
#             "size": 10000  # 设置导出的最大数量
#         } 
#     )
#     response_hits = response["hits"]["hits"]
#     hit_list = []
#     for hit in response_hits:
#         hit_dict = {}
#         hit_dict["title"] = hit["_source"]["title"]
#         hit_dict["description"] = hit["_source"]["description"]
#         hit_dict["url"] = hit["_source"]["url"]
#         hit_dict["create_date"] = hit["_source"]["riqi"]
#         hit_dict["source_site"] = hit["_source"]["site"]
#         hit_list.append(hit_dict)

#     # 设置响应头
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename= ' + key_words + ".csv"

#     # 写入csv文件
#     writer = csv.writer(response)
#     writer.writerow(['Title', 'Description', 'URL', 'Create Date', 'Source Site'])
#     for hit in hit_list:
#         writer.writerow([hit['title'], hit['description'], hit['url'], hit['create_date'], hit['source_site']])

        # return response

    # return_dict =
    return render(request, 'result.html', {
        "page": page,
        'page_num': page_num,
        "total": total,
        "all_hits": hit_list,
        "key_words": key_words,
        "search_time": search_time,
        # "re":re 
    })

