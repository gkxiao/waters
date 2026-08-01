#!/usr/bin/env python3
"""
将 GIST 水合位点数据 (CSV) 转换为 Schrödinger WaterMap 风格 MAE 文件

输入 CSV 列（必需）: x, y, z, dG, dH, -TdS, occupancy
可选列: site (位点名，缺省自动生成 HS1, HS2, ...)
        potential_energy (若提供则直接使用；否则按 dH + bulk 计算)

用法:
  python3 csv2watermap_mae.py input.csv -o output.mae --bulk -19.67

字段换算:
  potential_energy = CSV 中该列的值（若有），否则 = dH + bulk_energy
  entropy          = -TdS                    (与 WaterMap 一致, 冗余字段)
  density          = occupancy
"""

import argparse
import csv
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='CSV -> WaterMap 风格 MAE 转换')
    parser.add_argument('input', help='输入 CSV 文件')
    parser.add_argument('-o', '--output', default='output.mae', help='输出 MAE 文件 (默认 output.mae)')
    parser.add_argument('--bulk', type=float, default=-19.67,
                        help='体相水单分子能量 kcal/mol (默认 -19.67, TIP3P)，仅当 CSV 无 potential_energy 列时使用')
    parser.add_argument('--title', default='gist_watermap', help='MAE 条目名 (默认 gist_watermap)')
    return parser.parse_args()


def read_sites(csv_path):
    """读取 CSV，返回位点字典列表"""
    sites = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            site = {
                'name': row.get('site', '').strip() or f'HS{i + 1}',
                'x': float(row['x']),
                'y': float(row['y']),
                'z': float(row['z']),
                'dG': float(row['dG']),
                'dH': float(row['dH']),
                'mTdS': float(row['-TdS']),
                'occ': float(row['occupancy']),
                'pe': float(row['potential_energy']) if row.get('potential_energy', '').strip() else None,
            }
            sites.append(site)
    return sites


def write_mae(sites, out_path, title, bulk):
    """生成 WaterMap 风格 MAE 文件"""
    lines = []
    n = len(sites)

    # ---- 文件头 ----
    lines.append('{ ')
    lines.append(' s_m_m2io_version')
    lines.append(' :::')
    lines.append(' 2.0.0 ')
    lines.append('} ')
    lines.append('')
    lines.append('f_m_ct { ')
    lines.append(' s_m_title')
    lines.append(' s_m_entry_id')
    lines.append(' s_m_entry_name')
    lines.append(' s_watermap_type')
    lines.append(' s_m_Source_File')
    lines.append(' i_m_Source_File_Index')
    lines.append(' s_m_Source_Path')
    lines.append(' s_m_subgroup_title')
    lines.append(' s_m_subgroupid')
    lines.append(' b_m_subgroup_collapsed')
    lines.append(' i_m_ct_format')
    lines.append(' :::')
    lines.append(f' {title} ')
    lines.append('  1 ')
    lines.append(f'  {title}_wm.1 ')
    lines.append('  watermap ')
    lines.append(f'  {out_path.rsplit("/", 1)[-1]} ')
    lines.append('  1')
    lines.append('  ./ ')
    lines.append(f'  {title} ')
    lines.append(f'  {title} ')
    lines.append('  0')
    lines.append('  2')
    lines.append(f' m_atom[{n}] {{ ')
    lines.append('  # First column is atom index #')
    lines.append('  i_m_mmod_type')
    lines.append('  r_m_x_coord')
    lines.append('  r_m_y_coord')
    lines.append('  r_m_z_coord')
    lines.append('  i_m_color')
    lines.append('  i_m_atomic_number')
    lines.append('  s_m_color_rgb')
    lines.append('  s_m_atom_name')
    lines.append('  r_watermap_-TdeltaS')
    lines.append('  r_watermap_deltaG')
    lines.append('  r_watermap_deltaH')
    lines.append('  r_watermap_density')
    lines.append('  r_watermap_entropy')
    lines.append('  r_watermap_potential_energy')
    lines.append('  i_watermap_site_num')
    lines.append('  :::')

    # ---- 数据行 ----
    for i, s in enumerate(sites):
        pe = s['pe'] if s['pe'] is not None else s['dH'] + bulk
        ent = s['mTdS']              # entropy 与 -TdS 相同
        lines.append(
            f"  {i + 1} 61 {s['x']:.6f} {s['y']:.6f} {s['z']:.6f} "
            f"10 -2 1EE11E {s['name']} "
            f"{s['mTdS']:.6f} {s['dG']:.6f} {s['dH']:.6f} "
            f"{s['occ']:.6f} {ent:.6f} {pe:.6f} {i + 1}"
        )

    # ---- 文件尾 ----
    lines.append('  :::')
    lines.append(' } ')
    lines.append('} ')
    lines.append('')

    with open(out_path, 'w') as f:
        f.write('\n'.join(lines))

    pe_src = 'CSV 提供' if sites[0]['pe'] is not None else f'dH + bulk = dH + ({bulk:.2f})'
    pe0 = sites[0]['pe'] if sites[0]['pe'] is not None else sites[0]['dH'] + bulk
    print(f'✅ 已写入 {out_path}  ({n} 个水合位点)')
    print(f'   potential_energy 来源: {pe_src}')
    print(f'   示例首行: {sites[0]["name"]} dG={sites[0]["dG"]:.2f} '
          f'dH={sites[0]["dH"]:.2f} -TdS={sites[0]["mTdS"]:.2f} '
          f'PE={pe0:.2f}')


def main():
    args = parse_args()
    sites = read_sites(args.input)
    if not sites:
        print('❌ CSV 无数据行')
        sys.exit(1)
    write_mae(sites, args.output, args.title, args.bulk)


if __name__ == '__main__':
    main()
