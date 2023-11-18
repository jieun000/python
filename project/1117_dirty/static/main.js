// $(document).ready(function(){} 과 같음. 문서가 준비되면 실행되는 함수
$(function(){
  // area5(한국 차트 박스): 연 채로 시작
  $("#area5Box").toggle();

  // 버튼 부분
  var buttonIndex = null;
  var chk = [true, false, false, false]; // chk 배열을 전역 범위에서 정의

  // left_side_btn의 각 버튼에 대해 이벤트 설정
  $("#left_side_btn button").each(function (idx, data) {
    $(this).click(function () {
      // 클릭된 버튼의 인덱스 가져오기
      buttonIndex = $(this).index(); 
      // 클릭한 버튼에 'active' 클래스를 토글(누르면 추가되고, 다시누르면 제거됨)
      $(this).toggleClass("active"); 
      // 버튼에 따른 동작 분기
      switch (buttonIndex) {
        case 0:
          console.log("확진자 버튼이 눌렸어요");
          break;
        case 1:
          console.log("사망자 버튼이 눌렸어요");
          break;
        case 2:
          console.log("접종자 버튼이 눌렸어요");
          break;
        case 3:
          console.log("총 인구수 버튼이 눌렸어요");
          break;
      } // switch case
      data_call(); // 데이터 호출 함수 실행
      chk[buttonIndex] = !chk[buttonIndex]; // 해당 인덱스의 버튼의 상태 업데이트(true와 false 교체)
      console.log("chk:" + chk); // chk 배열 출력
    });
  });
  
  // 슬라이드, 월별 부분
  var months = [
    "2020년 1월","2020년 2월","2020년 3월","2020년 4월","2020년 5월","2020년 6월","2020년 7월","2020년 8월","2020년 9월","2020년 10월","2020년 11월","2020년 12월",
    "2021년 1월","2021년 2월","2021년 3월","2021년 4월","2021년 5월","2021년 6월","2021년 7월","2021년 8월","2021년 9월","2021년 10월","2021년 11월 , 오미크론 발생","2021년 12월",
    "2022년 1월","2022년 2월","2022년 3월","2022년 4월","2022년 5월","2022년 6월","2022년 7월","2022년 8월","2022년 9월","2022년 10월","2022년 11월","2022년 12월",
    "2023년 1월","2023년 2월","2023년 3월","2023년 4월","2023년 5월","2023년 6월","2023년 7월","2023년 8월","2023년 9월","2023년 10월","2023년 11월",
  ];
  
  // 초기 선택된 월과 인덱스 설정
  var selectedMonthIndex = 21;  // 21 = 2021년 11월
  var selectedMonth = months[selectedMonthIndex]; // 21 = 2021년 11월
  $("#month-display").text(selectedMonth); // id가 month-display곳의 텍스트를 2021년 11월로 변경

  // 슬라이드 바의 값이 변경되었을 때 이벤트
  $("#lever").change(function () {
    selectedMonthIndex = $(this).val(); // 선택된 월의 인덱스 가져오기
    selectedMonth = months[selectedMonthIndex]; // 선택된 월 가져오기
    data_call(); // 데이터 호출 함수 실행

    var str = "";
    // 특정 월에 오미크론 발생이라는 문자열이 포함된 경우
    if (selectedMonth === "2021년 11월 , 오미크론 발생") {
        var array1_1 = selectedMonth.split(","); // 쉼표를 기준으로 문자열 분할
        for (var i in array1_1) {
            // 두 번째 문자열(오미크론 발생)이면 빨간색으로 스타일 적용
            if (i == 1) {
                str += "<span style='color:red;'>" + array1_1[i] + "</span><br>";
            } else {
                str += "<span>" + array1_1[i] + "</span><br>";
            }
        }
        console.log(str); // 콘솔창에 문자열 출력
        $("#month-display").html(str); // 해당 문자열을 HTML에 적용
    } else {
        $("#month-display").text(selectedMonth); // 특정 월이 아닌 경우에는 그냥 텍스트 설정
    }
    console.log("슬라이더 값 변경: " + selectedMonth);
  });

  data_call(); // 초기에 데이터 호출 함수 실행

  var chartInstances = [];
  function make_chart(myChart, labels, label, data, chartIndex) {
    const ctx = document.getElementById(myChart).getContext("2d");
    console.log("차트 생성 코드 실행됨" + ctx);
    console.log("Label:", label);
    console.log("Labels:", labels);
    console.log("Data:", data);
    $("#" + myChart).css({
      "background-color": "white",
      "border-radius": "5%",
    });
    data = {
      labels: labels,
      datasets: chked_data(
        [
          {
            label: label,
            data: chked_data(
              chk[3]
                ? [data[0] / data[3], data[1] / data[3], data[2] / data[3]]
                : data.slice(0, 3),
              chk.slice(0, 3)
            ),
            backgroundColor: [
              "rgba(0, 0, 255,0.5 )",
              "rgba(255, 0, 0,0.5)",
              "rgba(0, 128, 0,0.5)"
            ],
            borderColor: "rgba(0, 0, 0, 1)",
            borderWidth: 1,
          },
        ],
        chk.slice(0, 3)
      ),
    };
    options = {
      scales: {
        x: {
          display: true
        },
        y: {
          display: true,
          type: "logarithmic"
        },
      },
      plugins: {
        title: {
          display: true,
          text: label,
          font: {
            size: 18
          }
        },
        legend: {
          display: false // 레이블 박스 표시 비활성화
        },
      },
    };
    var matchingChart = chartInstances.find(function (chart) {
      return chart.canvas.id === myChart;
    });
    if (matchingChart == undefined) {
      newChart = new Chart(ctx, {
        type: "bar",
        data: data,
        options: options
      });
      chartInstances.push(newChart);
    } else {
      chartInstances[chartIndex].data = data;
      chartInstances[chartIndex].update();
    }
  }
  // 체크박스 상태에 따라 데이터를 필터링하는 함수
  function chked_data(data, chk) {
    // console.log("chk array:", chk);
    // console.log("data array:", data);

    // chk 배열의 각 요소에 따라 데이터를 필터링합니다.
    const filter_data = data.filter((_, i) => chk[i]);
    console.log(filter_data);
    return filter_data;
  }
  
  function data_call() {
    $.ajax({
      type: "get", // 타입 (get, post, put 등등)
      url: "/ajax", // 요청할 서버 url    async : true, // 비동기화 여부 (default : true)
      data: { month: selectedMonthIndex },
      dataType: "json",
      success: function (data) {
        console.log("요청 성공", data);
        const labels = chked_data(
          ["확진자", "사망자", "접종자"],
          chk.slice(0, 3)
        );

        const SAF = chked_data(Object.values(data["SAF"]), chk);
        const AFR = chked_data(Object.values(data["AFR"]), chk);
        const ASIA = chked_data(Object.values(data["ASIA"]), chk);
        const CHN = chked_data(Object.values(data["CHN"]), chk);
        const KOR = chked_data(Object.values(data["KOR"]), chk);
        const AUS = chked_data(Object.values(data["AUS"]), chk);
        const JPN = chked_data(Object.values(data["JPN"]), chk);
        const RSI = chked_data(Object.values(data["RSI"]), chk);
        const EEU = chked_data(Object.values(data["EEU"]), chk);
        const WEU = chked_data(Object.values(data["WEU"]), chk);
        const NAM = chked_data(Object.values(data["NAM"]), chk);
        const USA = chked_data(Object.values(data["USA"]), chk);
        const SAM = chked_data(Object.values(data["SAM"]), chk);

        const loc_name_list = ["남아프리카공화국","아프리카","아시아","중국","한국","오세아니아","일본","러시아","동유럽","서유럽","북아메리카","미국","남아메리카"];
        const loc_data_list = [SAF,AFR,ASIA,CHN,KOR,AUS,JPN,RSI,EEU,WEU,NAM,USA,SAM];
        const chart_id_list = [
          "area1_chart","area2_chart","area3_chart","area4_chart","area5_chart","area6_chart","area7_chart",
          "area8_chart","area9_chart","area10_chart","area11_chart","area12_chart","area13_chart",
        ];

        for (let i = 0; i < loc_data_list.length; i++) {
          const chart_name = chart_id_list[i];
          const loc_code = loc_name_list[i];
          const loc_data = loc_data_list[i];

          make_chart(chart_name, labels, loc_code, loc_data, i);
        }
      }, //success callback
      error: function (error) {
        console.log("에러 발생", error);
      },
    }); //ajax
  }
  
  // area 요소 클릭 이벤트 설정
  $("area").click(function () {
    console.log("클릭 이벤트 발생");
    console.log("selectedMonthIndex 값:", selectedMonthIndex); // 선택된 월의 인덱스 출력
    var areaId = $(this).attr("id"); // 클릭된 area 요소의 id 속성 값 가져오기
    var $areaBox = $("#" + areaId + "Box"); // 해당 area에 대응하는 areaBox 선택

    $areaBox.toggle(); // areaBox의 보이기/숨기기 토글
  });

  // areaBox 요소 클릭 이벤트 설정
  $(".areaBox").click(function () {
    $(this).hide(); // .areaBox 숨기기
  });

  // maphilight 플러그인 초기 설정
  $.fn.maphilight.defaults = {
    fill: true, // 채우기 여부
    fillColor: 'CCCCCC', // 채우기 색상
    fillOpacity: 0.5, // 채우기 투명도
    stroke: true, // 테두리 여부
    strokeColor: 'FFFFFF', // 테두리 색상
    strokeOpacity: 1, // 테두리 투명도
    strokeWidth: 1 // 테두리 너비
  };

  $('img[usemap]').maphilight(); // 이미지에 maphilight 플러그인 적용


  // areaId에 해당하는 지역의 내용을 반환하는 함수
  function getAreaContent(areaId) {
    // areaId와 해당 지역 내용을 매핑한 객체
    var areaContents = {
      'area1': '남아공','area2': '아프리카','area3': '아시아','area4': '중국','area5': '한국','area6': '오세아니아',
      'area7': '일본','area8': '러시아','area9': '동유럽','area10': '서유럽','area11': '북아메리카','area12': '미국',
      'area13': '남아메리카'
    };
    return areaContents[areaId];
  }

  // 호버 시 국가 이름: area에 hover 이벤트 설정
  $('area').hover(function (event) {
    // areaId에 대응하는 지역 내용 가져와 변수에 저장
    var areaContent = getAreaContent($(this).attr('id')); 

    // infoBox에 지역 내용을 표시하고 위치 설정
    $('#infoBox').html(areaContent).css({
        top: event.pageY + 'px', // event.pageY: 호버된 곳의 페이지 Y좌표
        left: event.pageX + 'px', // event.pageY: 호버된 곳의 페이지 X좌표
        display: 'block' // display: 'none'이었던 요소가 보이도록
    });
  }, function () {
    $('#infoBox').css('display', 'none'); // 마우스가 벗어날 때 infoBox 다시 안 보이도록
  });

  // body에 infoBox 추가
  $('body').append('<div id="infoBox"></div>');
});