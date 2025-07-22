import pandas as pd
from map_visualization import draw_map

def main():
    """
    메인 실행 함수: 데이터 로드 및 지도 시각화
    """
    try:
        merged_df = pd.read_csv('output/area_merged.csv')
    except FileNotFoundError:
        print("오류: 'output/area_merged.csv' 파일을 찾을 수 없습니다.")
        print("1단계(caffee_map.py)를 먼저 실행하여 데이터를 생성해주세요.")
        return

    draw_map(merged_df, output_filename='map.png')

if __name__ == '__main__':
    main()