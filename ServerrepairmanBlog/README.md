### API 주소
- [ ] User

  - /blog/post/register/
    [ ] POST : 회원가입 및 authtoken 발급

        ```
        request : {
            "id" : "",
            "password" : "",
            "first_name" : "",
            "last_name" : "",
            "email" : ""
        }
        response : {
            "Token" : ""
        }
        ```

- [ ] Post 
  - /blog/posts/
    [ ] GET : post list 요청. 생성시간 역순 기준, 5개 기준으로 pagination

        ```
        request : {}
        response : {
            "count" : 0,
            "next" : null,
            "previous" : null,
            "results" : [{
	    		    "id": 1,
	    		    "created_by": {
	    		    	"id": 2,
	    		    	"username": "",
	    		    	"email": ""
	    		    },
	    		    "title": "",
	    		    "content": "", // 최대길이 300 제한
	    		    "created_at": "2022-11-08T05:46:37.506875Z"
	    	    },
                ...
            ]
        }
        ```

    [ ] POST : 새 post 생성. 로그인 필요

        ```
        request : {
            "title" : "",
            "content" : "",
            "tags" : [
                "tag1", 
                "tag2"
                ]
        }
        response : {
	        "title": "",
	        "id": 1,
	        "created_by": {
	        	"id": 2,
	        	"username": "",
	        	"email": ""
	        },
	        "created_at": "2022-11-08T10:30:34.396876Z",
	        "updated_at": null, 
	        "content": "",
	        "tags": [
	        	"tag1",
	        	"tag2"
	        ]
        }
        ```
  - /blog/posts/<int:pk>/
    [ ] GET : id가 pk인 post의 detail을 요청.

        ```
        request : {}
        response : {
	        "title": "",
	        "id": 1,
	        "created_by": {
	        	"id": 2,
	        	"username": "",
	        	"email": ""
	        },
	        "created_at": "2022-11-08T10:30:34.396876Z",
	        "updated_at": null, 
	        "content": "",
	        "tags": [
	        	"tag1",
	        	"tag2"
	        ]
        }
        ```

    [ ] PUT : id가 pk인 post를 수정. pk번 post 생성자/Admin 만 가능

        ```
        request : {
            "title" : "",
            "content" : "",
            "tags" : [
                "tag1", 
                "tag2"
                ]
        }
        response : {
	        "title": "",
	        "id": 1,
	        "created_by": {
	        	"id": 2,
	        	"username": "",
	        	"email": ""
	        },
	        "created_at": "2022-11-08T10:30:34.396876Z",
	        "updated_at": null, 
	        "content": "",
	        "tags": [
	        	"tag1",
	        	"tag2"
	        ]
        }
        ```

    [ ] PATCH : id가 pk인 post를 일부만 수정. pk번 post 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
	        "title": "",
	        "id": 1,
	        "created_by": {
	        	"id": 2,
	        	"username": "",
	        	"email": ""
	        },
	        "created_at": "2022-11-08T10:30:34.396876Z",
	        "updated_at": null, 
	        "content": "",
	        "tags": [
	        	"tag1",
	        	"tag2"
	        ]
        }
        ```

    [ ] DELETE : id가 pk인 post를 제거. pk번 post 생성자/Admin 만 가능

        ```
        request : {}
        response : 204 No Content
        ```

- [ ] Comment
  - /blog/comments/
    [ ] GET : comment의 리스트를 요청

       ```
       request : {}
       response : {
       	"count": 4,
       	"next": null,
       	"previous": null,
       	"results": [
    		{
    			"id": 1,
    			"created_by": {
    				"id": 1,
    				"username": "",
    				"email": ""
    			},
    			"content": "",
    			"post": 3
    		},
           ...
       }
       ```

    [ ] POST : 새 comment를 생성
    
        ```
        request : {
            "content" : "",
	        "post_id" : 3
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

  - /blog/comments/<int:pk>/
    [ ] GET : id가 pk인 comment의 detail을 요청

        ```
        request : {}
        response : {
        	"id": 1,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "",
        		"email": ""
        	},
        	"created_at": "2022-11-08T06:10:11.607727Z",
        	"updated_at": null,
        	"content": "",
        	"tags": [
                "commenttag1",
                "commenttag2"
            ]
        }
        ```

    [ ] PUT : id가 pk인 comment를 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [ ] PATCH : id가 pk인 comment를 일부만 수정. pk번 comment 생성자/Admin 만 가능

        ```
        request : {
            "content" : "",
        }
        response : {
        	"id": 14,
        	"post": 3,
        	"created_by": {
        		"id": 2,
        		"username": "testuser2",
        		"email": ""
        	},
        	"created_at": "2022-11-08T11:02:35.522016Z",
        	"updated_at": null,
        	"content": "",
        	"tags": []
        }
        ```

    [ ] DELETE : id가 pk인 comment를 제거. pk번 comment 생성자/Admin 만 가능

        ```
        request : {}
        response : 204 No Content
        ```

  - [ ] /blog/posts/<int:post_id>/comments/
    
    [ ] GET : id가 post_id인 post에 달린 comment의 리스트를 요청.

        ```
        request : {}
        response : {
    	    "count": 2,
	        "next": null,
	        "previous": null,
	        "results": [
	        	{
	        		"id": 15,
	        		"created_by": {
	        			"id": 2,
	        			"username": "testuser2",
	        			"email": ""
	        		},
	        		"content": "",
	        		"post": 14
	        	},
                ...
	        ]
        }
        ```

- [ ] Tag
  - /blog/posts/tags/
    [ ] GET : post에 붙은 태그들의 리스트를 요청

        ```
        request : {}
        response : {
            "count": 3,
	        "next": null,
	        "previous": null,
	        "results": [
	        	{
	        		"content": "tag1"
	        	},
	        	{
	        		"content": "tag2"
	        	},
	        	{
	        		"content": "tag3"
	        	}
	        ]
        }
        ```

  - /blog/posts/tags/<str:tag>/
    [ ] GET : tag가 태그로 붙은 post의 list를 요청. 생성시간 역순 기준

        ```
        request : {}
        response : {
            "count" : 0,
            "next" : null,
            "previous" : null,
            "results" : [{
	    		    "id": 1,
	    		    "created_by": {
	    		    	"id": 2,
	    		    	"username": "",
	    		    	"email": ""
	    		    },
	    		    "title": "",
	    		    "content": "", // 최대길이 300 제한
	    		    "created_at": "2022-11-08T05:46:37.506875Z"
	    	    },
                ...
            ]
        }
        ```

  - /blog/comments/tags/
    [ ] GET : comment에 붙은 태그들의 리스트를 요청

        ```
        request : {}
        response : {
        	"count": 2,
        	"next": null,
        	"previous": null,
        	"results": [
        		{
        			"content": "commenttag1"
        		},
        		{
        			"content": "commenttag2"
        		}
        	]
        }
        ```

  - /blog/posts/tags/<str:tag>/
    [ ] GET : tag가 태그로 붙은 comment의 list를 요청. 생성시간 역순 기준

        ```
        request : {}
        response : {
        	"count": 2,
        	"next": null,
        	"previous": null,
        	"results": [
        		{
        			"id": 1,
        			"created_by": {
        				"id": 1,
        				"username": "",
        				"email": ""
        			},
        			"content": "",
        			"post": 3
        		},
                ...
        	]
        }
        ```

  