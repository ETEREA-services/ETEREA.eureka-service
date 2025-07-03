import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader

def load_data(data_dir='../data'):
    """Carga los datos de issues, milestones y releases desde archivos JSON."""
    # Crear directorio de datos si no existe y ficheros dummy
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(os.path.join(data_dir, 'issues.json')):
        with open(os.path.join(data_dir, 'issues.json'), 'w') as f:
            json.dump([], f)
    if not os.path.exists(os.path.join(data_dir, 'milestones.json')):
        with open(os.path.join(data_dir, 'milestones.json'), 'w') as f:
            json.dump([], f)
    if not os.path.exists(os.path.join(data_dir, 'releases.json')):
        with open(os.path.join(data_dir, 'releases.json'), 'w') as f:
            json.dump([], f)

    with open(os.path.join(data_dir, 'issues.json'), 'r') as f:
        issues = json.load(f)
    with open(os.path.join(data_dir, 'milestones.json'), 'r') as f:
        milestones = json.load(f)
    with open(os.path.join(data_dir, 'releases.json'), 'r') as f:
        releases = json.load(f)
    return issues, milestones, releases

def load_config(config_file='../src/main/resources/bootstrap.yml'):
    """Carga la configuración de la aplicación desde un archivo YAML."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def generate_docs(output_dir='../docs'):
    """Genera la documentación del proyecto en el directorio de salida."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    issues, milestones, releases = load_data()
    config = load_config()
    
    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)

    # Generar index.md
    template = env.get_template('index.md.j2')
    with open(os.path.join(output_dir, 'index.md'), 'w') as f:
        f.write(template.render(
            title="Welcome to Eterea Eureka Service",
            description="This is the main documentation for the Eterea Eureka Service. Here you will find all the necessary information to understand, use, and contribute to the project."
        ))

    # Generar getting-started.md
    template = env.get_template('getting-started.md.j2')
    with open(os.path.join(output_dir, 'getting-started.md'), 'w') as f:
        f.write(template.render(
            title="Getting Started",
            description="This guide will walk you through the process of setting up the Eterea Eureka Service in your local environment for development and testing purposes."
        ))

    # Generar configuration.md
    template = env.get_template('configuration.md.j2')
    with open(os.path.join(output_dir, 'configuration.md'), 'w') as f:
        f.write(template.render(
            title="Configuration Guide",
            description="This section details the configuration options available for the Eureka service.",
            config=config
        ))

    # Generar monitoring.md
    template = env.get_template('monitoring.md.j2')
    with open(os.path.join(output_dir, 'monitoring.md'), 'w') as f:
        f.write(template.render(
            title="Monitoring and Management",
            description="The service exposes several endpoints for monitoring and management via Spring Boot Actuator."
        ))

    # Generar contributing.md
    template = env.get_template('contributing.md.j2')
    with open(os.path.join(output_dir, 'contributing.md'), 'w') as f:
        f.write(template.render(
            title="Contributing",
            description="We welcome contributions from the community. Please follow these guidelines to ensure a smooth and effective collaboration process."
        ))

    # Generar changelog.md
    template = env.get_template('changelog.md.j2')
    with open(os.path.join(output_dir, 'changelog.md'), 'w') as f:
        f.write(template.render(
            title="Changelog",
            releases=releases
        ))

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Crear/Actualizar templates
    with open('templates/index.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
nav_order: 1
---

# {{ title }}

{{ description }}

## Architecture Overview

The Eterea Eureka Service is a central component in the Eterea microservices ecosystem. It acts as a service registry, allowing other services to register themselves and discover others.

```mermaid
graph TD
    subgraph "Eterea Ecosystem"
        A[Eureka Service]
        B[Microservice 1]
        C[Microservice 2]
        D[API Gateway]
    end

    B -- Registers with --> A
    C -- Registers with --> A
    D -- Discovers services from --> A
    B -- Communicates with --> C
```
""")

    with open('templates/getting-started.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
parent: "User Guide"
nav_order: 2
---

# {{ title }}

{{ description }}

## Prerequisites

- Java 24 or higher
- Maven 3.9 or higher
- Git

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/eterea-project/eterea.eureka-service.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd eterea.eureka-service
    ```
3.  Build the project using Maven:
    ```bash
    ./mvnw clean install
    ```

## Running the Application

You can run the application using the following command:

```bash
java -jar target/eterea.eureka-service-*.jar
```
""")

    with open('templates/configuration.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
parent: "User Guide"
nav_order: 3
---

# {{ title }}

{{ description }}

The application is configured via `src/main/resources/bootstrap.yml`. Below is a summary of the key properties.

## Application Settings
| Property | Default Value | Description |
|---|---|---|
| `app.port` | `${APP_PORT:8761}` | Port on which the application will run. Can be overridden by the `APP_PORT` environment variable. |
| `app.logging` | `debug` | Default logging level for the application. |

## Server Configuration
| Property | Value | Description |
|---|---|---|
| `server.port` | `${app.port}` |  Inherits the port from the `app.port` property. |

## Spring Application
| Property | Value | Description |
|---|---|---|
| `spring.application.name` | `eureka-service` | Name of the Spring application. |

## Eureka Configuration
| Property | Description |
|---|---|
| `eureka.instance.hostname` | `localhost` | The hostname of the Eureka server instance. |
| `eureka.client.register-with-eureka` | `false` | This instance should not register itself with another Eureka server. |
| `eureka.client.fetch-registry` | `false` | This instance should not fetch the registry from another Eureka server. |
| `eureka.client.server-url.defaultZone` | The URL for other services to connect to this Eureka server. |

## Logging
| Path | Level | Description |
|---|---|---|
| `logging.level.eterea.eureka.service` | `${app.logging}` | Logging level for the main application package. |
| `logging.level.web` | `${app.logging}` | Logging level for web-related components. |
| `logging.level.org.springframework.cloud.config` | `${app.logging}` | Logging level for Spring Cloud Config client. |

## Management Endpoints
| Property | Value | Description |
|---|---|---|
| `management.endpoints.web.exposure.include` | `*` | Exposes all Actuator endpoints over HTTP. |
| `management.endpoint.health.show-details` | `always` | Always shows full details in the `/actuator/health` endpoint. |

""")

    with open('templates/monitoring.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
parent: "User Guide"
nav_order: 4
---

# {{ title }}

{{ description }}

The Actuator endpoints are available under the `/actuator` path. For example, to check the health of the service, you can access `http://localhost:8761/actuator/health`.

## Key Endpoints

| Endpoint | Description |
|---|---|
| `/actuator/health` | Shows the application's health status. |
| `/actuator/info` | Displays arbitrary application info. |
| `/actuator/metrics` | Provides detailed metrics about the application. |
| `/actuator/env` | Shows the current environment properties. |
| `/actuator/beans` | Lists all Spring beans in the application. |
| `/actuator/configprops` | Displays all `@ConfigurationProperties`. |

For a full list of endpoints and their descriptions, please refer to the [Spring Boot Actuator documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html).
""")

    with open('templates/contributing.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
nav_order: 5
---

# {{ title }}

{{ description }}

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the standards of behavior we expect from our community members.

## How to Contribute

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Push your changes to your fork.
5.  Create a pull request to the `main` branch of the original repository.
""")

    with open('templates/changelog.md.j2', 'w') as f:
        f.write("""---
layout: default
title: {{ title }}
nav_order: 6
---

# {{ title }}

All notable changes to this project will be documented in this file.

{% for release in releases %}
## [{{ release.tag_name }}] - {{ release.published_at[:10] }}

{{ release.body }}
{% endfor %}
""")

    # Añadir dependencia PyYAML si no está
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Installing...")
        os.system('pip install PyYAML')

    generate_docs()
