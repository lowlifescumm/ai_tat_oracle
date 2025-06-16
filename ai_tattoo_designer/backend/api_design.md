# AI Tattoo Designer API Design

## Endpoint: `/generate_tattoo`

- **Method**: `POST`
- **Description**: Generates a unique tattoo design concept and an image based on user information.

### Request Body (JSON):
```json
{
  "first_name": "string",
  "last_name": "string",
  "date_of_birth": "dd/mm/yyyy",
  "age": "integer"
}
```

### Response Body (JSON):
```json
{
  "symbolic_analysis": "string",
  "core_tattoo_theme": "string",
  "visual_motif_description": "string",
  "placement_suggestion": "string",
  "mystical_insight": "string",
  "image_url": "string" // URL to the generated image
}
```

## Error Handling:
- Invalid input will result in a 400 Bad Request with an error message.
- Internal server errors will result in a 500 Internal Server Error.

