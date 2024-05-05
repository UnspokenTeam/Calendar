# Calendar Backend

###### Backend для приложения Calendar

---

## Содержание

---

1. ### [Secrets](#secrets)
2. ### [Запуск](#запуск)

## Secrets

---

**_Для запуска проекта при помощи Kubernetes, требуется прописать несколько конфигурационных secret файлов_**

1. ### ```deployments/event_service/event_service_secret.yaml```
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: event-service-secret
    data:
      # Url для доступа к базе данных, где хост - postgres-service.default.svc.cluster.local
      DATABASE_URL: "VALUE_IN_BASE_64_ENCODING"
      # Вид окружения DEVELOPMENT или PRODUCTION
      ENVIRONMENT: "VALUE_IN_BASE_64_ENCODING"
      # Api key для доступа к OpenRouter
      OPENROUTER_API_KEY: "VALUE_IN_BASE_64_ENCODING"
    ```
2. ### ```deployments/invite_service/invite_service_secret.yaml```
    ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
    name: invite-service-secret
   data:
      # Url для доступа к базе данных, где хост - postgres-service.default.svc.cluster.local
      DATABASE_URL: "VALUE_IN_BASE_64_ENCODING"
      # Вид окружения DEVELOPMENT или PRODUCTION
      ENVIRONMENT: "VALUE_IN_BASE_64_ENCODING"
    ```
3. ### ```deployments/identity_service/identity_service_secret.yaml```
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: identity-service-secret
   data:
     # Ключ для генерации Access token
     ACCESS_SECRET: "VALUE_IN_BASE_64_ENCODING"
     # Ключ для генерации Refresh token
     REFRESH_SECRET: "VALUE_IN_BASE_64_ENCODING"
     # Url для доступа к базе данных, где хост - postgres-service.default.svc.cluster.local
     DATABASE_URL: "VALUE_IN_BASE_64_ENCODING"
     # Вид окружения DEVELOPMENT или PRODUCTION
     ENVIRONMENT: "VALUE_IN_BASE_64_ENCODING"
     # Время истечения срока валидности Refresh token в днях
     REFRESH_TOKEN_EXPIRATION: "VALUE_IN_BASE_64_ENCODING"
     # Время истечения срока валидности Access token в минутах
     ACCESS_TOKEN_EXPIRATION: "VALUE_IN_BASE_64_ENCODING"
   ```
4. ### ```deployments/notification_service/notification_service_secret.yaml```
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: notification-service-secret
   data:
     # Url для доступа к базе данных, где хост - postgres-service.default.svc.cluster.local
     DATABASE_URL: "VALUE_IN_BASE_64_ENCODING"
     # Вид окружения DEVELOPMENT или PRODUCTION
     ENVIRONMENT: "VALUE_IN_BASE_64_ENCODING"
   ```
5. ### ```deployments/postgres/postgres-secret.yaml```
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: postgres-secret
   data:
     # Пароль для админа бд
     POSTGRES_PASSWORD: "VALUE_IN_BASE_64_ENCODING"
   ```
## Запуск

---

###### Все комманды применяются в директории deployments

1. Применение Secrets
   ```shell
   kubectl apply -f ./postgres/postgres-secret.yaml, event_service/event_service_secret.yaml,./invite_service/invite_service_secret.yaml,./identity_service/identity_service_secret.yaml,./notification_service/notification_service_secret.yaml
   ```
2. Создание базы даннных
   ```shell
   kubectl apply -f ./postgres/postgres-stateful-set.yaml, ./postgres/postgres_service.yaml
   ```
3. Создание сервисов
   ```shell
   kubectl apply -f ./notification_service/notification_service-deployment.yaml, ./identity_service/identity_service-deployment.yaml, ./invite_service/invite_service-deployment.yaml, ./event_service/event_service-deployment.yaml
   ```
4. Создание Service объектов для сервисов
   ```shell
   kubectl apply -f ./notification_service/notification_service-service.yaml, ./identity_service/identity_service-service.yaml, ./invite_service/invite_service-service.yaml, ./event_service/event_service-service.yaml
   ```
5. Создание Gateway
   ```shell
   kubectl apply -f ./gateway/gateway_deployment.yaml, ./gateway/gateway_service.yaml
   ```

###### Backend будет доступен по externalIp, который указан в ```deployments/gateway/gateway_service.yaml```
