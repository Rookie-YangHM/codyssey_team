import pandas as pd
import os

def load_and_analyze_data():
    """1단계: CSV 파일을 읽고 area 1 데이터 분석 및 구조물 이름 매핑, 통계 리포트 저장"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        area_map = pd.read_csv(os.path.join(current_dir, 'area_map.csv'))
        area_struct = pd.read_csv(os.path.join(current_dir, 'area_struct.csv'))
        area_category = pd.read_csv(os.path.join(current_dir, 'area_category.csv'))
        area_category.columns = area_category.columns.str.strip()

        # 열 이름 자동 인식 (예: id/name 또는 category/struct)
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
        if cat_id_col is None or cat_name_col is None:
            raise ValueError(f"area_category.csv의 열 이름이 올바르지 않습니다. 실제 컬럼: {area_category.columns.tolist()}")

        # area_struct의 구조물 id 컬럼명 자동 인식
        struct_cat_col = None
        for s_cand in ['category', 'id']:
            if s_cand in area_struct.columns:
                struct_cat_col = s_cand
                break
        if struct_cat_col is None:
            raise ValueError('area_struct.csv의 구조물 id 열 이름이 올바르지 않습니다.')

        # 구조물 ID를 이름으로 변환
        category_dict = dict(zip(area_category[cat_id_col], area_category[cat_name_col]))
        area_struct['structure_name'] = area_struct[struct_cat_col].map(category_dict)

        # 데이터 병합 및 정렬
        merged_data = pd.merge(area_struct, area_map, on=['x', 'y'])
        merged_data = merged_data.sort_values('area')

        # area 1 데이터만 필터링
        area1_data = merged_data[merged_data['area'] == 1].copy()

        # 구조물 종류별 요약 통계
        structure_summary = area1_data['structure_name'].value_counts()

        # 리포트 파일로 저장
        report_path = os.path.join(current_dir, 'report_01.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('[구조물 종류별 요약 통계]\n')
            f.write(str(structure_summary))
            f.write('\n')

        return area1_data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    data = load_and_analyze_data()
    if data is None:
        print('프로그램 실행 중 오류가 발생했습니다.')