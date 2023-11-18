import MySQLdb # MySQLdb(데이터베이스와 상호 작용) 모듈을 가져옴.
# a_init_data 모듈(파이썬 코드가 포함된 파일)에서 loc_code_list를 가져옴.
from a_init_data import loc_code_list

# MySql에 테이블을 만드는 함수.
def create_loc_code_tbl():
    # 지역 리스트를 요소들을 반복할 것: 
    for loc_code in loc_code_list:
        # MySql DB(데이터베이스)와 연결하는 변수 conn
        conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="1234", db="c")

        # 데이터베이스에서 사용할 명령문을 f-String 방법으로 작성하여 sql변수에 저장함.
        sql = f'''CREATE TABLE %s_tbl (
                    date_day date,
                    loc_code varchar(5),
                    total_cases DOUBLE,
                    total_deaths DOUBLE,
                    total_vaccinations DOUBLE,
                    total_population DOUBLE
                )'''%loc_code

        # conn(데이터베이스와 연결하는 변수)를 사용할 것임
        with conn:
            # conn의 cursor():데이터베이스에 쿼리를 보내고 쿼리 결과를 검색, 수정, 추가, 삭제하는 기능을 사용할 것임. 이걸 cur로 부르겠다!
            with conn.cursor() as cur:
                # sql변수로 데이터베이스 내에서 쿼리 실행!
                cur.execute(sql)
                # 데이터베이스 커밋
                conn.commit()

# 직접 실행될 때만 밑의 내용을 실행함.
if __name__ == '__main__':
    # create_loc_code_tbl 함수 호출
    create_loc_code_tbl()