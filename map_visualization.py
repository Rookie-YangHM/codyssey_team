import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
import pandas as pd

def draw_map(merged_df, path_to_draw=None, output_filename='map.png', show_areas=True):
    """
    데이터프레임과 선택적 경로를 기반으로 지도를 시각화하고 저장합니다.

    Args:
        merged_df (pd.DataFrame): 구조물 정보가 포함된 데이터프레임.
        path_to_draw (list, optional): 지도에 그릴 경로 좌표 리스트. Defaults to None.
        output_filename (str, optional): 저장할 이미지 파일 이름. Defaults to 'map.png'.
        show_areas (bool, optional): 구역 정보를 배경으로 표시할지 여부. Defaults to True.
    """
    x_max = merged_df['x'].max()
    y_max = merged_df['y'].max()

    fig, ax = plt.subplots(figsize=(x_max / 2, y_max / 2))

    ax.set_xticks(range(1, x_max + 2))
    ax.set_yticks(range(1, y_max + 2))
    ax.grid(True, which='both', color='lightgray', linewidth=0.5, zorder=0)
    ax.set_xlim(0.5, x_max + 0.5)
    ax.set_ylim(0.5, y_max + 0.5)
    ax.set_aspect('equal')
    ax.set_title('Area Map Visualization')

    # Area 구역을 배경으로 표시
    if show_areas and 'area' in merged_df.columns:
        area_colors = {
            0: '#e0e0e0',  # 진한 회색 (기본 구역)
            1: '#bbdefb',  # 진한 파랑 (구역 1)
            2: '#ffcc80',  # 진한 주황 (구역 2)
            3: '#c8e6c9'   # 진한 초록 (구역 3)
        }
        
        # Area별로 그룹화하여 효율적으로 처리
        for area_id, area_color in area_colors.items():
            area_data = merged_df[merged_df['area'] == area_id]
            for _, row in area_data.iterrows():
                ax.add_patch(plt.Rectangle(
                    (row['x'] - 0.5, row['y'] - 0.5), 1, 1, 
                    facecolor=area_color, 
                    alpha=0.6, 
                    zorder=1,
                    edgecolor='white',
                    linewidth=0.2
                ))

    for _, row in merged_df.iterrows():
        name = row['struct_name']
        x, y = row['x'], row['y']
        
        if row['ConstructionSite'] == 1:
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', alpha=0.7, zorder=2))
        elif pd.notna(name):
            name = name.strip()
            if name in ['Apartment', 'Building']:
                ax.add_patch(plt.Circle((x, y), 0.4, color='brown', zorder=3))
            elif name == 'BandalgomCoffee':
                ax.add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=4))
            elif name == 'MyHome':
                ax.add_patch(plt.Polygon([[x, y + 0.4], [x - 0.4, y - 0.4], [x + 0.4, y - 0.4]], color='green', zorder=4))

    if path_to_draw:
        path_x, path_y = zip(*path_to_draw)
        ax.plot(path_x, path_y, color='red', linewidth=2, marker='o', markersize=4, zorder=5)
        ax.set_title('Shortest Path from Home to Cafe')

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Apartment/Building', markerfacecolor='brown', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='BandalgomCoffee', markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='^', color='w', label='MyHome', markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='ConstructionSite', markerfacecolor='gray', markersize=10, alpha=0.7)
    ]
    
    # Area 범례 추가
    if show_areas and 'area' in merged_df.columns:
        area_labels = {
            0: 'Area 0 (Default)',
            1: 'Area 1 (Blue Zone)',
            2: 'Area 2 (Orange Zone)', 
            3: 'Area 3 (Green Zone)'
        }
        area_colors = {
            0: '#e0e0e0',
            1: '#bbdefb',
            2: '#ffcc80',
            3: '#c8e6c9'
        }
        
        for area_id in sorted(merged_df['area'].unique()):
            if pd.notna(area_id) and int(area_id) in area_labels:
                area_int = int(area_id)
                legend_elements.append(
                    Line2D([0], [0], marker='s', color='w', 
                          label=area_labels[area_int], 
                          markerfacecolor=area_colors[area_int], 
                          markersize=8, alpha=0.7)
                )
    
    if path_to_draw:
        legend_elements.append(Line2D([0], [0], color='red', lw=2, label='Shortest Path'))
    
    ax.legend(handles=legend_elements, loc='upper right')

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    map_path = os.path.join(output_dir, output_filename)
    plt.savefig(map_path, bbox_inches='tight')
    plt.close()
    
    print(f"지도 이미지가 '{map_path}'에 저장되었습니다.")


if __name__ == '__main__':
    """
    독립 실행 시 area 구역 정보가 포함된 기본 지도를 생성합니다.
    """
    try:
        merged_df = pd.read_csv('output/area_merged.csv')
        draw_map(merged_df, show_areas=True, output_filename='map.png')
    except FileNotFoundError:
        print("오류: 'output/area_merged.csv' 파일을 찾을 수 없습니다.")
        print("1단계(caffee_map.py)를 먼저 실행하여 데이터를 생성해주세요.")