def build_recommend_query(clothes, style, occasion, specific_clothes, history_recommend):
    # Initialize an empty list to hold parts of our query
    query_parts = []
    
    # Append parts of the query
    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(clothes))
    query_parts.append("Please follow the information provided above and meet the following criteria:")
    query_parts.append(str(style))
    query_parts.append(str(occasion))
    query_parts.append("And must include the following garments:")
    query_parts.append(str(specific_clothes))
    query_parts.append("And must not be any of the following combinations:")
    query_parts.append(str(history_recommend))
    query_parts.append("Recommend the most suitable outfit (at least two items).")
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    query_parts.append("{\"recommend_result\": {\"recommend_set\": [\"clothes_file_name_1\", \"clothes_file_name_2\"],\"description\": \"......\"}}")
    
    # Join all parts into a single string with newline separators
    query = "\n".join(query_parts)
    return query

def build_explore_query(user_clothes, shop_clothes, style, number_of_set):
    query_parts = []

    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(user_clothes))
    query_parts.append(str(shop_clothes))
    query_parts.append("Please follow the information provided above and meet the following criteria:")
    query_parts.append(str(style))
    query_parts.append("Recommend " + str(number_of_set) + " the most suitable outfit.")
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    query_parts.append("{\"recommend_result\": {\"recommend_set_1\": [\"clothes_file_name_1\", \"clothes_file_name_2\"],\"description\": \"......\",\"style\": [\"style1\", \"style2\"]}}")
    
    query = "\n".join(query_parts)
    return query

def build_specific_clothes_explore_query(user_clothes, shop_clothes, style, specific_clothes, number_of_set):
    query_parts = []

    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(user_clothes))
    query_parts.append(str(shop_clothes))
    query_parts.append("Please follow the information provided above and meet the following criteria:")
    query_parts.append(str(style))
    query_parts.append("Recommend " + str(number_of_set) + " the most suitable outfit.")
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    query_parts.append("{\"recommend_result\": {\"recommend_set_1\": [\"clothes_file_name_1\", \"clothes_file_name_2\"],\"description\": \"......\",\"style\": [\"style1\", \"style2\"]}}")
    
    query = "\n".join(query_parts)
    return query