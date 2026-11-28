import pandas as pd


def 정제(df):
    # 원본을 보존하기 위해 복사본을 만든다.
    결과 = df.copy()
    print("시작        ", len(결과))

    # 점수가 비어 있는 행을 삭제한다.
    결과 = 결과.dropna(subset=["점수"])
    print("빈 칸 제거  ", len(결과))

    # 모든 열의 값이 같은 중복 행을 삭제한다.
    결과 = 결과.drop_duplicates()
    print("중복 제거   ", len(결과))

    # 반과 과목의 앞뒤 공백을 제거한다.
    # 결과["반"] = 결과["반"].str.strip()
    # 결과["과목"] = 결과["과목"].str.strip()

    # 점수가 0 이상 100 이하인 행만 남긴다.
    결과 = 결과[결과["점수"].between(0, 100)]
    print("범위 밖 제거", len(결과))

    return 결과


def 수학만(df):
    결과 = df[df["과목"] == "수학"]
    print("수학 행 수", len(결과))
    return 결과


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


def 과목반별평균(df):
    return df.groupby(["과목", "반"])["점수"].mean()


def 반별통계(df):
    return df.groupby("반").agg(
        개수=("점수", "count"),
        평균=("점수", "mean"),
        중앙값=("점수", "median"),
        최댓값=("점수", "max"),
    ).round(2)