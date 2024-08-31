from openai import OpenAI
from dotenv import load_dotenv
from .messages import INITIAL_SYSTEM_MESSAGE, SYSTEM_MESSAGE

load_dotenv()
client_openai = OpenAI()


def get_ai_answer(prompt):
    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            timeout=10
        )
        response = response.choices[0].message.content
        print(f"✅ Successfully generated AI response!")
        return response

    except Exception as e:
        print(f"❌ Error generating AI response: {e}")
        return None


def insert_line_breaks(text, max_length=200):
    words = text.split()
    current_line = ""
    formatted_text = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (word + " ")
        else:
            formatted_text += current_line.strip() + "\n"
            current_line = word + " "

    formatted_text += current_line.strip()  # Add the last line

    return formatted_text


def construct_prompt(user_query, top_n_documents, chat_history):
    fragments = ""
    for i, doc in enumerate(top_n_documents):
        chunk_text = insert_line_breaks(doc['chunk_text'])

        fragments += f'''
            FRAGMENT {i + 1} - pochodzi z: {doc['metadata']['filename']}:
            {chunk_text}
            '''

    main_query = f'''
        Proszę odpowiedz na poniższe pytanie:
        {user_query}

        {'=' * 60}
        Poniżej znajdują się fragmenty instrukcji gier planszowych, które mogą okazać się przydatne:
        {fragments}
        {'=' * 60}
        Jeżeli nie znasz odpowiedzi na pytanie oraz jeżeli nie znajduje się ona w powyższych fragmentach instrukcji, napisz, że nie znasz odpowiedzi.
        '''

    if not chat_history:
        messages = [
            {"role": "system", "content": INITIAL_SYSTEM_MESSAGE},
            {"role": "user", "content": main_query}
        ]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            *chat_history,
            {"role": "user", "content": main_query}
        ]

    print(f'PROMPT:\n{main_query}\n')
    return messages



