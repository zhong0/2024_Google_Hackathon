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
    query_parts.append("{\"recommend_result\": {\"recommend_set\": [\"clothes_file_name_1\", \"clothes_file_name_2\"],\"description\": \"......\",\"style\": [\"style_1\", \"style_2\"]}}")
    query_parts.append("Recommended outfits must be complete ensembles.")
    query_parts.append("Recommended outfits set must be wearable at the same time.")
    query_parts.append("Descriptions must not mention the filename.")

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

    query_parts.append("Recommend as more as possible suitable outfits.")
    query_parts.append("the limitaion of outfits is " + str(recommend_count))
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")
    
    recommendations = [
        {
            "recommend_set": ["clothes_file_name_1", "clothes_file_name_2"],
            "description": "discription1",
            "style": ["style1", "style2", "style3"]
        },
        {
            "recommend_set": ["clothes_file_name_3", "clothes_file_name_4"],
            "description": "discription2",
            "style": ["style4", "style5", "style6"]
        }
    ]

    query_parts.append(json.dumps({"recommend_results": recommendations}))
    query_parts.append("Recommended outfits set must be wearable at the same time.")
    query_parts.append("Recommended outfits must be complete ensembles.")
    query_parts.append("Descriptions must not mention the filename.")

    query = "\n".join(query_parts)
    return query

def build_explore_pieces_recommend(user_clothes, shop_clothes, style, specific_clothes, recommend_count):
    query_parts = []

    query_parts.append("Here is all the information about the clothing.")
    query_parts.append(str(user_clothes))
    query_parts.append("Here is all the information about the shop's clothing.")
    query_parts.append(str(shop_clothes))

    query_parts.append("And must include the following specific clothes:")
    query_parts.append(str(specific_clothes))

    if style :
        query_parts.append("Please follow the information provided above and meet the following criteria:")
        query_parts.append(str(style))

    query_parts.append("Recommend as more as possible suitable clothes outfit for each specific clothes.")
    query_parts.append("the limitaion of outfits is " + str(recommend_count))
    query_parts.append("Your response should only be in a JSON format string, formatted as follows:")

    recommend_results = {
        "specific_clothes_filename_1": ["clothes_file_name_1", "clothes_file_name_2"],
        "specific_clothes_filename_2": ["clothes_file_name_3", "clothes_file_name_4"]
    }

    output_json = {
        "recommend_results": recommend_results
    }
                       
    json_str = json.dumps(output_json)
    query_parts.append(json_str)

    query_parts.append("Recommended clothing must not include any specific clothes.")

    query = "\n".join(query_parts)
    return query