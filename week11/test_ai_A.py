import pytest

from load_scores import load_scores


def test_load_scores_keeps_valid_rows_and_ignores_header_and_blank_lines(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"이름,점수\nAlice,85\n\n Bob , 92 \n",
		encoding="utf-8-sig",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Alice", 85), ("Bob", 92)]
	assert skipped == []


@pytest.mark.parametrize("score", [0, 100])
def test_load_scores_accepts_boundary_scores(tmp_path, score):
	path = tmp_path / "scores.csv"
	path.write_text(f"name,score\nStudent,{score}\n", encoding="utf-8")

	assert load_scores(path) == ([("Student", score)], [])


@pytest.mark.parametrize(
	("row", "reason"),
	[
		("OnlyOneColumn", "열 개수가 2가 아님"),
		("A,1,extra", "열 개수가 2가 아님"),
		(",50", "이름이 비어 있음"),
		("A,", "점수가 비어 있음"),
		("A,1.5", "점수가 정수가 아님"),
		("A,-1", "점수가 0~100 밖"),
		("A,101", "점수가 0~100 밖"),
	],
)
def test_load_scores_records_invalid_rows(tmp_path, row, reason):
	path = tmp_path / "scores.csv"
	path.write_text(f"name,score\n{row}\n", encoding="utf-8")

	kept, skipped = load_scores(path)

	assert kept == []
	assert skipped == [(2, row, reason)]


def test_load_scores_raises_for_missing_file(tmp_path):
	with pytest.raises(FileNotFoundError):
		load_scores(tmp_path / "missing.csv")
