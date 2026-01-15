import json
from mendeleev import element

def generate_and_save_data():
    mass_dict = {}
    
    print("正在从 mendeleev 库获取数据...")
    
    # 遍历原子序数 1 到 118
    for z in range(1, 119):
        try:
            el = element(z)
            symbol = el.symbol
            mass = el.mass
            
            # 数据处理逻辑：确保获取到一个有效的浮点数
            valid_mass = None
            
            if mass is not None:
                # 检查是否为区间
                if hasattr(mass, '__iter__') and not isinstance(mass, str):
                    valid_mass = float(mass[0]) if len(mass) > 0 else float(el.mass_number)
                else:
                    valid_mass = float(mass)
            else:
                # 回退到 mass_number
                if el.mass_number is not None:
                    valid_mass = float(el.mass_number)
                else:
                    valid_mass = 0.0
            
            # 存入字典
            # 注意：这里我们直接存 float 类型，方便后续计算
            # 没必要存保留小数位的字符串，那样在使用时还需要再转回 float
            mass_dict[symbol] = valid_mass
            
        except Exception as e:
            print(f"Error processing element Z={z}: {e}")
            continue

    # 将字典写入 JSON 文件
    # ensure_ascii=False 保证非英文字符（虽然元素符号都是英文，但这是好习惯）能正常显示
    # indent=4 让生成的文件具有良好的缩进格式，方便人类阅读
    filename = '01_element_atomic-masses.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mass_dict, f, ensure_ascii=False, indent=4)
        
    print(f"数据已成功保存到 {filename}")

if __name__ == "__main__":
    generate_and_save_data()