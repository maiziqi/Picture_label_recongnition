import requests
import re
from bs4 import BeautifulSoup


def get_soup(url):
    """通过requests获取静态网页内容并使用BeautifulSoup渲染"""
    r = requests.get(url)
    # 生成BeautifulSoup对象，使用lxml第三方解析器
    soup = BeautifulSoup(r.text, "lxml")
    return soup.text


def write_file(text, file_type):
    """在程序开发过程中，将中间网站静态代码转化成文本，方便在编辑器中查看"""
    filename = 'sample.' + file_type
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def get_tree_id(soup):
    """通过正则表达式搜索返回tree_id"""
    return re.search(r'"tree_id":(\d+)', soup).group(1)


def get_c_id(soup):
    """通过正则表达式搜索返回c_id"""
    return re.findall(r'"cate_id":"(\d+)"', soup)


def get_name_dic(soup):
    """通过正则表达式搜索一二级标签编号及对应名称，并以字典形式返回"""
    cate_list = re.findall(r'"cate_id":"(\d+)","cate_type":"[12]","cate_name":"([\\u\w+/]+)"', soup)
    name_dic = {}
    for item in cate_list:
        name_dic[item[0]] = url_simplify(item[1])
    return name_dic


def get_url_dic(soup, name_dic):
    """通过正则表达式搜索三级标签对应的上级标签编号，对应的url，并将整体名称以及url以字典形式返回"""
    cate = re.findall(r'"cate_id":"(\d+)","cate_type":"(3)","cate_name":"([\\u\w+/]+)","top_cate_id":"(\d+)",'
                      r'"sub_cate_id":"(\d+)",.*?"url":"(.*?)"', soup)

    # 将三级菜单中的链接与文件夹名对应存放在字典中
    url_dic = {}
    for item in cate:
        name = 'F:/数据集/训练集/'
        for key, value in name_dic.items():
            if item[3] == key:
                name += value
            if item[4] == key:
                name = name + '_' + value
        name1 = name + '_' + url_simplify(item[2])
        url_dic[name1] = item[5]
        # 将第二页数据url替换后放入字典中
        name2 = name + '_' + url_simplify(item[2]) + '_2'
        url_dic[name2] = re.sub(r'search-1-0-1', 'search-1-0-2', item[5])
        # 将第三页数据url替换后放入字典中
        name2 = name + '_' + url_simplify(item[2]) + '_3'
        url_dic[name2] = re.sub(r'search-1-0-1', 'search-1-0-3', item[5])

    return url_dic


def get_product_list(url):
    """获取当前小类下的各个product_id"""
    pic_url = "https://category.vip.com/{}".format(url)
    # 获取爬取图片链接所需product_id
    pic_soup = get_soup(pic_url)
    product_raw = re.search('"productIds":\[(.*?)\]', pic_soup)
    return re.findall('"(\d+)"', product_raw.group(1))


def get_img_url(product_list):
    """使用product_id完成爬取图片所需url"""
    img_url = "https://category.vip.com/ajax/mapi.php?service=product_info&productIds="
    for product_id in product_list:
        img_url += product_id
        if product_id != product_list[-1]:
            img_url += "%2C"
    img_url += "&functions=brandShowName%2CsurprisePrice%2CpcExtra&warehouse=VIP_NH" \
               "&mobile_platform=1&app_name=shop_pc&app_version=4.0"
    return img_url


def get_img_list(soup):
    """通过正则表达式搜索返回图片链接"""
    return re.findall('"(?:image3|image7|smallImage)":"(.*?)",', soup)


def url_simplify(url):
    """将带有反斜杠的url修改回正常url"""
    return url.encode('utf-8').decode('unicode_escape').replace('\\/', '')


def folder_name_simplify(folder):
    """修改字典key值使同样分类的图片下载至同一个文件夹"""
    return re.sub(r'(_2)|(_3)', '', folder)
