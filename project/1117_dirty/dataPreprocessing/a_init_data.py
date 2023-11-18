# 우리가 최종적으로 분류한 지역 리스트 -> 테이블을 생성할 때, 등으로 쓰일 것임.
loc_code_list=['USA','NAM','KOR','SAM','JPN','CHN','RSI','EEU','WEU','AUS','AFR','SAF','ASIA']

# 국가들을 대륙으로 . 빈 곳은 나머지 국가를 포함할 곳.
C_L_dict={'Africa':{'SAF':['South Africa'],'AFR':[]},
          'Asia':{'KOR':['South Korea'],'JPN':['Japan'],
                  'CHN':['China'],
                  'ASIA':[]},
          'Europe':{'RSI':['Russia'],
                    'WEU':['Andorra','Austria','Belgium','England',
                           'France','Guernsey','Iceland','Ireland','Isle of Man',
                           'Italy','Jersey','Luxembourg','Netherlands','Poland','Portugal',
                           'Scotland','Spain','Sweden','United Kingdom','Wales'],
                    'EEU':[]},
          'North America':{'USA':['United States'],'NAM':[]},
          'Oceania':{'AUS':[]},
          'South America':{'SAM':[]}}