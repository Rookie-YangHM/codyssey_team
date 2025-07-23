import pandas as pd
import os
from collections import deque
from map_visualization import draw_map

def find_shortest_path(merged_df):
    """
    BFS 알고리즘을 사용하여 최단 경로를 찾습니다.

    Args:
        merged_df (pd.DataFrame): 구조물 정보가 포함된 데이터프레임.

    Returns:
        list: 최단 경로 좌표 리스트. 경로를 찾지 못한 경우 None.
    """
    try:
        start_node = tuple(merged_df[merged_df['struct_name'] == 'MyHome'][['x', 'y']].iloc[0])
        end_node = tuple(merged_df[merged_df['struct_name'] == 'BandalgomCoffee'][['x', 'y']].iloc[0])
    except IndexError:
        print("오류: 'MyHome' 또는 'BandalgomCoffee' 위치를 찾을 수 없습니다.")
        return None

    obstacles = set(tuple(row) for _, row in merged_df[merged_df['ConstructionSite'] == 1][['x', 'y']].iterrows())
    x_max = merged_df['x'].max()
    y_max = merged_df['y'].max()

    queue = deque([(start_node, [start_node])])
    visited = {start_node}

    while queue:
        (current_x, current_y), path = queue.popleft()

        if (current_x, current_y) == end_node:
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x, next_y = current_x + dx, current_y + dy
            next_node = (next_x, next_y)

            if (1 <= next_x <= x_max and 1 <= next_y <= y_max and
                    next_node not in visited and next_node not in obstacles):
                visited.add(next_node)
                new_path = list(path)
                new_path.append(next_node)
                queue.append((next_node, new_path))
    
    return None

def main():
    """
    메인 실행 함수: 데이터 로드, 최단 경로 탐색, 결과 저장 및 시각화
    """
    try:
        merged_df = pd.read_csv('output/area_merged.csv')
    except FileNotFoundError:
        print("오류: 'output/area_merged.csv' 파일을 찾을 수 없습니다.")
        print("1단계(caffee_map.py)를 먼저 실행하여 데이터를 생성해주세요.")
        return

    path_found = find_shortest_path(merged_df)

    if path_found:
        # 경로 데이터를 CSV로 저장
        path_df = pd.DataFrame(path_found, columns=['x', 'y'])
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        path_csv_path = os.path.join(output_dir, 'home_to_cafe.csv')
        path_df.to_csv(path_csv_path, index=False)
        print(f"최단 경로가 '{path_csv_path}'에 저장되었습니다.")

        # 경로가 포함된 지도 시각화 (area 구역 정보 포함)
        draw_map(merged_df, path_to_draw=path_found, show_areas=True, output_filename='map_final.png')
    else:
        print("경로를 찾을 수 없습니다.")

if __name__ == '__main__':
    main()