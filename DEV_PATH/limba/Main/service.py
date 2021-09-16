from rest_framework.pagination import PageNumberPagination

"""Pagination Users"""
class PaginationUsers(PageNumberPagination):
    page_size = 300
    max_page_size = 3000

"""Pagination UsersAllInfo"""
class PaginationUsersInfo(PageNumberPagination):
    page_size = 300
    max_page_size = 3000

"""Pagination Objects"""
class PaginationObjects(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination Departments"""
class PaginationDepartments(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination SubDepartments"""
class PaginationSubDepartments(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination MainTasks"""
class PaginationMainTasks(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination SubTasks"""
class PaginationSubTasks(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination MainTaskImages"""
class PaginationMainTaskImgs(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination SubTaskImages"""
class PaginationSubTaskImgs(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination MainTaskComments"""
class PaginationMainTaskComments(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

"""Pagination SubTaskComments"""
class PaginationSubTaskComments(PageNumberPagination):
    page_size = 100
    max_page_size = 3000

