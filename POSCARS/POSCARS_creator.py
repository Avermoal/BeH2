#!/usr/bin/env python
"""
Генерация POSCAR-файлов для адсорбции H на Pd(111)
с покрытиями 0.25, 0.50 и 0.75 монослоя.
"""

from ase.build import fcc111, add_adsorbate
from ase.io import write

def create_H_Pd_slab(theta, a=3.89, size=(2,2,4), vacuum=15.0, height=1.0):
    """
    Создаёт структуру Pd(111) с адсорбированным водородом.

    Параметры:
        theta : float
            Покрытие водорода (0.25, 0.50, 0.75).
        a : float
            Параметр решётки Pd в ангстремах.
        size : tuple
            Размеры суперячейки (nx, ny, n_layers).
        vacuum : float
            Вакуумный промежуток в ангстремах.
        height : float
            Высота адсорбата над поверхностью в ангстремах.

    Возвращает:
        ase.Atoms : Готовая структура.
    """
    # 1. Создаём чистую пластину Pd(111)
    slab = fcc111('Pd', size=size, a=a, vacuum=vacuum)

    # 2. Определяем количество атомов H в зависимости от покрытия
    n_surface_atoms = size[0] * size[1]  # для p(2x2) = 4
    n_H = int(theta * n_surface_atoms)

    if n_H not in (1, 2, 3):
        raise ValueError(
            f"Некорректное покрытие {theta} для ячейки {size}. "
            f"Ожидалось 1, 2 или 3 атома H."
        )

    # 3. Добавляем атомы водорода в ГЦК-пустоты (fcc hollow sites)
    # offset = i обеспечивает размещение в разных пустотах без наложения
    for i in range(n_H):
        add_adsorbate(slab, 'H', height=height, position='fcc', offset=i)

    return slab

def main():
    # Параметры системы
    pd_a = 3.89          # параметр решётки Pd, Å
    size = (2, 2, 4)     # p(2x2) supercell, 4 слоя
    vacuum = 15.0        # вакуум, Å
    height = 1.0         # высота H над поверхностью, Å

    # Список требуемых покрытий
    theta_values = [0.25, 0.50, 0.75]

    for theta in theta_values:
        # Генерируем структуру
        slab = create_H_Pd_slab(theta=theta, a=pd_a, size=size,
                                vacuum=vacuum, height=height)

        # Формируем имя файла
        # Заменяем точку на 'p' для избежания проблем в некоторых системах
        theta_str = f"{theta:.2f}".replace('.', 'p')
        filename = f"POSCAR_H_Pd_theta_{theta_str}.vasp"

        # Сохраняем в формате VASP 5 (с элементами)
        write(filename, slab, direct=True, vasp5=True)

if __name__ == '__main__':
    main()
