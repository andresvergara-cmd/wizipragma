"""Module: Config Class"""

# ───────────────────────────────────────────── IMPORTS ─────────────────────────────────────────────
import os
from loguru import logger
import boto3
from boto3.dynamodb.conditions import Key
from bedrock_config import stream_chat


# ────────────────────────────────── ENV VARIABLES + AWS RESOURCES ──────────────────────────────────
REGION_NAME = os.environ.get('REGION_NAME')
bedrock_service = boto3.client('bedrock-runtime')
agent_service = boto3.client('bedrock-agent-runtime', region_name=REGION_NAME)
dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)


# ──────────────────────────────────────────── METHODS ──────────────────────────────────────────────
class ConfigChat:

    def __init__(self):
        self.ch_table_name = os.environ.get('CHAT_HISTORY_TABLE')
        self.ch_table = dynamodb.Table(os.environ.get('CHAT_HISTORY_TABLE'))
        self.model_id = os.environ.get('MODEL_ID')
        self.table_names = {
            "profile": "poc-wizi-dyn-users-table",
            "transactions": "poc-wizi-dyn-transactions-table",
            "retailers": "poc-wizi-dyn-retailers-table"
        }

    def get_session_data(self, session_id: str):
        """Query user data from DynamoDB based on the session id."""
        try:
            response = self.ch_table.query(
                KeyConditionExpression=Key('session_id').eq(f"{session_id}"),
                Limit=1
            )

            return response['Items']
        except Exception as e:
            err_msg = f"Error retrieving user data for category: {session_id}. Error: {e}"
            logger.exception(err_msg)
            return []

    def delete_session(self, session_id: str):
        """Delete current session"""
        try:
            _ = self.ch_table.delete_item(
                Key={'session_id': session_id}
            )
        except Exception as e:
            logger.exception(f'Error while deleting item: {str(e)}')

    def retrieve_chat_history(self, session_id: str):
        """Retrieve Actual Chat History"""
        session_data = self.get_session_data(session_id=session_id)

        conversation = []
        if session_data:
            conversation = session_data[0]['conversation']
            self.delete_session(session_id)

        chat_history = {
            'session_id': session_id,
            'conversation': conversation
        }

        return chat_history

    def update_chat_history(
            self, 
            chat_history: dict,
            question: str,
            response: str
        ):
        """"Update Chat History with last response"""
        chat_history['conversation'].append({
            'user_question': question,
            'agent_response': response
        })
        logger.info('New interaction added successfully!')

        self.ch_table.put_item(Item=chat_history)
        logger.info('Chat updated successfully')

    def limit_conversation_history(self, messages: list, max_turns: int = 5) -> list:
        """
        Limits the history to control tokens (optional)
        Keeps the last N conversation shifts
        """
        if len(messages) <= max_turns:
            return messages

        return messages[-(max_turns):]

    def parse_conversation_history(
            self,
            chat_history: list,
            limit_conversation: bool = False,
            max_turns: int = 5
        ) -> list:
        """
        Converts DynamoDB JSON to the format required by Bedrock
        """
        messages = []

        try:
            conversation_history = chat_history.get('conversation', [])
            if limit_conversation and conversation_history:
                conversation_history = self.limit_conversation_history(
                    conversation_history,
                    max_turns
                )
                logger.info(f'History successfully truncated')

            for entry in conversation_history:
                user_question = entry["user_question"]
                agent_response = entry["agent_response"]
                
                messages.append({
                    "role": "user",
                    "content": [{"text": user_question}]
                })

                messages.append({
                    "role": "assistant", 
                    "content": [{"text": agent_response}]
                })

            return messages
        except Exception as e:
            logger.warning(f'Error parsing user conversation history. Error: {str(e)}')
            return []

    def chat_with_bedrock(
            self,
            user_query: str,
            user_context: str,
            connection_id: str,
            session_id: str,
            limit_chat_history: bool = False,
            max_turns: int = 5
        ):
        """Send question to Bedrock"""
        try:
            logger.info(f'Retrieving and processing user chat history...')
            chat_history = self.retrieve_chat_history(session_id=session_id)

            processed_chat = []
            if chat_history.get('conversation'):
                processed_chat = self.parse_conversation_history(
                    chat_history=chat_history,
                    limit_conversation=limit_chat_history,
                    max_turns=max_turns

                )
                inf_msg = f'Number of interactions retrieved from conversation history: {len(processed_chat)}'
                logger.info(inf_msg)

            logger.info('Generating user response...')
            bedrock_response = stream_chat(
                model_id=self.model_id,
                user_context=user_context,
                user_message=user_query,
                user_hist_conversation=processed_chat,
                connection_id=connection_id
            )

            if bedrock_response:
                self.update_chat_history(
                    chat_history=chat_history,
                    question=user_query,
                    response=bedrock_response
                )

            return bedrock_response
        except Exception as e:
            err_msg = f'[ERROR] generating response. Error: {str(e)}'
            logger.exception(err_msg)
            raise e


# ───────────────────────────────────────────────────────────────────────────────────────────────────
config = ConfigChat()
