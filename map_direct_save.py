import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

def find_shortest_path(data, start_point, end_point):
    """BFS를 사용한 최단 경로 탐색"""
    rows = max(data['x'])
    cols = max(data['y'])
    
    # 건설 현장 위치 저장
    construction_sites = set()
    for _, row in data[data['ConstructionSite'] == 1].iterrows():
        construction_sites.add((row['x'], row['y']))
    
    # BFS 구현
    queue = deque([(start_point, [start_point])])
    visited = {start_point}
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end_point:
            return path
            
        # 상하좌우 이동
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            
            # 맵 범위 내에 있고, 건설 현장이 아니며, 방문하지 않은 경우
            if (1 <= new_x <= rows and 1 <= new_y <= cols and 
                (new_x, new_y) not in construction_sites and 
                (new_x, new_y) not in visited):
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))
    
    return None

def save_path_and_visualize(data, path):
    """경로를 저장하고 시각화"""
    # 경로를 CSV로 저장
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df.to_csv('home_to_cafe.csv', index=False)
    
    # 지도 시각화 (map_draw.py의 코드를 재사용하되 경로 추가)
    plt.figure(figsize=(12, 12))
    plt.grid(True)
    plt.gca().invert_yaxis()
    
    # 구조물 시각화
    # ... (map_draw.py의 시각화 코드)
    
    # 경로 시각화
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    plt.plot(path_x, path_y, 'r-', linewidth=2, label='Shortest Path')
    
    plt.legend()
    plt.savefig('map_final.png')
    plt.close()

if __name__ == '__main__':
    # 데이터 로드
    data = pd.read_csv('proc01/99/area_struct.csv')  # 실제로는 1단계의 결과를 사용
    
    # 시작점(내 집)과 도착점(반달곰 커피) 찾기
    my_home = data[data['structure_name'] == 'MyHome'].iloc[0]
    coffee_shop = data[data['structure_name'] == 'BandalgomCoffee'].iloc[0]
    
    start_point = (my_home['x'], my_home['y'])
    end_point = (coffee_shop['x'], coffee_shop['y'])
    
    # 최단 경로 찾기
    path = find_shortest_path(data, start_point, end_point)
    
    if path:
        save_path_and_visualize(data, path)
    else:
        print('No path found!')