import pytest

from ai_B import read_scores


def _csv_file(tmp_path, contents, *, encoding="utf-8"):
	path = tmp_path / "scores.csv"
	path.write_text(contents, encoding=encoding)
	return path


def test_reads_csv_as_name_score_tuples(tmp_path):
	path = _csv_file(tmp_path, "name,score\nAlice,95\nBob,82.5\n")

	assert read_scores(path) == [("Alice", 95.0), ("Bob", 82.5)]


def test_reads_utf8_bom(tmp_path):
	path = _csv_file(
		tmp_path, "name,score\nAlice,90\n", encoding="utf-8-sig"
	)

	assert read_scores(path) == [("Alice", 90.0)]


def test_header_only_csv_returns_empty_list(tmp_path):
	path = _csv_file(tmp_path, "name,score\n")

	assert read_scores(path) == []


def test_missing_file_raises_file_not_found_error(tmp_path):
	with pytest.raises(FileNotFoundError):
		read_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize("header", ["name\n", "score\n", "student,grade\n"])
def test_missing_header_column_raises_value_error(tmp_path, header):
	path = _csv_file(tmp_path, header)

	with pytest.raises(ValueError):
		read_scores(path)


@pytest.mark.parametrize("row", ["Alice\n", ",95\n", "Alice,\n", ",\n"])
def test_incomplete_or_empty_row_raises_value_error(tmp_path, row):
	path = _csv_file(tmp_path, "name,score\n" + row)

	with pytest.raises(ValueError):
		read_scores(path)


def test_non_numeric_score_raises_value_error(tmp_path):
	path = _csv_file(tmp_path, "name,score\nAlice,excellent\n")

	with pytest.raises(ValueError):
		read_scores(path)
