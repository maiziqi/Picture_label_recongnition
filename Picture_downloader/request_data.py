import spider
import download

# 设置根url 获取唯品会商品页面内容
root_url = 'https://category.vip.com/'
soup = spider.get_soup(root_url)

# 抓取tree_id、c_id
tree_id = spider.get_tree_id(soup)
c_id = spider.get_c_id(soup)

for c_item in c_id[9:11]:
    # 使用tree_id、c_id设置获取类别对应链接的url
    format_url = 'https://category.vip.com/ajax/getTreeList.php?cid={}&tree_id={}'.format(c_item, tree_id)
    url_soup = spider.get_soup(format_url)
    name_dic = spider.get_name_dic(url_soup)
    url_dic = spider.get_url_dic(url_soup, name_dic)
    for folder, url in url_dic.items():
        product_list = spider.get_product_list(url)
        # 由于唯品会网站限制，先取前五十个进行存取
        download.down_img(folder, product_list[:50])
        if len(product_list) >= 50:
            download.down_img(folder, product_list[50:])
        print(folder + ' 已下载完成')
