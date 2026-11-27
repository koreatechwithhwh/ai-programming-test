import csv


def read_scores(path):
    """Read name/score CSV data as (name, float) tuples."""
    kept = []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return kept

        if "name" not in header or "score" not in header:
            raise ValueError("필수 열이 없습니다")

        name_index = header.index("name")
        score_index = header.index("score")

        for row in reader:
            if not row:
                continue
            if name_index >= len(row) or score_index >= len(row):
                raise ValueError("열의 값이 불완전합니다")

            name = row[name_index].strip()
            raw_score = row[score_index].strip()
            if not name or not raw_score:
                raise ValueError("이름 또는 점수가 비어 있습니다")

            try:
                score = float(raw_score)
            except ValueError:
                raise ValueError("점수가 숫자가 아닙니다") from None

            kept.append((name, score))

    return kept
