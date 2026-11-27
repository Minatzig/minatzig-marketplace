# Writing rules for Minatzig documents

## Contents
- Why these rules
- Structure
- Sections that stand alone
- Wording
- Images
- Tables
- Questions customers ask
- Minimal example

## Why these rules

Minatzig splits each document into chunks by its headings. Each chunk is summarized, embedded and retrieved on its own, then filtered for relevance before an answer is written. A section that only makes sense next to the one before it will be retrieved badly or answered wrongly.

## Structure

- **One topic per document**: one product manual, one procedure, one set of FAQs. Not one huge file with everything. Several topics means several documents.
- **One `# H1` title**, once, at the top. It becomes the document title.
- **`##` for each topic or procedure**, `###` for steps or cases inside it. Prefer more, shorter sections over long ones.
- Headings say what the section answers, in the reader's words: `## Cómo dar de alta un cliente nuevo`, not `## Alta` or `## Sección 3`.

## Sections that stand alone

- Name the product (and the module or screen) in each section, not only in the title.
- When a procedure depends on another, name it: "Antes de esto, complete el alta de cliente". Never "as above", "see previous section" or "in the other document".
- Repeat a key condition rather than relying on an earlier section, for example "Esto solo está disponible en el plan Pro".

## Wording

- Direct sentences, written the way you would explain it to a customer (or to a colleague, for internal documents).
- Screen, menu and button names **exactly** as they appear in the product, in **bold**: `**Operaciones** > **Clientes** > **Nuevo**`.
- Numbered steps for procedures, each with the expected result: "Presione **Guardar**. El sistema muestra el número de cliente asignado."
- One term per concept throughout. Do not alternate between "cliente", "usuario" and "cuenta" for the same thing.
- No dates that will age ("desde el mes pasado"). Versions are set at upload.

## Images

- Use images only where they help: a screen, a form, an error message. Never decorative images (logos and separators are discarded anyway).
- Insert each image at the exact place it belongs: `![Formulario de alta de cliente](images/formulario-alta-cliente.png)`.
- The bracket text is a short description. The path is always relative to `images/`.
- Never `<img>` HTML tags and never web URLs. They are not processed.
- Minatzig replaces each image with a generated description plus the visible text it can read. So screenshots should be sharp, cropped to what matters, and free of real customer data.
- Do not rely on the image alone: the step text should say what to click even if the image fails.
- Accepted image types and size limits come from `get_authoring_guide`.

## Tables

Use Markdown tables for comparisons, parameters and error codes. Keep each table under the heading it belongs to, and give it a heading that says what it lists. Do not put whole procedures inside tables.

## Questions customers ask

Include the real questions the company receives, with their answers, worded the way customers write them by WhatsApp or email. Either:
- a `## Preguntas frecuentes` section with `### <question>` per question, or
- a separate FAQ document for the product.

Each answer must be complete without the rest of the document.

## Minimal example

```markdown
# Manual operativo: módulo Clientes

## Ingreso al módulo Clientes

Abra la aplicación y complete usuario y contraseña. Si es la primera vez,
el sistema pide cambiar la contraseña al ingresar.

![Pantalla de inicio de sesión](images/pantalla-login.png)

## Alta de un cliente nuevo en el módulo Clientes

1. En el menú **Operaciones**, elija **Clientes** y luego **Nuevo**.
2. Complete los datos obligatorios marcados con asterisco.
3. Presione **Guardar**. El sistema muestra el número de cliente asignado.

![Formulario de alta de cliente](images/formulario-alta-cliente.png)

### Errores frecuentes al dar de alta un cliente

| Mensaje | Causa | Solución |
|---|---|---|
| Documento ya registrado | El cliente ya existe | Buscarlo en **Clientes** |
| Sucursal inválida | Falta asignar sucursal | Elegir sucursal en el paso 2 |
```
