"""
간단한 지도 시각화 스크립트
직접 draw_map 함수를 호출하여 area 구역 정보가 포함된 지도를 생성합니다.
"""
import pandas as pd
from map_visualization import draw_map

if __name__ == '__main__':
    try:
        merged_df = pd.read_csv('output/area_merged.csv')
        draw_map(merged_df, show_areas=True, output_filename='map.png')
    except FileNotFoundError:
        print("오류: 'output/area_merged.csv' 파일을 찾을 수 없습니다.")
        print("1단계(caffee_map.py)를 먼저 실행하여 데이터를 생성해주세요.")