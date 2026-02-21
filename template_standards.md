# Django Template Best Practices & Patterns

To maintain a stable and error-free inventory system, follow these standardized patterns for template logic.

## 1. Conditionals (If/Elif)
Always include spaces around comparison operators. Never split tags across multiple lines.

**Incorrect:**
```html
{% if count<=0 %}...{% endif %}
{% if status == 
   code %}...{% endif %}
```

**Correct:**
```html
{% if count <= 0 %}...{% endif %}
{% if status == code %}...{% endif %}
```

## 2. Loops and Empty States
Use `{% empty %}` directly within `{% for %}` loops for empty state handling. Do not use `{% else %}` inside a `for` block unless it belongs to a nested `if`.

**Incorrect:**
```html
{% for item in items %}
    ...
{% else %}
    No items found.
{% endfor %}
```

**Correct:**
```html
{% for item in items %}
    ...
{% empty %}
    No items found.
{% endfor %}
```

## 3. Comparison Operators
Always use the combined character form without internal spaces.

| Operator | Pattern |
| :--- | :--- |
| Equals | `==` |
| Not Equals | `!=` |
| Less Than or Equal | `<=` |
| Greater Than or Equal | `>=` |

## 4. Heavy Logic
Avoid complex math or property lookups that might return `None` without safe guards.

**Bad:** `{{ item.price * item.tax_rate }}` (Django doesn't support math in templates like this).
**Good:** Implement a `@property` or method in the `models.py` and call `{{ item.total_price_with_tax }}`.

## 5. Tag Integrity
Always close tags on the same line they start if they contain logic, to avoid parsing ambiguity.

**Good:** `{% if condition %} Result {% endif %}`
