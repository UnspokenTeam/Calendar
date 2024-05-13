# Calendar Backend

###### Backend для приложения Calendar

## Содержание

1. ### [Secrets](#secrets)
2. ### [Запуск](#запуск)

## Secrets

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

###### Все команды применяются в директории deployments и для примера взят microk8s

1. Создание базы даннных
   ```shell
   microk8s microk8s kubectl apply -f ./postgres
   ```
2. Создание сервисов
   ```shell
   microk8s kubectl apply -f ./notification_service
   microk8s kubectl apply -f ./event_service
   microk8s kubectl apply -f ./identity_service
   microk8s kubectl apply -f ./notification_service
   ```
3. Создание Gateway
   ```shell
   microk8s kubectl apply -f ./gateway
   ```
4. Создание тунеля
   ```shell
   microk8s kubectl port-forward --address 0.0.0.0 --namespace default svc/gateway-service 8084:8084
   ```

###### Backend будет доступен по ip 0.0.0.0:8084
