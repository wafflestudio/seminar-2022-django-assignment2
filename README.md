# Medium alternative : Large Scale Blog Service
![logo_new](https://user-images.githubusercontent.com/81140673/196366827-142b7ced-6cf0-426b-b72c-a1f7b68e7b60.png)
- 작성자 : 박용주 (2022.10.13)


<br></br>

# Overview
![new명세](https://user-images.githubusercontent.com/81140673/196373512-fc2c68a4-f84e-4c1c-aa44-d33604727ec6.png)

<br></br>

# User App
## Models
|Fields|Type|
|-|-|
|username|CharField|
|password|CharField|
|nickname|CharField|
|short_bio|CharField|
|photo|ImageField|
|url|URLField|
|followers|ManyToManyField('self')|
|following|ManyToManyField('self')|
|post_count|self.post.all().count()|
|followers_count|self.followers.all().count()|
|following_count|self.following.all().count()|
<br></br>

## Urls
|기능|url|viewset|Authentication|
|-|-|-|-|
|회원가입|register/|Register| - |
|로그인|login/|Login|-|
<br></br>

## Views
<br></br>
<br></br>

# Post App
<br></br>

## Models
<br></br>

## Urls
<br></br>

## Views
<br></br>

# Notification App
<br></br>

## Models
<br></br>

## Urls
<br></br>

## Views
<br></br>

## environment
- requirements.txt
