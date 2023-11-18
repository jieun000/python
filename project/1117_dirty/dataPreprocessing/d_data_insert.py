import csv # CSV 파일을 읽기 위한 라이브러리
import MySQLdb # MySQL 데이터베이스와 연동하기 위한 라이브러리
import datetime # 날짜 및 시간을 다루기 위한 라이브러리
from a_init_data import loc_code_list

# 문자열을 실수로 변환하는 함수
def string_to_float(s):
    """
    csv의 열데이터'date_day, total_cases, total_deaths,people_vaccinated' 중 Nan이 있어
    float()함수가 제대로 작동하지 않아 빈 문자열을 0.0으로 변환하는 함수를 작성
    """
    # 빈 문자열은 0.0으로 반환
    if s=='': return 0.0
    # 숫자면 실수형으로 반환
    else: return float(s)

# 데이터베이스에 삽입(insert) 함수
def insert_data():
    # 지역 리스트 인자 돌리며 반복.
    for loc_code in loc_code_list:
        # CSV 파일 열고 이걸 csvfile로 부를 것임: 
        with open(f'../data_segment_by_loc_code/%s.csv'%loc_code) as csvfile:
             # CSV 파일을 딕셔너리 형태로 만들어 reader로 저장. 
            reader = csv.DictReader(csvfile, delimiter=',')
            # CSV 파일의 각 행 반복.
            for  idx,row in enumerate(reader):
                # MySql DB연결.
                conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="1234", db="c")
                # 지역 코드 이름인 테이블에 데이터를 삽입하는 SQL 쿼리 작성 (17개 시도).
                sql_statement = f'INSERT INTO %s_tbl'%loc_code +'(date_day,loc_code, total_cases, total_deaths,total_vaccinations,total_population ) VALUES (%s,%s,%s,%s,%s,%s)'

                # 'date_day' 칼럼을 날짜로 변환.
                date_day = datetime.datetime.strptime(row['date_day'], '%Y-%m').date()
                # 데이터베이스 커서 생성.
                cur = conn.cursor()
                # CSV 파일의 각 행의 열들을 튜플 형태로 저장.
                tupled_list= (date_day,loc_code, string_to_float(row['total_cases']), string_to_float(row['total_deaths']), string_to_float(row['total_vaccinations']), string_to_float(row['total_population']))
                # 데이터베이스 커서 실행 (sql문에 f-string으로 연결).
                cur.execute(sql_statement, tupled_list)
                # 특수 문자, 사용자가 입력한 SQL인젝션 공격(악의적인 SQL 코드)등을 방지하기 위한 이스케이프 함수.
                conn.escape_string(sql_statement)
                # 변경사항을 데이터베이스에 반영.
                conn.commit()
                # CSV 파일의 각 행 인덱스가 10의 배수이면 진행 상황 출력.
                if idx%10 == 0:
                    print("진행중 ===========================" + str(idx))

if __name__ == '__main__':
    insert_data()