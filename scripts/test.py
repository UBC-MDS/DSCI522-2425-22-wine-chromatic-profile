from pathlib import Path

p = Path(__file__).parent

print(p)

data_p = p.parent / "data/"

print(p / ".." / "data" / "wind_data.csv")


print(data_p)