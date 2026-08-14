# Common

La app `common` contiene componentes reutilizables para todo el proyecto Pámi y para futuros proyectos Lyon Dev.

## Responsabilidad

`common` no debe contener lógica específica de Pámi, confecciones, papelería o tecnología.

Debe contener únicamente elementos reutilizables:

- Modelos base
- Mixins
- Managers
- Validadores
- Constantes
- Choices
- Excepciones
- Utilidades generales

## Modelos base

- `UUIDModel`
- `TimeStampedModel`
- `SoftDeleteModel`
- `BaseModel`

## Mixins

- `PublishableMixin`
- `SEOModel`
- `SortableMixin`

## Managers

- `ActiveManager`
- `PublishedManager`

## Regla

Si una funcionalidad pertenece a un módulo específico, no debe ir en `common`.