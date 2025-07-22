import pandas as pd
import os

def analyze_and_prepare_data(output_dir='output', csv_dir='csv'):
    """
    세 개의 CSV 파일을 로드하여 데이터를 분석, 병합, 정제하고 요약 리포트를 생성합니다.

    Args:
        output_dir (str): 결과물을 저장할 디렉토리.
        csv_dir (str): CSV 파일이 위치한 디렉토리.

    Returns:
        pd.DataFrame: 병합되고 정제된 데이터프레임.
    """
    try:
        area_map = pd.read_csv(os.path.join(csv_dir, 'area_map.csv'), skipinitialspace=True)
        area_struct = pd.read_csv(os.path.join(csv_dir, 'area_struct.csv'), skipinitialspace=True)
        area_category = pd.read_csv(os.path.join(csv_dir, 'area_category.csv'), skipinitialspace=True)
    except FileNotFoundError as e:
        print(f"오류: {e}. '{csv_dir}' 폴더에 필요한 파일이 있는지 확인하세요.")
        return None

    for df in [area_map, area_struct, area_category]:
        df.columns = df.columns.str.strip()

    category_dict = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_dict)

    merged_df = pd.merge(area_struct, area_map, on=['x', 'y'], how='left')
    merged_df['ConstructionSite'] = merged_df['ConstructionSite'].fillna(0).astype(int)
    merged_df = merged_df.sort_values(by='area').reset_index(drop=True)

    valid_structs = merged_df.dropna(subset=['struct_name'])
    report_lines = []
    for area_id, group in valid_structs.groupby('area'):
        report_lines.append(f"Area {area_id} 요약:")
        struct_counts = group['struct_name'].value_counts()
        for name, count in struct_counts.items():
            report_lines.append(f"  - {name}: {count}개")
        construction_count = group[group['ConstructionSite'] == 1].shape[0]
        if construction_count > 0:
            report_lines.append(f"  - 건설 현장: {construction_count}개")
        report_lines.append("")

    report_content = "\n".join(report_lines)
    print("\n--- 구조물 종류별 요약 통계 ---")
    print(report_content)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    report_path = os.path.join(output_dir, 'report_01a.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"\n요약 리포트가 '{report_path}'에 저장되었습니다.")
    
    merged_data_path = os.path.join(output_dir, 'area_merged.csv')
    merged_df.to_csv(merged_data_path, index=False, encoding='utf-8')
    print(f"병합된 데이터가 '{merged_data_path}'에 저장되었습니다.")

    return merged_df


def main():
    """
    메인 실행 함수
    """
    analyze_and_prepare_data()


if __name__ == '__main__':
    main()