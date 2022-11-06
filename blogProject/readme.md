# API 안내 및 기타사항

본 API는 블로그의 서버를 서비스하기 위해 제작되었습니다.

포함하고 있는 주요 기능은 회원가입, 토큰 발행, 블로그 기능입니다.

## API 안내

- /register/signup/

    - POST 요청을 통해 계정을 생성할 수 있습니다. 입력값으로는 "username',
      "email", "password" 가 필요합니다. password 는 해시된 상태로 DB 테이블에 저장됩니다.
    - 유저 생성은 admin user 이거나, anonymous user 만 가능합니다.
    - 유저 생성과 동시에 토큰이 생성됩니다.
- /register/token/${user_id}/
    - GET 요청을 통해 유저의 토큰 값을 가져옵니다.
    - GET 요청은 admin user 혹은 유저 본인만 가능합니다. 즉, 유저 A는 본인의 토큰만을 조회할 수 있고, 유저 B의 토큰을 조회할 수 없습니다.
- /blog/posts/
    - GET 요청을 통해 post list를 조회합니다. cursor_pagin
ation 을 통해 최근 생성일 순으로 10개의 post를 조회할 수 있습니다.
글의 전체 내용을 최대 앞의 300글자만 가져옵니다.
    - GET 요청은 인증 / 비인증된 유저 모두 가능합니다.
    - POST 요청을 통해 새로운 post를 생성할 수 있습니다.
“title”, “description”, “tags”를 입력받을 수 있습니다. “title”, “description”은 필수 값이며, blank가 불가능합니다. “tags”는 Tag의 list 형식으로, tag 하나마다 {“content”: “content”} 형식을 취해야합니다. 
    - 예시) tags = [ {“content”: “tagA”}, {“content”: “tagB”}]
    - POST 요청은 admin user 또는 인증된 유저만 가능합니다.
- /blog/posts/${post_id}/
    - GET 요청을 통해 특정 post의 세부내용을 조회합니다. 
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.
    - PUT/PATCH/DELETE 요청은 admin user 또는 해당 post를 작성한 유저만 가능합니다.
- /blogs/posts/${post_id}/comments/
    - GET 요청을 통해 특정 post의 comment list를 조회합니다.
cursor_pagination 을 통해 최근 생성일 순으로 10개의 comment를 조회할 수 있습니다.
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.
    - POST 요청을 통해 특정 post에 새로운 comment를 생성할 수 있습니다.
“content”, “tags”를 입력받을 수 있습니다. “content”는 필수 값이며, blank가 불가능합니다. “tags”는 Tag의 list 형식으로, tag 하나마다 {“content”: “content”} 형식을 취해야합니다.
    - 예시) tags = [ {“content”: “tagA”}, {“content”: “tagB”}
    - POST 요청은 admin user 또는 인증된 유저만 가능합니다.
- /blogs/comments/${comment_id}/
    - GET 요청을 통해 특정 comment의 detail을 조회합니다.
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.
    - PUT/PATCH/DELETE 요청은 admin user 또는 comment를 작성한 유저만 가능합니다.
- /blogs/tags/
    - GET 요청을 통해 tag list 를 조회합니다.
  cursor_pagination 을 통해 'content' 사전 순으로 10개의 tag를 조회할 수 있습니다.
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.
- /blogs/posts/tags/{str:content}/
    - GET 요청을 통해 특정 content를 가진 post list를 조회합니다.
cursor_pagination 을 통해 최근 생성일 순으로 10개의 post를 조회할 수 있습니다.
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.
- /blogs/comments/tags/{str:content}/
    - GET 요청을 통해 특정 content를 가진 comment list를 조회합니다.
  cursor_pagination 을 통해 최근 생성일 순으로 10개의 comment를 조회할 수 있습니다.
    - GET 요청은 인증/비인증된 유저 모두 가능합니다.

## 기타사항
tag는 post 또는 comment를 생성할 때 함께 생성할 수 있습니다.
따로 tag를 Delete하는 요청은 존재하지 않습니다. post 또는 comment가 삭제되어
특정 tag가 어느 곳에서도 참조되지 않는다면, tag를 삭제합니다.

## 추가구현사항
1. comment의 DetailView가 없는 상태로 수정/삭제를 구현하는 것이 더 어렵다고
판단히여 DetailView를 구현하였습니다.
2. Tag의 update를 구현하였습니다.

## 미구현사항
1. Tag Model 에서, content 를 primary key 로 사용하는 것을 구현하지 못했습니다.
ManyToMany Field 로 Post와 Comment, Tag 를 이어주는 테이블이
생성될 때 항상 테이블의 column에 tag_id가 들어가 해결방법을 찾지 못했습니다.
대신 tag_id를 사용해 과제에서 요구하던 tag 관련 동작들은 모두 구현하였습니다.
2. 과제의 "Client error 시 참고할 error를 예쁘게 내려주세요. validation이 실패했는데 500이 나면 안됩니다."
가 어떤 의미인지 이해하지 못했습니다.