# 引入Django自带的Paginator
from django.core.paginator import Paginator


def Custom_Paginator(obj: object, page: object, page_size: object) -> object:
    page = int(page)
    page_size = int(page_size)
    # 将接收到的obj变量按照page_size分页
    paginator = Paginator(obj, page_size)

    # 得到当前page的数据列表
    page_of_obj = paginator.get_page(page)

    # 上一页
    has_previous = page_of_obj.has_previous()

    # 下一页
    has_next = page_of_obj.has_next()

    # 当前页码
    current_page_num = page_of_obj.number

    # 总页数
    total_page = paginator.num_pages  # 总页数

    # 数据记录总数
    count = paginator.count

    # 这里判断左右两边的页码小于最小页数或大于最大页数
    if current_page_num - 1 <= 0:
        prevous_page_num = 1
    else:
        prevous_page_num = current_page_num - 1

    if current_page_num + 1 >= total_page:
        next_page_num = total_page
    else:
        next_page_num = current_page_num + 1

    # 重点！！！这里判断两遍的省略号，用get_elided_page_range()方法，给它提供当前页码
    page_range = list(paginator.get_elided_page_range(number=page))
    if current_page_num * page_size - page_size == 0:
        current_start_num = 1
    else:
        current_start_num = current_page_num * page_size - page_size
    if current_page_num * page_size > count:
        current_end_num = count
    else:
        current_end_num = current_page_num * page_size

    # 封装一下数据
    data = {
        # 注意这里得到的当前页码的数据列表是QuerySet，不能直接返回前端，会报错
        # 还需要拿到data后简单转换一下
        'objects_list': page_of_obj,
        'has_previous': has_previous,
        'has_next': has_next,
        'page_range': page_range,
        'elided': page_of_obj.paginator.ELLIPSIS,
        'current_page': current_page_num,
        'prevous_page_num': prevous_page_num,
        'next_page_num': next_page_num,
        'current_start_num': current_start_num,
        'current_end_num': current_end_num,
        'total_page': total_page,
        'total': count,
    }

    return data