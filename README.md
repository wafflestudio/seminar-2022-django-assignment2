# Assignment 2 (Project 1)

제출기한: 22.10.30(일) 23:59:59

## 안내
- 과제 1과 달리, maximum하게 구현할수록 점수가 가산됩니다. 하단 구축 사항들은 필수 사항들이지만, 실제 블로그에서 필요하다고 판단된다면 구현사항을 추가해서 구현해주세요.
- Third party library는 기본적으로 허용됩니다. 출제 의도를 벗어날 정도의 의견을 제공하는 라이브러리는 금지되니, 논란이 될만한 라이브러리 사용은 문의주세요.
- 구현 내용의 기준은 [medium.com](https://medium.com/) 입니다. 구현 내용 중 애매모호한 부분이 있을때는 참고해주시고, 그래도 해결이 되지 않는다면 문의주세요.


## The large blog service

![미디엄 대안](./medium-alternative.webp)

여러분은 medium에서 나와, 새로운 블로그의 Rest API를 설계해아 하는 스타트업 서버 개발자가 되었습니다. 

이런! 협업할 서버 개발자는 따로 없습니다.

---

기획자이자 대표 C씨는 우리 블로그는 다른 서비스와 무언가 다를거라고 강조하면서, 다음과 같이 유저 스토리를 작성해주셨습니다. 하단 유저 스토리들을 하나씩 구현해나가야 합니다. 
### 유저 스토리
- [ ] User
  - [ ] Create  
    - [ ] 유저는 아이디와 비밀번호로 서비스에 가입할 수 있다.
    - [ ] 비밀번호는 hash된 상태로 DB 테이블에 저장되어야 한다.
- [ ] Admin 
  - [ ] admin user의 경우 모든 authentication을 무시하고 요청을 날릴 수 있어야 한다.
- [ ] Post 
  - [ ] Create
    - [ ] (인증) 비회원은 Post를 생성할 수 없고, 오직 회원만 가능하다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `created_by, created_at, updated_at, title, description`
  - [ ] List 
    - [ ] (인증) 회원 / 비회원 모두 리스트 요청을 날릴 수 있다.
    - [ ] Post 내용은 List 요청시 최대 앞 300자만 보낸다.
  - [ ] Detail 
    - [ ] (인증) 회원 / 비회원 모두 상세 요청을 날릴 수 있다.
  - [ ] Delete 
    - [ ] (인증) 작성한 사람만 해당 Post를 삭제할 수 있다.
  - [ ] Update 
    - [ ] (인증) 작성한 사람만 해당 Post를 수정할 수 있다.
- [ ] Comment
  - [ ] Create 
    - [ ] (인증) 비회원은 Comment를 생성할 수 없고, 오직 회원만 가능하다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `post, created_by, created_at, updated_at, content, is_updated`
  - [ ] Detail은 따로 없다.
  - [ ] List 
    - [ ] (인증) 회원 / 비회원 모두 리스트 요청을 날릴 수 있다.
    - [ ] Post id로 해당 post의 comment를 불러올 수 있다.
    - [ ] updated된 comment는 따로 `(수정됨)` 이 노출될 예정이므로, 해당 정보를 표시할 칼럼이 필요하다.
  - [ ] Update 
    - [ ] (인증) 작성한 사람만 수정할 수 있다.
  - [ ] Delete 
    - [ ] (인증) 작성한 사람만 삭제할 수 있다.


---

클라이언트는 우선 React 개발자인 R씨 한명입니다. R씨는 다음과 같이 요청했습니다.

- 인증을 server side에서 API별로 빡세게 구현해주세요. Frontend에서 인증 로직을 빡세게 걸진 않을거에요.
  - [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) 을 사용해주세요.
- Client error 시 참고할 error를 예쁘게 내려주세요. validation이 실패했는데 500이 나면 안됩니다.
- 모든 list 요청에는 무한 로딩을 적용할 거에요. 생성 역순으로 정렬해주시고, 이에 맞는 [cursor pagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination) 을 적용해주세요.
- 페이지 렌더시 필요한데요, 리스트 요청시와 상세 요청시의 정보는 달라야해요.
  - 리스트 요청시 무거운 내용이 함께 내려오면 안돼요. network 비용이 증가합니다.

---
디자이너 D씨는 서버 개발자가 대체 뭐하는 건지는 모르겠지만, 모든 클라이언트 로딩이 2초 이상 걸리지 않게 협조해달라고 요청했습니다.

---

#### 추가 점수: Tag 기능
(꼭 구현할 필요는 없지만, 구현시 추가 점수가 부여됩니다. 구현했을시 PR 제목에 언급해주세요.)

<details>
<summary>여기를 클릭하기!</summary>

C씨는 post에도, comment에도 태그를 달고 추후 이 태그로 알고리즘을 돌리는 게 large 블로그 서비스의 핵심 차별성이라고 하셨습니다.

- [ ] Tag 
  - [ ] Create
    - [ ] 따로 Tag를 생성하는 API는 없다. Post 생성, Comment 생성시 태그를 달고, 이 태그가 존재하지 않을시 생성된다.
    - [ ] tag content가 해당 tag의 id이자, primary key 이다.
    - [ ] 당연히 해당 내용들은 필요하다. 다른 내용도 필요할수도?: `content`
  - [ ] Tag update는 존재하지 않는다.
  - [ ] Delete
    - [ ] 따로 Tag를 삭제하는 API는 없다. Post / Comment 삭제시, 해당 Tag를 가진 Post나 Comment가 없을 경우 삭제된다.
  - [ ] Post list by tag
    - [ ] 해당 태그가 달린 Post List를 불러올 수 있다.
    - [ ] (인증) 회원 / 비회원 모두 Post list by tag를 불러올 수 있다.
  - [ ] Comment list by tag
    - [ ] 해당 태그가 달린 Comment List를 불러올 수 있다.
    - [ ] (인증) 회원 / 비회원 모두 Comment list by tag를 불러올 수 있다.

</details>

---
## 제출
[requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files) 를 작성하고, 해당 repository root에 django project를 업로드해 PR요청을 날려주세요.
