from datetime import datetime
from typing import List, Dict, Any


def validate_user_data(
    fields: List[Dict[str, Any]], data: Dict[str, Any]
) -> Dict[str, Any]:
    validated_data = {}

    for field in fields:
        name = field["name"]
        field_type = field["type"]
        required = field["required"]
        options = field.get("options")

        raw_value = data.get(name)

        # Check required
        if required and (
            raw_value is None
            or raw_value == ""
            or (isinstance(raw_value, list) and len(raw_value) == 0)
        ):
            return {"valid": False, "error": f"{name} is required"}

        # If not required and empty, skip validation but store default
        if raw_value is None or raw_value == "":
            validated_data[name] = None
            continue

        try:
            # Typecast and validate
            if field_type in ("text", "textarea"):
                value = str(raw_value)

            elif field_type in ("select", "radio"):
                value = str(raw_value)
                if options and value not in options:
                    return {
                        "valid": False,
                        "error": f"{name} has invalid option: {value}",
                    }

            elif field_type == "checkbox":
                if isinstance(raw_value, str):
                    # Convert comma-separated string to list
                    value = [v.strip() for v in raw_value.split(",")]
                elif isinstance(raw_value, list):
                    value = raw_value
                else:
                    return {
                        "valid": False,
                        "error": f"{name} should be a list or string",
                    }

                if options:
                    for v in value:
                        if v not in options:
                            return {
                                "valid": False,
                                "error": f"{name} has invalid option: {v}",
                            }

            elif field_type == "number":
                pass

            elif field_type == "date":
                try:
                    # Accept both date object and ISO string
                    if isinstance(raw_value, datetime):
                        value = raw_value
                    else:
                        value = datetime.fromisoformat(str(raw_value))
                except Exception:
                    return {
                        "valid": False,
                        "error": f"{name} should be a valid ISO date string",
                    }

            elif field_type == "file":
                value = raw_value  # Skip file validation for now

            else:
                return {"valid": False, "error": f"Unknown field type: {field_type}"}

            validated_data[name] = value

        except Exception as e:
            return {"valid": False, "error": f"{name} validation failed: {str(e)}"}

    return {"valid": True, "data": validated_data}
