# 에셋 생성 스크립트

README의 그래픽은 전부 여기서 만듭니다. 항목이나 수치가 바뀌면 해당 스크립트 위쪽의
데이터만 고치고 다시 실행하세요.

```bash
python3 gen_images.py    # 앱 아이콘 스퀘어클, 디바이스 프레임 스크린샷  (Pillow 필요)
python3 gen_apps.py      # 런처 스타일 앱 패널   (gen_images.py 이후에 실행, Pillow 필요)
python3 gen_walkers.py   # 걷는 도트 띠          (포스크탑 캐시 필요, Pillow 필요)
python3 gen_hero.py      # 히어로 배너
python3 gen_cards.py     # 기술 스택 칩
python3 gen_contrib.py   # 기여도 잔디           (네트워크 필요)
python3 gen_langs.py     # 언어 비중             (네트워크 필요)
```

## 알아둘 것

- `icon-*.png` 는 README가 직접 참조하지 않습니다. `gen_apps.py` 가 런처 패널로 합칠 때
  쓰는 중간 산출물이라 지우면 안 됩니다.
- `gen_images.py` 와 `gen_walkers.py` 는 이 저장소 밖의 원본을 읽습니다. 경로는 각
  스크립트의 `SRC` / `CACHE` 상수에 있습니다. 원본이 없는 환경에서는 돌지 않습니다.
- `gen_contrib.py` 와 `gen_langs.py` 만 네트워크에서 값을 읽습니다. 이 둘은
  `.github/workflows/refresh-cards.yml` 이 매주 다시 돌려 커밋합니다.
- 걷는 도트는 SpriteCollab(CC BY-NC 4.0)입니다. 출처 표기는 README 본문에 있고,
  상업적 이용은 라이선스가 허용하지 않습니다.
