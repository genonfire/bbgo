# -*- coding: utf-8 -*-
import sys

from django.core.urlresolvers import reverse_lazy

reload(sys)
sys.setdefaultencoding('utf-8')


class BoardTable():
    """Table for all board settings"""

    BOARD_LIST_COUNT = 20  # 한 페이지에 표시될 게시물 수
    BEST_THRESHOLD = 20  # 베스트로 갈 추천 수
    VETO_THRESHOLD = 10  # 베스트로 못가게 비토할 비추 수

    CATEGORY = [
        None,
        ['잡담', '질문', '팁', '정보', '홍보'],  # 0
    ]

    BOARD_TABLES = [
        # ('게시판 제목', '게시판 설명', '카테고리')
        # 0: 카테고리 안씀
        # > 0: CATEGORY 에 설정된 카테고리 사용
        # 0 ~ 9 관리자만(superuser, staff) 쓰기 가능
        ['최신글', '모든 게시판의 최근 게시물을 모아봅니다.', 0],  # 0: 쓰기금지
        ['전체공지', '', 0],  # 1
        ['도움말', '', 1],  # 2
        ['', '', 0],  # 3
        ['', '', 0],  # 4
        ['', '', 0],  # 5
        ['', '', 0],  # 6
        ['', '', 0],  # 7
        ['', '', 0],  # 8
        ['핫게', '추천을 많이 받은 게시물이 자동 등록됩니다.', 0],  # 9
        # 회원 쓰기 가능
        ['게시판', '게시판 입니다.', 1],  # 10
    ]

    def get_list_count(self):
        """Get list count"""
        return self.BOARD_LIST_COUNT

    def get_best_threshold(self):
        """Get best threshold"""
        return self.BEST_THRESHOLD

    def get_veto_threshold(self):
        """Get veto threshold"""
        return self.VETO_THRESHOLD

    def get_table_len(self):
        """Get number of tables"""
        return len(self.BOARD_TABLES)

    def get_table_name(self, table):
        """Get name of the table"""
        return self.BOARD_TABLES[int(table)][0]

    def get_table_url(self, table):
        """Get URL of the table"""
        return reverse_lazy('boards:show_list_0', args=[table])

    def get_table_desc(self, table):
        """Get description of the table"""
        return self.BOARD_TABLES[int(table)][1]

    def get_table_category(self, table):
        """Get category of the table"""
        return self.BOARD_TABLES[int(table)][2]

    def get_category(self, table):
        """Get pre-defined category for the table"""
        return self.CATEGORY[(self.BOARD_TABLES[int(table)][2])]

    def get_table_list(self):
        """Get BOARD_TABLES"""
        return self.BOARD_TABLES

    def writable(self, request, table):
        """Writable for table"""
        if request.user.is_authenticated():
            writable = True
            if int(table) == 0 or int(table) == 9:
                writable = False
            elif int(table) < 10 and not request.user.is_staff:
                writable = False
        else:
            writable = False

        return writable
