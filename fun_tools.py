from llama_index.core.tools import FunctionTool
from deep_translator import GoogleTranslator

def get_tools(query_engine):
    # Relating problems to Ramayana story
    def relate_problem_to_story(problem):
        # This function relates user problems to a story in Ramayana and suggests a solution
        result = query_engine.query(f"Relate this problem to a story in Ramayana and provide a solution: {problem}")
        return f"Based on your problem, here is how it relates to Ramayana:\n{result}"

    problemSolve = FunctionTool.from_defaults(
        fn=relate_problem_to_story,
        name="RelateProblem",
        description="This tool connects user problems with relevant stories from the Ramayana, offering insights into how similar issues were addressed within the text. It analyzes the user’s input and suggests examples from the Ramayana where characters faced comparable challenges, illustrating how they solved these problems. The tool provides users with practical, actionable advice inspired by the teachings of the Ramayana, helping them reflect on how ancient wisdom can be applied to modern-day situations."
    )

    # Generating slokas on different contexts
    def generate_sloka(context, language='telugu'):
        # This function generates a sloka based on the context
        sloka_query = f"Generate a sloka relevant to the context: {context}, in language{language} base on your knowledge base"
        result = query_engine.query(sloka_query)
        return result

    generateSloka = FunctionTool.from_defaults(
        fn=generate_sloka,
        name="GenerateSloka",
        description="This tool generates slokas (verses) on user requested language from the Ramayana based on user-provided contexts or topics. Whether the user seeks verses related to emotions such as courage, devotion, or sorrow, or wishes to explore specific themes like dharma (duty), karma (action), or bhakti (devotion), this tool identifies and delivers relevant slokas. It enables the user to experience the poetic and philosophical essence of the Ramayana in the form of appropriate verses."
    )

    # Interacting as a character from Ramayana
    def interact_as_character(character_name, user_query):
        # This function interacts as a specified character from Ramayana
        interaction_query = f"Assume the role of {character_name} from Ramayana and respond to: {user_query}"
        result = query_engine.query(interaction_query)
        return result

    rollPlay = FunctionTool.from_defaults(
        fn=interact_as_character,
        name="InteractAsCharacter",
        description="This tool allows users to engage in interactive dialogue with characters from the Ramayana. The user can specify a particular character—such as Rama, Sita, Hanuman, or Ravana or any other charectes in ramanaya—and the tool will simulate a conversation in the voice and personality of that character. It draws on the character’s attributes, experiences, and wisdom to offer responses that are true to their portrayal in the Ramayana, creating an immersive role-playing experience for the user."
    )

    # Translating Sanskrit words into English
    def translate_sanskrit(word):
        try:
            translator = GoogleTranslator(source='auto', target='en')
            translation = translator.translate(word)
            return translation
        except Exception as e:
            print(f"Error translating: {e}")
            return "Translation error."

    translateSanskrit = FunctionTool.from_defaults(
        fn=translate_sanskrit,
        name="TranslateSanskrit",
        description="This tool provides accurate translations of Sanskrit words or phrases from the Ramayana into English. Whether the user seeks to understand the meaning of specific slokas, names, or terms, this tool offers clear and precise translations. By breaking down complex Sanskrit language constructs into understandable English, it enhances the user’s comprehension of the Ramayana’s teachings, making the ancient text accessible to those unfamiliar with Sanskrit."
    )

    # Return the list of tools
    return [translateSanskrit, rollPlay, generateSloka, problemSolve]
