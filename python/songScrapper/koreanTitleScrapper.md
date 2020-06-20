# 한국어 제목 스크래핑 분류 및 오류 해결

## 목표:

    BeautifulSoup를 이용하여 스크래핑 한 제목 div에서 순수한 한국 노래 제목만 스트링으로 가져와야한다.
    한국어 제목 스크래핑 시 HTML element의 타입은 아래와 같은 총 6가지다.
    원하는 아웃풋은 예제 기준으로 "마음을 드려요"라는 스트링이다.

- **가.** Raw String

  ```html
  <div class="title-div">
    "마음을 드려요"
  </div>
  ```

- **나.** Raw String + 참조 Anchor

  ```html
  <div class="title-div">
    "마음을 드려요"
    <a href="#fn">[참조]</a>
  </div>
  ```

- **다.** Raw String + 제목 Anchor

  ```html
  <div class="title-div">
    "마음을"
    <a href="#">드려요</a>
  </div>
  ```

- **라.** 제목 Anchor + Raw String

  ```html
  <div class="title-div">
    <a href="#">마음을</a>
    "드려요"
  </div>
  ```

- **마.** 제목 Anchor + 참조 Anchor

  ```html
  <div class="title-div">
    <a href="#">마음을 드려요</a>
    <a href="#fn">[참조]</a>
  </div>
  ```

- **바.** 제목 Anchor

  ```html
  <div class="title-div">
    <>
    <br />
  </div>
  ```

## 해결 방안:

contents는 항상 2의 사이즈를 갖고 있으므로, contents[0], contenst[1] 로 확인한다.

1. 우선 div의 contents들중 anchor의 유무를 확인하여 필터링한다. Anchor가 없을시 무조건 첫번째 contents는 RawString.

   ```
   anchor 無: [가]
   achor 有: [나, 다, 라, 마, 바]
   ```

   가 --> str(contents[0])

2. anchor 가 존재하는 div contents 중 anchor 가 2개있는 경우를 필터링 한다. 둘 다 anchor인 경우에 항상 제목\[참조\] 형식이므로 contents[0]을 스트링으로 변환한다.

   ```
   anchor 2개: [마]
   anchor 1개: [나, 다, 라, 바]
   ```

   마 --> contents[0].get_text()

3. 참조는 항상 마지막에 나오므로, 두번째 anchor contents가 #fn인지 확인한다.

   ```
   contents[1] == 참조: [나]
   contenst[1] != 참조: [다, 라]

   Exception Tag Error: [바] // 두번째 contents <br>은 참조인지 확인하기 전 contents[1].name 이 None 인지 확인
   // contenst[1].name == None 인 경우는 contents[1] 이 RawString

   // 나, 바: 두개의 경우 contents[0] 를 스트링으로 변환
   ```

   나 --> str(contents[0])
   바 --> contents[0].get_text()

4. 나머지 경우에 대해서는 anchor, rawString을 get_text() 또는 str()을 사용하여 변환하여 concatenate함.
