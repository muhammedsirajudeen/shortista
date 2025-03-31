import openai
from load_keys import OPENAI_KEY
def generate_title_from_ass(file_path='captions.ass'):

    # Set OpenAI API key
    openai.api_key = OPENAI_KEY

    # Read the .ass file and extract captions
    captions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("Dialogue:"):
                # Extract the text part of the dialogue
                parts = line.split(",", 9)  # The 10th part contains the actual text
                if len(parts) > 9:
                    captions.append(parts[9].strip())

    # Combine captions into a single prompt
    prompt = "Generate a concise and descriptive title for the following captions:\n\n" + "\n".join(captions)

    # Send the prompt to GPT
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the cheaper model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        # Extract and return the generated title
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating title: {e}")
        return None

# Example usage
# if __name__ == "__main__":
#     file_path = "caption.ass"
#     api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key
#     title = generate_title_from_ass(file_path, api_key)
#     if title:
#         print("Generated Title:", title)