import pytest
from kdtree.kdtree import KDTree, Point

pontos = [
    Point(point=(-43.9, -19.9), name="Restaurante Dijkstra Gourmet", alvara="NÃO", date="2018-01-01", address="Rua A"),
    Point(point=(-43.91, -19.91), name="Buteco do Kruskal", alvara="SIM", date="2019-02-01", address="Rua B"),
    Point(point=(-43.92, -19.92), name="Café P vs NP", alvara="NÃO", date="2020-03-01", address="Rua C"),
    Point(point=(-43.93, -19.93), name="Petiscos do Backtrack", alvara="SIM", date="2021-04-01", address="Rua D"),
    Point(point=(-43.91, -19.89), name="Bubble Beer Bar", alvara="NÃO", date="2022-05-01", address="Rua E"),
    Point(point=(-43.89, -19.91), name="Lanchonete QuickByte", alvara="SIM", date="2023-06-01", address="Rua F")
]

@pytest.fixture
def tree():
    return KDTree(pontos)

def names(resultado):
    return sorted([p.name for p in resultado])

def test_only_one_point(tree):
    region = [(-43.915, -19.915), (-43.91, -19.905)]
    assert names(tree.search(region)) == ["Buteco do Kruskal"]

def test_border_points(tree):
    region = [(-43.91, -19.91), (-43.89, -19.88)]
    assert names(tree.search(region)) == sorted(["Lanchonete QuickByte", "Buteco do Kruskal", "Bubble Beer Bar", "Restaurante Dijkstra Gourmet"])

def test_all_points(tree):
    region = [(-43.94, -19.95), (-43.88, -19.88)]
    assert names(tree.search(region)) == sorted([p.name for p in pontos])

def test_none_point(tree):
    region = [(-44.0, -20.0), (-43.95, -19.96)]
    assert names(tree.search(region)) == []
