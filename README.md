# Django demo template

Шаблон для настройки пайплайна деплоя Django приложения

## Задачи

1. Сделать **публичный** fork этого репозитория
2. Добавить Jenkinsfile с одним stage, который запускает тесты на джангу
3. Создать multibranch pipeline в jenkins с этим репозиторием
4. Настройте запуск по webhook
5. Создать Dockefile, который будет собирать Django приложение с uvicorn
6. Создать stage сборки docker контейнера
7. Создать репозиторий в dockerhub
8. Создать stage, который пушит собранный образ в dockerhub
9. testing :) (ploho testitsa :(((( )
