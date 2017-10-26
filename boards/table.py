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

    SAMPLE_LIMIT = 10  # 포탈에서 샘플로 보여줄 리스트 수
    SAMPLE_LIMIT_MOBILE = 5  # 포탈 모바일용 샘플 리스트 수
    SAMPLE_NOTICE = 3  # 포탈에서 샘플로 보여줄 공지사항 수

    CATEGORY = [
        None,
        ['잡담', '질문', '홍보'],  # 1
        ['정보', '강좌', '팁'],  # 2
    ]

    BOARD_TABLES = [
        # ('게시판 제목', '게시판 설명', '카테고리')
        # 0: 카테고리 안씀
        # > 0: CATEGORY 에 설정된 카테고리 사용
        # 0 ~ 9 관리자만(superuser, staff) 쓰기 가능
        ['최신글', '모든 게시판의 최근 게시물을 모아봅니다.', 0],  # 0: 쓰기금지
        ['전체공지', '', 0],  # 1
        ['공지사항', '', 0],  # 2
        ['도움말', '', 0],  # 3
        ['', '', 0],  # 4
        ['', '', 0],  # 5
        ['', '', 0],  # 6
        ['', '', 0],  # 7
        ['신고게시판', '신고 게시판의 모든 글은 글쓴이와 관리자만 볼 수 있습니다.', 0],  # 8: 비밀글
        ['베스트', '추천을 많이 받은 게시물이 자동 등록됩니다.', 0],  # 9
        # 회원 쓰기 가능
        ['운영/문의/건의', '사이트 운영에 대한 건의나 문의, 버그신고 게시판입니다. 신고는 비밀글을 지원하는 신고게시판을 이용해 주세요.', 0],  # 10
        ['정보게시판', '각종 정보, 강좌나 팁을 공유합니다.', 2],  # 11
        ['자유게시판', '', 1],  # 12
    ]

    def get_list_count(self):
        """Get list count"""
        return self.BOARD_LIST_COUNT

    def get_sample_limit(self):
        """Get sample limit"""
        return self.SAMPLE_LIMIT, self.SAMPLE_LIMIT_MOBILE

    def get_sample_notice(self):
        """Get sample notice"""
        return self.SAMPLE_NOTICE

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
        return reverse_lazy('boards:show_list', args=[table, 1])

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
            elif int(table) == 8:
                writable = True
            elif int(table) < 8 and not request.user.is_staff:
                writable = False
        else:
            writable = False

        return writable
