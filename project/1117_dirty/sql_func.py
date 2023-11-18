import mysql.connector # MySQL 데이터베이스와 통신하기 위한 공식 MySQL 드라이버, MySQL 데이터베이스에 연결하고 쿼리를 실행. 

# MySQL 데이터베이스에서 데이터를 읽어와서 date_loc_data_dict에 저장하는 함수
def from_sql(date_loc_data_dict, loc_code_list): # (빈 객체, 지역 리스트)
    # 각 지역 코드에 대해 반복  
    for loc_code in loc_code_list:
        # MySQL 연결 정보 설정
        mysql_config = {
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'database': 'c'
        }
        # MySQL 데이터베이스에 연결.
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        # 반복중 현재의 지역 코드에 해당하는 테이블에서 모든 데이터를 가져오는 SQL 쿼리 실행.
        cursor.execute(f"select * from %s_tbl"%(loc_code))
        # 현재 쿼리의 결과 집합에서 모든 행을 가져와 리스트로 반환.
        data_list = cursor.fetchall()
        # data_list의 열들을 돌리며 반복할 것임.
        for date_day, loc_code, total_cases, total_deaths, people_vaccinated, population in data_list:
            # date_day 키에 해당하는 값을 가져와 빈 객체에 저장하는데, 만약 해당 키가 존재하지 않으면 빈 딕셔너리 {}로 기본값을 설정.
            date_loc_data_dict[date_day] = date_loc_data_dict.get(date_day, {})
            # 위 객체에서 loc_code 키에 해당하는 값을 가져오는데, 만약 해당 키가 존재하지 않으면 빈 딕셔너리 {}로 기본값을 설정. 
            date_loc_data_dict[date_day][loc_code] = date_loc_data_dict[date_day].get(loc_code, {})
            # 날짜와 지역을 기준으로 업데이트. 
            date_loc_data_dict[date_day][loc_code].update({
                'total_cases': total_cases,
                'total_deaths': total_deaths,
                'people_vaccinated': people_vaccinated,
                'population': population
            })