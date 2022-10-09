### Large blog service
maximum하게 구현할수록 점수가 가산
실제 블로그에서 필요하다고 판단된다면 구현사항을 추가해서 구현해주세요.
### 유저 스토리
- [ ] User
  - [ ] Create  
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

  - [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) 을 사용해주세요.
- Client error 시 참고할 error를 예쁘게 내려주세요. validation이 실패했는데 500이 나면 안됩니다.
- 모든 list 요청에는 무한 로딩을 적용할 거에요. 생성 역순으로 정렬해주시고, 이에 맞는 [cursor pagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination) 을 적용해주세요.
- 페이지 렌더시 필요한데요, 리스트 요청시와 상세 요청시의 정보는 달라야해요.
  - 리스트 요청시 무거운 내용이 함께 내려오면 안돼요. network 비용이 증가합니다.

- 클라이언트 로딩이 2초 이하

### Tag 기능

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
    - [ ] 해당 태그가 달린 Post List를 불러올 수 있다.
    - [ ] (인증) 회원 / 비회원 모두 Comment list by tag를 불러올 수 있다.
