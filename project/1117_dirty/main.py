# Flask 모듈에서 필요한 클래스 및 함수들을 임포트합니다. 
from flask import Flask, render_template, request, json
# Flask: Flask 웹 애플리케이션을 생성하기 위한 클래스
# render_template: HTML 템플릿을 렌더링하는 함수
# request: HTTP 요청을 다루는 객체
# json: JSON 데이터를 처리하는 모듈
import pandas as pd
from sql_func import from_sql
from dataPreprocessing.a_init_data import loc_code_list

# Flask 애플리케이션을 생성하고 app 변수에 할당
app = Flask(__name__)

date_loc_data_dict = {}

# 루트 경로에 대한 라우트를 정의. 즉, 홈페이지에 접속했을 때 실행될 함수를 지정
@app.route('/') # 홈페이지에 접속했을 때 실행
def start():
    # 전역 변수 date_loc_data_dict
    global date_loc_data_dict
    # sql_func 모듈의 from_sql함수(전역변수, a_init_data 모듈의 지역 리스트)
    from_sql(date_loc_data_dict, loc_code_list)
    return render_template('main.html') # HTML 템플릿을 불러와서 필요한 데이터를 템플릿에 전달

def to_json2(df,orient='split'):
    df_json = df.to_json(orient=orient, force_ascii=False)
    return json.loads(df_json)

@app.route('/ajax')
def hello():
    global date_loc_data_dict
    month_idx = int(request.args.get('month'))
    print(month_idx)
    date=date_loc_data_dict.keys()
    loc_data_dict_by_date = date_loc_data_dict[list(date)[month_idx]]
    json2_list=[]
    for loc_code in loc_code_list:
        df=pd.DataFrame([loc_data_dict_by_date[loc_code]])
        json2_list.append(to_json2(pd.DataFrame(df)))
    result_df = pd.DataFrame(loc_data_dict_by_date).T
    print(result_df)
    json_result = result_df.to_json(orient='index')
    return json_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
