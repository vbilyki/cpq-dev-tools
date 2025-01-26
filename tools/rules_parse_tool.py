def find_reference_values_and_data_fields(json_obj):
    """
    Searches for values associated with 'op': '$lookup' or '$fm' and data field names
    in 'update_quote_data_fields_values' commands in a JSON structure.

    :param json_obj: The JSON object to search.
    :return: A tuple containing two lists:
             - lookup_values: List of values found for '$lookup' or '$fm'.
    """
    lookup_values = []

    if isinstance(json_obj, dict):
        # Check for 'op': '$lookup' or '$fm'
        if json_obj.get("op") in {"$lookup", "$fm"}:
            lookup_values.append(json_obj.get("value"))

        # Check for 'update_quote_data_fields_values' command
        if json_obj.get("name") == "update_quote_data_fields_values":
            args = json_obj.get("args", {})
            data_fields = args.get("data_fields", [])
            for field in data_fields:
                if "name" in field:
                    lookup_values.append("quote_ctx.quote.data_fields_map." + field["name"])

        # Recursively process all dictionary values
        for value in json_obj.values():
            lv = find_reference_values_and_data_fields(value)
            lookup_values.extend(lv)

    elif isinstance(json_obj, list):
        # Recursively process all items in the list
        for item in json_obj:
            lv = find_reference_values_and_data_fields(item)
            lookup_values.extend(lv)

    return lookup_values
