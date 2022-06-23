import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launchRequest(handler_input): 
    characterQuestionList = [" ","What's is the dragon's name in Mulan?",  "What kind of animal is Bambi?", "What is the name of the snowman in Frozen", "What is the name of the crab in the little mermaid",  "What is Boo's nickname for Sully in Monster.Inc"]
    characterAnswerList = [" ", "Mushu", "deer", "Olaf", "Sebastian", "Kitty"]
    playerPoints = 0
    pointList = [" ","100","200","300","400","500"]
    handler_input.attributes_manager.session_attributes["pointList"] = pointList
    handler_input.attributes_manager.session_attributes["characterQuestionList"] = characterQuestionList
    handler_input.attributes_manager.session_attributes["characterAnswerList"] = characterAnswerList
    handler_input.attributes_manager.session_attributes["playerPoints"] = playerPoints
    
    speechOutput = "Hello player! Welcome to Jeopardy. Choose a point value for your first question(100,200,300,400,500). " 
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .ask(speechOutput)
        .response
    )
@sb.request_handler(can_handle_func=is_intent_name("PointIntent"))
def PointIntent(handler_input): 
    pointList = handler_input.attributes_manager.session_attributes["pointList"]
    pointValue = handler_input.request_envelope.request.intent.slots["points"].value
    Index = int(pointValue)/100
    points = pointList[int(Index)]
    handler_input.attributes_manager.session_attributes["points"] = points
    
    handler_input.attributes_manager.session_attributes["Index"] = Index
    speechOutput =  "Enter category: "
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .set_should_end_session(False)
        .response
    )
@sb.request_handler(can_handle_func=is_intent_name("CharactersIntent"))
def CharactersIntent(handler_input): 
    Index = handler_input.attributes_manager.session_attributes["Index"]
    characterQuestionList = handler_input.attributes_manager.session_attributes["characterQuestionList"]
    question = characterQuestionList[int(Index)]
    
    speechOutput =  question
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .set_should_end_session(False)
        .response
    )

@sb.request_handler(can_handle_func=is_intent_name("AnswerIntent"))
def AnswerIntent(handler_input): 
    userAnswer = handler_input.request_envelope.request.intent.slots["answer"].value
    points = handler_input.attributes_manager.session_attributes["points"]
    characterAnswerList = handler_input.attributes_manager.session_attributes["characterAnswerList"] 
    Index = handler_input.attributes_manager.session_attributes["Index"]
    playerPoints  = handler_input.attributes_manager.session_attributes["playerPoints"] 
    answer =  characterAnswerList[int(Index)]
    #deleting question, answer and point value in list
    handler_input.attributes_manager.session_attributes["playerPoints"] += int(points)
    handler_input.attributes_manager.session_attributes["characterQuestionList"].pop(int(Index))
    handler_input.attributes_manager.session_attributes["characterAnswerList"].pop(int(Index))
    handler_input.attributes_manager.session_attributes["pointList"].pop(int(Index))
    
    #insert empty space
    handler_input.attributes_manager.session_attributes["characterQuestionList"].insert(int(Index)," ")
    
    handler_input.attributes_manager.session_attributes["pointList"].insert(int(Index)," ")
    handler_input.attributes_manager.session_attributes["characterAnswerList"].insert(int(Index)," ")
    speechPoint = " "
    for x in range(len(handler_input.attributes_manager.session_attributes["pointList"])):
        speechPoint += handler_input.attributes_manager.session_attributes["pointList"][x] 
        speechPoint += ", "
    if (userAnswer.lower() == answer.lower()):
        
        speechOutput = "Congrats, you got it your have " + str(handler_input.attributes_manager.session_attributes["playerPoints"] ) + " points. Choose the points value for your next question("  + speechPoint +")"
    else:
        
        speechOutput = "you got it wrong"
    return(
        handler_input.response_builder.speak(speechOutput)
        .set_should_end_session(False)
        .response
    )
@sb.request_handler(can_handle_func=is_intent_name("NextQuestionIntent"))
def NextQuestionIntent(handler_input): 
    Index = handler_input.attributes_manager.session_attributes["Index"]
    characterQuestionList = handler_input.attributes_manager.session_attributes["characterQuestionList"]
    question = characterQuestionList[int(Index)]
    speechOutput =  question
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .set_should_end_session(False)
        .response
    )
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def helpIntent(handler_input): 
    speechOutput = "You can say hello to me! How can I help?"
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .set_should_end_session(False)
        .response
        )

@sb.request_handler(can_handle_func=lambda input: 
    is_intent_name("AMAZON.CancelIntent")(input) or 
    is_intent_name("AMAZON.StopIntent")(input))
def cancelOrStopIntent(handler_input): 
    speechOutput = "Okay, see you later"
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .response
    )

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallbackIntent(handler_input): 
    speechOutput = "Hmm, I'm not sure I caught that. You can say hello or help"
    reprompt = "I didn't catch that. What can I help you with?"
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .ask(reprompt)
        .response
    )

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def sessionEndedRequest(handler_input): 
    logger.info("Session ended with reason: {}".format(
        handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_request_type("IntentRequest"))
def intentReflectorHandler(handler_input): 
    intentName = ask_utils.get_intent_name(handler_input)
    speechOutput = "You just triggered " + intentName + "."
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .response
    )

@sb.request_handler(can_handle_func=lambda i,e: True)
def catchAllHandler(handler_input, exception): 
    logger.error(exception, exc_info = True)
    speechOutput = "Sorry, I had trouble doing what you asked. Please try again."
    
    return(
        handler_input.response_builder.speak(speechOutput)
        .ask(speechOutput)
        .response
        )

lambda_handler = sb.lambda_handler()