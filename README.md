# foodgram-project
Описание проекта
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикую рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Демо: http://178.154.198.140/ Логин root2, пароль admin

![foodgram-project](https://github.com/RustamIR/foodgram-project/workflows/foodgram/badge.svg)

##Установка и запуск в Docker контейнере

 - Клонируйте проект с репозитория 
```
 git clone https://github.com/RustamIR/foodgram-project.git
```

 - Перейдите в проект 
```
cd foodgram-project/
```
 - Запустить контейнеры
```
sudo docker-compose up
```
 - Перейти в контейнер web
```
docker-compose exec <web-name-container> bash
```
 - Внутри контейнера выполнить следующие команды:
 ```
python manage.py makemigrations 
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures.json
```

Приложение готово к работе

##Стэк технологий
 - Docker
 - Nginx
 - Djnago
 - Django Rest Framework
 - JS, CSS, HTML
 
 #Об авторе:
 Иштеев Рустам: https://ufa.hh.ru/applicant/resumes/view?resume=7c488b34ff0896d6de0039ed1f7274734a4246