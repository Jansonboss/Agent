import logging

from googlesearch import search


def public_search(query: str, domain: str):
    if domain not in ["IT"]:
        return "Inform user {query} is out of scope for. In addition, no need to search on this again."

    results = "\n".join([
        f"Title: {s.title}. Content: {s.description}. Url: {s.url}"
        for s in search(query, 3, advanced=True)
    ])

    print("===============================Google Search Retrieval Start=============================")
    for i in results.split("\n"):
        print("=====" + i)
    print("================================Google Search Retrieval End=============================")
    print()

    return results


def send_email(parameters):
    print(parameters)


FUNCTIONS = [
    {
        "name": "send_email",
        "description": "send email in an polite and professional way.",
        "parameters": {
            "type": "object",
            "properties": {
                "to_address": {
                    "type": "string",
                    "description": "The email address you wanna send it to."
                },
                "body": {
                    "type": "string",
                    "description": "The email content"
                }
            }
        }
    },

    {
        "name": "public_search",
        "description": "Searches for specified content in a database.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "domain": {
                    "type": "string",
                    "enum": ["IT", "HR", "Others"],
                    "description": "check which domain user request belows to. Could be (IT, HR, or Others)"
                }
            },
            "required": ["query", "domain"]
        }
    },
    # {
    #     "name": "convert_currency",
    #     "description": "Converts an amount from one currency to another.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "amount": {
    #                 "type": "number",
    #                 "description": "Amount to convert"
    #             },
    #             "from_currency": {
    #                 "type": "string",
    #                 "description": "Source currency code"
    #             },
    #             "to_currency": {
    #                 "type": "string",
    #                 "description": "Target currency code"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "generate_report",
    #     "description": "Generates a report based on provided data.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "data": {
    #                 "type": "array",
    #                 "description": "Data for the report"
    #             },
    #             "format": {
    #                 "type": "string",
    #                 "enum": ["PDF", "Excel", "HTML"],
    #                 "description": "Report format"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "send_notification",
    #     "description": "Sends a notification to a user.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "user_id": {
    #                 "type": "string",
    #                 "description": "Unique identifier for the user"
    #             },
    #             "message": {
    #                 "type": "string",
    #                 "description": "Notification message"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "plot_graph",
    #     "description": "Plots a graph based on input data.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "data": {
    #                 "type": "array",
    #                 "description": "Data points for the graph"
    #             },
    #             "type": {
    #                 "type": "string",
    #                 "enum": ["line", "bar", "pie"],
    #                 "description": "Type of graph"
    #             },
    #             "title": {
    #                 "type": "string",
    #                 "description": "Title of the graph"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "create_user",
    #     "description": "Creates a new user in the system.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "username": {
    #                 "type": "string",
    #                 "description": "Desired username"
    #             },
    #             "password": {
    #                 "type": "string",
    #                 "description": "User's password"
    #             },
    #             "email": {
    #                 "type": "string",
    #                 "description": "User's email address"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "book_appointment",
    #     "description": "Books an appointment for a service.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "service_id": {
    #                 "type": "string",
    #                 "description": "Identifier for the service"
    #             },
    #             "date": {
    #                 "type": "string",
    #                 "description": "Date for the appointment"
    #             },
    #             "time": {
    #                 "type": "string",
    #                 "description": "Time for the appointment"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "check_weather",
    #     "description": "Checks the weather for a given location.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "location": {
    #                 "type": "string",
    #                 "description": "Location to check the weather for"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "analyze_text",
    #     "description": "Performs sentiment analysis on the provided text.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "text": {
    #                 "type": "string",
    #                 "description": "Text to analyze"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "get_commands",
    #     "description": "Get a list of bash commands on an Ubuntu machine",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "commands": {
    #                 "type": "array",
    #                 "items": {
    #                     "type": "string",
    #                     "description": "A terminal command string"
    #                 },
    #                 "description": "List of terminal command strings to be executed"
    #             }
    #         },
    #         "required": ["commands"]
    #     }
    # },
    # {
    #     "name": "calculate_tax",
    #     "description": "Calculates tax based on income and region.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "income": {
    #                 "type": "number",
    #                 "description": "Annual income"
    #             },
    #             "region": {
    #                 "type": "string",
    #                 "description": "Region for tax calculation"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "track_package",
    #     "description": "Tracks a package based on its tracking number.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "tracking_number": {
    #                 "type": "string",
    #                 "description": "Package tracking number"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "resize_image",
    #     "description": "Resizes an image to specified dimensions.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "image_path": {
    #                 "type": "string",
    #                 "description": "Path to the image file"
    #             },
    #             "width": {
    #                 "type": "number",
    #                 "description": "Desired width in pixels"
    #             },
    #             "height": {
    #                 "type": "number",
    #                 "description": "Desired height in pixels"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "translate_text",
    #     "description": "Translates text from one language to another.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "text": {
    #                 "type": "string",
    #                 "description": "Text to translate"
    #             },
    #             "source_language": {
    #                 "type": "string",
    #                 "description": "Language code of the source text"
    #             },
    #             "target_language": {
    #                 "type": "string",
    #                 "description": "Language code of the target text"
    #             }
    #         }
    #     }
    # },
    # {
    #     "name": "generate_password",
    #     "description": "Generates a strong, random password.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "length": {
    #                 "type": "number",
    #                 "description": "Length of the password"
    #             },
    #             "include_symbols": {
    #                 "type": "boolean",
    #                 "description": "Whether to include symbols in the password"
    #             },
    #             "include_numbers": {
    #                 "type": "boolean",
    #                 "description": "Whether to include numbers in the password"
    #             }
    #         }
    #     }
    # }
]