# Eterea Eureka Service

[![Java Version](https://img.shields.io/badge/Java-24-blue.svg)](https://www.oracle.com/java/technologies/downloads/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.4.4-green.svg)](https://spring.io/projects/spring-boot)
[![Spring Cloud](https://img.shields.io/badge/Spring%20Cloud-2024.0.1-blue.svg)](https://spring.io/projects/spring-cloud)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/eterea/eureka-service/actions/workflows/maven.yml/badge.svg)](https://github.com/eterea/eureka-service/actions/workflows/maven.yml)
[![Documentation Status](https://github.com/eterea/eureka-service/actions/workflows/pages.yml/badge.svg)](https://github.com/eterea/eureka-service/actions/workflows/pages.yml)

## 📋 Descripción

El Servicio Eureka de Eterea es un componente fundamental de la arquitectura de microservicios que proporciona capacidades de registro y descubrimiento de servicios. Este servicio permite a otros microservicios registrarse y descubrirse entre sí, facilitando la comunicación y el balanceo de carga en la arquitectura distribuida.

## ✨ Características Principales

- Registro y descubrimiento automático de servicios
- Balanceo de carga entre instancias de servicios
- Monitoreo de estado de servicios en tiempo real
- Integración con Spring Cloud para una experiencia fluida
- Caché optimizado con Caffeine para mejor rendimiento
- Endpoints de Actuator para monitoreo y gestión

## 🚀 Comenzando

### Prerrequisitos

- Java 24
- Maven 3.9+
- Docker (opcional)

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/eterea/eureka-service.git
cd eureka-service
```

2. Compilar el proyecto:
```bash
mvn clean package
```

3. Ejecutar el servicio:
```bash
java -jar target/eureka-service-0.0.1-SNAPSHOT.jar
```

### Docker

Para ejecutar con Docker:
```bash
docker build -t eureka-service .
docker run -p 8761:8761 eureka-service
```

## 📚 Documentación

- [Documentación Técnica](https://eterea.github.io/eureka-service/)
- [Wiki del Proyecto](https://github.com/eterea/eureka-service/wiki)
- [Guía de API](https://eterea.github.io/eureka-service/api-documentation.html)

## 🛠️ Configuración

El servicio se puede configurar a través de `application.yml` o variables de entorno. Las configuraciones principales incluyen:

```yaml
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
  server:
    wait-time-in-ms-when-sync-empty: 0
```

## 🤝 Contribuyendo

Las contribuciones son bienvenidas. Por favor, lee nuestras [guías de contribución](CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

Para soporte o consultas, por favor abra un issue en el [repositorio](https://github.com/eterea/eureka-service/issues).

---

<div align="center">
  <sub>Construido con ❤️ por el equipo de Eterea</sub>
</div>
