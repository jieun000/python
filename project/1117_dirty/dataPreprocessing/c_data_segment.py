import pandas as pd # pandas 라이브러리(데이터 조작과 분석)를 가져와 앞으로 pd라고 부를 것임.
import os # os 라이브러리(운영체제와 상호작용)를 가져옴.
from a_init_data import loc_code_list,C_L_dict # a_init_data 모듈에서 loc_code_list와 C_L_dict를 가져옴.
#중동은 아시아와 아프리카 두 대륙에 포함되어 있어 제외하였다.

# loc_code_list로 columns을 다음과 같이 하는 빈 데이터프레임 객체 생성.
data_dict={i: pd.DataFrame(columns=["date_day", "loc", "total_cases",'total_deaths','total_vaccinations','total_population']) for i in loc_code_list}
# 'owid-covid-data.csv'와 'vaccinations.csv' 파일에서 필요한 열을 선택하여 데이터프레임을 생성
data1 = pd.read_csv('owid-covid-data.csv')[['date', 'continent', 'location', 'new_cases', 'new_deaths', 'population']]
data2= pd.read_csv('vaccinations.csv')[['date', 'location', 'daily_vaccinations']]

# 대륙와 국가를 사용해 분류하는 함수(국가별 분류, 대륙, 국가, 달 별로 분류한 객체, 분류해 넣을 객체)
def segment_by_continent_and_location(group, continent, location, data_dict, C_L_dict):
    """
        데이터 분류의 효율성을 높이기 위해 대륙 별로 분류된 데이터에서
        우리가 원하는 지역별 데이터를 분류하여
        data_dict에 담는다.
    """
    # 분류해서 담을 객체의 키와 값을 각각 continents와 location_dict라는 변수에 저장
    continents, location_dict = C_L_dict.keys(),C_L_dict.values()
    # 분류해서 담을 객체의 키들을 반복.
    for continent_ in continents:
        # 대륙이 같지 않으면 계속. (같은 대륙이면 아무 일도 안 벌어짐)
        if continent != continent_:
            continue
        # C_L_dict에서의 반복중 현재 키(대륙) 내의 국가 키와 값을 각각 name, loction_list 변수에 저장
        for name, loction_list in C_L_dict[continent_].items():
            # 국가값이 있으면 반복해서 나오게.
            if loction_list:
                if location in loction_list:
                    # 해당 국가 키에 대한 데이터프레임이 이미 존재하면 그 데이터프레임에 group(대륙별로 국가별로 분류한 것)을 수평으로 합치고, 
                    # 존재하지 않으면 새로운 데이터프레임을 생성하고 거기에 group을 추가하는 동작
                    data_dict[name] = pd.concat([data_dict.get(name, pd.DataFrame({})), group])
            # 국가값이 없으면 그냥 위의 데이터 프레임 합치기 실행
            else:
                data_dict[name] = pd.concat([data_dict.get(name, pd.DataFrame({})), group])


# 데이터를 분할하여 CSV 파일로 저장하는 함수
def segment_data_to_csv():
    # 두 개의 데이터프레임을 'date'와 'location' 열을 기준으로 외부 조인한 변수
    data = pd.merge(data1, data2, on=['date', 'location'], how='outer')

    # 'date' 열을 기준으로 월별로 데이터를 그룹화
        # pd.to_datetime(): datetime(날짜와 시간) 객체로 변환.
        # dt.: datetime 구성 요소(예: 연, 월, 일 등)에 액세스.
        # to_period('M'): 월별로 그룹화.
    data['month'] = pd.to_datetime(data['date']).dt.to_period('M')

    # month 변수에는 그룹의 기준이 되는 월의 값이 할당, month_group 변수에는 해당 월에 해당하는 데이터프레임이 할당.
    for month, month_group in data.groupby('month'):
        # 각 월별로 데이터를 저장할 빈 데이터프레임 생성
        data_segment_by_month_dict = {i: pd.DataFrame({}) for i in loc_code_list}
        # 대륙과 국가에 따라 데이터를 분할.
        for continent, continent_group in month_group.groupby('continent'):
            for location, location_group in continent_group.groupby('location'):
                # 위 함수에 (국가별 그룹, 대륙, 국가, 분류한 데이터, 각 월별로 데이터를 저장할 빈 데이터프레임, 분류해서 넣을 객체)을 보냄
                segment_by_continent_and_location(location_group,continent,location,data_segment_by_month_dict,C_L_dict)

        # 월별로 분류한 키와 값을 각각의 변수에 저장. (국가 코드, 그 코드에 해당하는 데이터프레임)
        for loc_code, loc_df in data_segment_by_month_dict.items():
            # 시도
            try:
                # [data_dict[loc_code]가 반복적으로 합쳐되며 누적될 것임.
                data_dict[loc_code] = pd.concat([data_dict[loc_code],
                                            # data_dict[loc_code]와 생성한 데이터프레임({})을 합침
                                           pd.DataFrame({'date_day': [month],
                                                         'loc': [loc_code],
                                                         'total_cases': [loc_df['new_cases'].sum()], # 지금 월별로 합쳐지는 중
                                                         'total_deaths': [loc_df['new_deaths'].sum()],
                                                         'total_vaccinations': [loc_df['daily_vaccinations'].sum()],
                                                        # .unique(): 해당 열에서 중복된 값을 제거하고 고유한 값만을 반환. 
                                                         'total_population':[loc_df['population'].unique().sum()]})]) # 고유값만 합쳐지는 중
            except: # 에러가 있을 경우 해당 달과 지역 코드를 출력함.
                print(f'ERORR: month(%s)  loc_code(%s)'%(month,loc_code),)

    # 각 지역 코드에 대한 결과를 CSV 파일로 저장합니다.
    for loc_code, loc_df in data_dict.items():
        # ../data_segment_by_loc_code/{지역코드}.csv로 파일 위치와 이름을 변수에 저장
        filename = f'../data_segment_by_loc_code/{loc_code}.csv'
        # to_csv(파일이름, 인덱스 출력여부)로 엑셀 파일 저장
        data_dict[loc_code].to_csv(filename, index=False)

if __name__ == '__main__':
    try:
        # '../data_segment_by_loc_code' 디렉토리를 생성. 
        os.mkdir('../data_segment_by_loc_code')
    except: # 이미 존재할 경우 예외 처리
        pass # 그냥 넘어가기.
    
    # 데이터를 분할하여 CSV 파일로 저장하는 함수를 호출
    segment_data_to_csv()