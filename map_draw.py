import pandas as pd
import matplotlib.pyplot as plt
import os

def draw_map():
    """2단계: area1 데이터 기반 지도 시각화 및 map.png 저장"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    area_map = pd.read_csv(os.path.join(current_dir, 'area_map.csv'))
    area_struct = pd.read_csv(os.path.join(current_dir, 'area_struct.csv'))
    area_category = pd.read_csv(os.path.join(current_dir, 'area_category.csv'))
    area_category.columns = area_category.columns.str.strip()

    # 열 이름 자동 인식
    cat_id_col = None
    cat_name_col = None
    for id_cand in ['category', 'id']:
        if id_cand in area_category.columns:
            cat_id_col = id_cand
            break
    for name_cand in ['struct', 'name']:
        if name_cand in area_category.columns:
            cat_name_col = name_cand
            break
    struct_cat_col = None
    for s_cand in ['category', 'id']:
        if s_cand in area_struct.columns:
            struct_cat_col = s_cand
            break
    # 구조물 이름 매핑
    category_dict = dict(zip(area_category[cat_id_col], area_category[cat_name_col]))
    area_struct['structure_name'] = area_struct[struct_cat_col].map(category_dict)
    merged_data = pd.merge(area_struct, area_map, on=['x', 'y'])
    merged_data = merged_data.sort_values('area')
    area1_data = merged_data[merged_data['area'] == 1].copy()
    if area1_data.empty:
        print('area1_data가 비어 있습니다. area_map/area_struct/area_category 파일과 area 값 확인 필요.')
        return

    # 좌표 타입 변환
    area1_data['x'] = area1_data['x'].astype(int)
    area1_data['y'] = area1_data['y'].astype(int)

    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    x_max = area1_data['x'].max()
    y_max = area1_data['y'].max()
    plt.xlim(0.5, x_max + 0.5)
    plt.ylim(0.5, y_max + 0.5)
    plt.gca().invert_yaxis()  # (1,1)이 좌상단
    plt.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)

    # 3~6번 조건: 건설 현장 우선, 도형/색상, 겹침 처리, 범례 중복 제거
    # 1) 건설 현장 좌표 집합
    construction_coords = set(
        (int(row['x']), int(row['y']))
        for _, row in area1_data[area1_data['structure_name'] == 'ConstructionSite'].iterrows()
    )
    # 2) 구조물별 좌표 분리(건설 현장 겹침 우선)
    coords = {
        '건설 현장': [],
        '아파트/빌딩': [],
        '반달곰 커피': [],
        '내 집': []
    }
    for _, row in area1_data.iterrows():
        x, y = int(row['x']), int(row['y'])
        name = row['structure_name']
        pos = (x, y)
        if pos in construction_coords:
            coords['건설 현장'].append(pos)
        elif name in ['Apartment', 'Building']:
            coords['아파트/빌딩'].append(pos)
        elif name == 'BandalgomCoffee':
            coords['반달곰 커피'].append(pos)
        elif name == 'MyHome':
            coords['내 집'].append(pos)

    # 3) 시각화(도형/색상/marker)
    if coords['건설 현장']:
        xs, ys = zip(*coords['건설 현장'])
        plt.scatter(xs, ys, marker='s', color='gray', s=300, label='건설 현장', edgecolors='black', linewidths=0.5)
    if coords['아파트/빌딩']:
        xs, ys = zip(*coords['아파트/빌딩'])
        plt.scatter(xs, ys, marker='o', color='saddlebrown', s=200, label='아파트/빌딩', edgecolors='black', linewidths=0.5)
    if coords['반달곰 커피']:
        xs, ys = zip(*coords['반달곰 커피'])
        plt.scatter(xs, ys, marker='s', color='green', s=200, label='반달곰 커피', edgecolors='black', linewidths=0.5)
    if coords['내 집']:
        xs, ys = zip(*coords['내 집'])
        plt.scatter(xs, ys, marker='^', color='green', s=250, label='내 집', edgecolors='black', linewidths=0.5)

    # 4) 범례(중복 제거)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='best')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Area 1 Map')
    plt.tight_layout()
    plt.savefig(os.path.join(current_dir, 'map.png'))
    plt.close()

if __name__ == '__main__':
    draw_map()