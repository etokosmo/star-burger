# Star Burger food delivery website

This is the website of the Star Burger restaurant chain. Here you can order excellent burgers with home delivery.

> An example of website is available at the link: [etokosmo.ru](https://etokosmo.ru/).

## About

The Star Burger chain combines several restaurants operating under a single franchise. All restaurants have the same menu and the same prices. Just select a dish from the menu on the site and specify the place of delivery. We will find the nearest restaurant to you, cook everything and deliver it to you.

### The site has three independent interfaces.

<details>
<summary>The first is the public part, where you can choose dishes from the menu and quickly place an order without registration and SMS.</summary>

### Main website

![Star Burger](https://user-images.githubusercontent.com/93794917/235744358-021efb43-1ca1-44a8-a8d4-67f7053fd715.gif)

### Try to order

![Star Burger (2)](https://user-images.githubusercontent.com/93794917/235748425-a2b4b9c5-6482-48ca-924c-6cf9b71b9c2f.gif)


</details>

<details>
<summary>The second interface is for the manager. This is where order processing takes place. The manager sees incoming new orders and first calls the client to confirm the order. After that, the operator selects the nearest restaurant and transfers the order there for execution. There, the dishes will be cooked and the food will be delivered to the client.</summary>

### You can manage orders

![image](https://user-images.githubusercontent.com/93794917/235747843-10ef6a83-8445-4cc8-b9a7-3b38aafaa800.png)

### You can manage menu

![image](https://user-images.githubusercontent.com/93794917/235746333-7d76b21d-0f8d-426e-9653-5087cdd2a543.png)

### You can manage restaurants

![image](https://user-images.githubusercontent.com/93794917/235746450-927adf75-6644-48e7-aa60-bb29900ec069.png)


</details>

<details>
<summary>The third interface is the admin panel. Mostly it is used by programmers when developing a site. The manager also comes in to update the Star Burger restaurant menu.</summary>

![image](https://user-images.githubusercontent.com/93794917/235746969-5fbf71fb-8617-4022-b195-a396dd745c0d.png)


</details>

## Configurations

* Python version: 3.9
* Libraries: [requirements.txt](https://github.com/etokosmo/star-burger/blob/master/backend/requirements.txt)

## Create `.env` file

- Write the environment variables in the `.env` file in the format KEY=VALUE

`SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

`ALLOWED_HOSTS` - A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.

`DEBUG` - A boolean that turns on/off debug mode. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py).

`POSTGRES_DB` - Set db name for creating Database.

`POSTGRES_USER` - Set username for creating user.

`POSTGRES_PASSWORD` - Set password for giving the user a password.

`DATABASE_URL` - URL to db. For more information check [this](https://github.com/jazzband/dj-database-url).

`YANDEX_GEO_API_TOKEN` — Yandex Geo API token. [For more information check documentation.](https://developer.tech.yandex.ru/)

`ROLLBAR_ACCESS_TOKEN` — Rollbar token to have access to the logs. [For more information check documentation.](https://rollbar.com/)

`ROLLBAR_ENVIRONMENT` — Site installation, default `development`

`CERTBOT_EMAIL` - Your email for Certbot. You need this if you want deploy with SSL. [For more information check documentation.](https://certbot.eff.org/)

## Deploy with Docker

### Local version

- Download code
- Install Docker
- Write the environment variables in the `.env` file in the format KEY=VALUE
- Create images and run container with command:
```bash
docker compose up --build
```
- Open `localhost:8080`

### Production version

- Download code
- Install Docker
- Write the environment variables in the `.env` file in the format KEY=VALUE
- Create images with command:
```bash
docker compose -f docker-compose.prod.yml build
```
- Run containers with command:
```bash
docker compose -f docker-compose.prod.yml up -d
```
### Production version with SSL

- Download code
- Install Docker
- Write the environment variables in the `.env` file in the format KEY=VALUE
- Create images with command:
```bash
docker compose -f docker-compose.prod_ssl.yml build
```
- Run containers with command:
```bash
docker compose -f docker-compose.prod_ssl.yml up -d
```
- Set var `git_revision` with command:
```bash
git_revision=$(git rev-parse HEAD)
```
- Report a deploy to Rollbar 
```bash
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header 'X-Rollbar-Access-Token: '$ROLLBAR_ACCESS_TOKEN'' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '{"environment": "'$ROLLBAR_ENVIRONMENT'", "revision": "'$git_revision'"}'
```
- Or you can run deploy script with command:
```bash
./deploy_star_burger_docker.sh
```

## Launch without Docker

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

<details>
<summary>Как собрать бэкенд</summary>

Скачайте код:
```sh
git clone https://github.com/etokosmo/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```
Получите токен [API Яндекс-геокодера](https://developer.tech.yandex.ru/). Впишите его в `.env` в формате:
```
YANDEX_GEO_API_TOKEN:ваш_токен
```



Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.
</details>

<details>
<summary>Собрать фронтенд</summary>

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v12.18.2
# Если ошибка, попробуйте node:
node --version
# v12.18.2

npm --version
# 6.14.5
```

Версия `nodejs` должна быть не младше 10.0. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточно и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.
</details>

## Как запустить prod-версию сайта

Собрать фронтенд:

```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

Настроить бэкенд: создать файл `.env` в каталоге `star_burger/` со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_GEO_API_TOKEN` — [API Яндекс-геокодера](https://developer.tech.yandex.ru/)
- `ROLLBAR_ACCESS_TOKEN` — [см. документацию Rollbar](https://rollbar.com/)
- `ROLLBAR_ENVIRONMENT` — инсталляции сайта, по умолчанию `development`

