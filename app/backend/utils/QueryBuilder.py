import json

def build_recommend_query(clothes, style, occasion, specific_clothes, history_recommend):
    # Initialize an empty list to hold parts of our query
    query_parts = []
    
    # Append parts of the query
    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(clothes))

    if style or occasion :
        query_parts.append("Please follow the information provided above and meet the following criteria:")
        query_parts.append(str(style))
        query_parts.append(str(occasion))

    if specific_clothes:
        query_parts.append("And must include the following garments:")
        query_parts.append(str(specific_clothes))

    if history_recommend:    
        query_parts.append("And must not be any of the following combinations:")
        query_parts.append(str(history_recommend))

    query_parts.append("Recommend the most suitable outfit.")
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    query_parts.append("{\"recommend_result\": {\"recommend_set\": [\"clothes_file_name_1\", \"clothes_file_name_2\"],\"description\": \"......\"}}")
    
    query = "\n".join(query_parts)
    return query

def build_explore_query(user_clothes, shop_clothes, style, recommend_count):
    query_parts = []

    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(user_clothes))
    query_parts.append("Here is all the information about the shop's clothing.")
    query_parts.append(str(shop_clothes))

    if style :
        query_parts.append("Please follow the information provided above and meet the following criteria:")
        query_parts.append(str(style))

    query_parts.append("Recommend the " + str(recommend_count) + " most suitable outfits.")
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    
    recommendations = [
        {
            "recommend_set": ["clothes_file_name_1", "clothes_file_name_2"],
            "description": "discription1",
            "style": ["style1", "style2"]
        },
        {
            "recommend_set": ["clothes_file_name_3", "clothes_file_name_4"],
            "description": "discription2",
            "style": ["style3", "style4"]
        }
    ]

    query_parts.append(json.dumps({"recommend_results": recommendations}))

    query = "\n".join(query_parts)
    return query

def build_explore_pieces_recommend(user_clothes, shop_clothes, style, specific_clothes, recommend_count):
    query_parts = [
        "Here is all the information about the clothing from the user and shop:",
        json.dumps(user_clothes, indent=2),
        json.dumps(shop_clothes, indent=2),
        "The recommendation must include the following specific garments:",
        json.dumps(specific_clothes, indent=2)
    ]

    if style:
        query_parts.append("Please follow the style criteria provided above:")
        query_parts.append(json.dumps(style, indent=2))

    query_parts.append(f"Recommend the top {recommend_count} most suitable clothes outfits including specified garments. Response format:")
    query_parts.append(json.dumps(["clothes_file_name_1", "clothes_file_name_2"], indent=2))

    return "\n".join(query_parts)