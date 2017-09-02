# -*- coding: utf-8 -*-
import sys

from django.core.urlresolvers import reverse_lazy

reload(sys)
sys.setdefaultencoding('utf-8')


class TeamTable():
    """Table for all team settings"""

    TEAM_LIST_COUNT = 20  # 한 페이지에 표시될 게시물 수

    CATEGORY = [
        None,
        ['레이드', '나이트폴', '스트라이크', '퀘스트', '크루시블', '기타'],  # 0
    ]

    TEAM_TABLES = [
        # ('게시판 제목', '게시판 설명', '카테고리')
        ['', '', 0],  # 0
        ['파티찾기 PS4', '회원정보에 PSN 아이디를 지정해두면 자동으로 입력됩니다.', 1],  # 1
        ['파티찾기 Xbox', '회원정보에 Live 아이디를 지정해두면 자동으로 입력됩니다.', 1],  # 2
        ['파티찾기 PC', '회원정보에 배틀태그를 지정해두면 자동으로 입력됩니다.', 1],  # 3
    ]

    def get_list_count(self):
        """Get list count"""
        return self.TEAM_LIST_COUNT

    def get_table_len(self):
        """Get number of tables"""
        return len(self.TEAM_TABLES)

    def get_table_name(self, table):
        """Get name of the table"""
        return self.TEAM_TABLES[int(table)][0]

    def get_table_url(self, table):
        """Get URL of the table"""
        return reverse_lazy('teams:recruitment', args=[table, 1])

    def get_table_desc(self, table):
        """Get description of the table"""
        return self.TEAM_TABLES[int(table)][1]

    def get_table_category(self, table):
        """Get category of the table"""
        return self.TEAM_TABLES[int(table)][2]

    def get_category(self, table):
        """Get pre-defined category for the table"""
        return self.CATEGORY[(self.TEAM_TABLES[int(table)][2])]

    def get_table_list(self):
        """Get TEAM_TABLES"""
        return self.TEAM_TABLES
